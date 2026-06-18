import os
import requests
import feedparser
from datetime import datetime, timezone

GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
DISCORD_WEBHOOK_URL = os.environ["DISCORD_WEBHOOK_URL"]

# 수집 소스
SOURCES = [
    "https://hnrss.org/frontpage?count=30",
    "https://www.reddit.com/r/MachineLearning/top/.rss?t=day",
    "https://www.reddit.com/r/ExperiencedDevs/top/.rss?t=day",
    "https://www.reddit.com/r/programming/top/.rss?t=day",
]

def fetch_rss(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0 (trend-bot/1.0)"}
        feed = feedparser.parse(url, request_headers=headers)
        items = []
        for entry in feed.entries[:10]:
            items.append({
                "title": entry.get("title", ""),
                "link": entry.get("link", ""),
                "summary": entry.get("summary", "")[:200],
            })
        return items
    except Exception as e:
        print(f"RSS 수집 실패 ({url}): {e}")
        return []

def collect_all_trends():
    all_items = []
    for url in SOURCES:
        items = fetch_rss(url)
        all_items.extend(items)
        print(f"수집: {url} → {len(items)}개")
    return all_items

def extract_keywords_with_gemini(items):
    # 제목 + 링크 함께 전달
    articles = "\n".join([f"- {item['title']} | {item['link']}" for item in items])

    prompt = f"""아래는 오늘 HackerNews와 Reddit에서 수집한 핫한 주제들이야. (형식: 제목 | 링크)

{articles}

위 내용을 분석해서 아래 세 카테고리별로 오늘 가장 주목할 만한 주제 3개씩 뽑아줘.

카테고리:
1. AI/LLM
2. 백엔드/개발
3. 요즘 핫한 주제 (기술 트렌드, 업계 이슈 등)

각 주제는 반드시 다음 형식으로 작성해:
- 주제 제목 (한 줄 요약)
- 왜 지금 핫한지 한 문장
- LinkedIn 포스팅에 쓸 수 있는 각도 한 가지 제안
- 🔗 원문: [위에서 받은 링크 그대로]

마지막에 오늘 전체를 관통하는 키워드 3개도 뽑아줘."""

    response = requests.post(
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent?key={GEMINI_API_KEY}",
        headers={"content-type": "application/json"},
        json={
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"maxOutputTokens": 2000},
        },
    )

    if response.status_code == 200:
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]
    else:
        raise Exception(f"Gemini API 오류: {response.status_code} {response.text}")

def send_to_discord(content):
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    message = {
        "embeds": [
            {
                "title": f"📊 오늘의 트렌드 키워드 — {today}",
                "description": content,
                "color": 0x5865F2,
                "footer": {
                    "text": "💡 원하는 주제 번호 + 내 생각을 답장하면 LinkedIn 초안을 작성해드릴게요"
                },
            }
        ]
    }

    response = requests.post(DISCORD_WEBHOOK_URL, json=message)
    if response.status_code in (200, 204):
        print("Discord 전송 완료")
    else:
        raise Exception(f"Discord 전송 실패: {response.status_code} {response.text}")

def main():
    print("트렌드 수집 시작...")
    items = collect_all_trends()
    print(f"총 {len(items)}개 항목 수집")

    print("Gemini로 키워드 추출 중...")
    summary = extract_keywords_with_gemini(items)

    print("Discord 전송 중...")
    send_to_discord(summary)

    print("완료!")

if __name__ == "__main__":
    main()
