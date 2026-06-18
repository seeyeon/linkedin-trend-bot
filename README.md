# 📊 LinkedIn Trend Bot

매일 아침 HackerNews·Reddit 트렌드를 수집해서 Discord로 LinkedIn 포스팅 주제를 던져주는 봇.

## 흐름

```
매일 오전 8시 (GitHub Actions)
→ HackerNews + Reddit 트렌드 수집
→ Claude API로 AI/LLM, 백엔드/개발, 핫한 주제 키워드 추출
→ Discord로 오늘의 주제 3개 전송
→ 내가 "2번 주제 + 내 생각" 답장
→ Claude가 LinkedIn 초안 작성 (2단계 예정)
```

## 설치 방법

### 1. 레포 Fork

우상단 Fork 버튼 클릭

### 2. GitHub Secrets 등록

레포 → Settings → Secrets and variables → Actions → New repository secret

| Secret 이름 | 값 |
|---|---|
| `GEMINI_API_KEY` | Google AI Studio API Key (무료) |
| `DISCORD_WEBHOOK_URL` | Discord 채널 Webhook URL |

### 3. Actions 활성화

레포 → Actions 탭 → "I understand my workflows" 클릭

### 4. 수동 테스트

Actions → Daily Trend Bot → Run workflow

## 커스터마이징

`scripts/trend_bot.py` 상단 `SOURCES` 리스트에서 RSS 소스 추가/제거 가능.

## 비용

- GitHub Actions: 무료 (월 2,000분 제공)
- Gemini API: 무료 (하루 1,500 요청 제공, 이 봇은 하루 1회라 충분)

## 로드맵

- [x] 1단계: 매일 트렌드 Discord 알림
- [ ] 2단계: Discord 답장 → LinkedIn 초안 자동 작성
- [ ] 3단계: Hermes Skill로 포팅
