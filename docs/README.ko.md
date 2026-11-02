# 🐾 AutoClaw Daily

AutoClaw 중국판과 국제판의 일일 체크인을 자동화하는 단일 파일 Python 도구입니다. 다중 계정을 지원하며 중국판 자격 증명을 자동으로 갱신할 수 있습니다.

[简体中文](../README.md) · [English](README.en.md) · [繁體中文](README.zh-Hant.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Português (BR)](README.pt-BR.md)

전체 중국어 문서는 [../README.md](../README.md)에서 확인하세요.

## 주요 기능

- `daily_signin`을 호출해 AutoClaw 중국판 일일 체크인을 수행합니다.
- `refresh_token`으로 중국판 액세스 토큰을 갱신하고 교체된 자격 증명을 로컬에 저장합니다.
- 데스크톱 앱의 `openclaw.json`에서 국제판 토큰을 추출하고 국제 리전에서 사용할 수 있는지 검증합니다.
- 체크인 후 포인트 원장을 읽고 `metadata.event_type`을 기준으로 당일 활동 보상을 확인합니다.
- 줄바꿈 또는 `&`로 구분한 다중 계정과 PushPlus, Bark, WeCom, DingTalk, Qinglong 알림을 지원합니다.

## Qinglong 최소 설정

```bash
python3 -m pip install -r requirements.txt
```

`autoclaw_cn_daily.py` 또는 `autoclaw_intl_daily.py`를 업로드하고 계정 변수를 설정한 뒤 패널 러너로 작업을 만듭니다.

```text
35 8 * * * task autoclaw_cn_daily.py
35 8 * * * task autoclaw_intl_daily.py
```

중국판 로그인과 국제판 토큰 추출:

```bash
python autoclaw_login.py --verify
python autoclaw_login.py --extract-intl
```

## GitHub Actions

**Settings → Secrets and variables → Actions**에서 필요한 Secrets를 만들고 Actions 탭에서 `AutoClaw Daily`를 수동 실행하세요.

```text
AUTOCLAW_CN_TOKENS
AUTOCLAW_INTL_TOKENS
PUSHPLUS_TOKEN          # 선택
BARK_URL                # 선택
WECOM_WEBHOOK           # 선택
DINGTALK_WEBHOOK        # 선택
DINGTALK_SECRET         # 선택
```

워크플로는 기본적으로 수동 실행만 허용합니다. 주석 처리된 스케줄을 사용하려면 `.github/workflows/daily.yml`을 수정하세요. cron은 UTC 기준입니다.

## 핵심 환경 변수

| 변수 | 용도 |
| :--- | :--- |
| `AUTOCLAW_CN_TOKENS` | 중국판 계정. `token`, `token\|refresh_token\|device_id`, `note\|token\|refresh_token\|device_id` 지원 |
| `AUTOCLAW_INTL_TOKENS` | 국제판 계정. 데스크톱 추출은 보통 `token`만 제공 |
| `PUSHPLUS_TOKEN`, `BARK_URL`, `WECOM_WEBHOOK`, `DINGTALK_WEBHOOK`, `DINGTALK_SECRET` | 선택 알림 채널 |
| `QL_URL`, `QL_TOKEN` | 선택 Qinglong 알림 주소와 구버전 패널 토큰 |

계정은 줄바꿈 또는 `&`로 구분합니다. 계정 메모에는 `|`를 넣지 마세요.

## 성공 기준과 개인정보

작업 API가 성공 표시 또는 보상을 반환하거나 오늘 이미 체크인했다고 명확히 알린 경우 성공입니다. 활동 보상은 포인트 원장으로 별도 확인하며, 보상 처리 실패만으로 체크인 결과를 실패로 바꾸지 않습니다.

`autoclaw_cn_tokens.json`과 `autoclaw_intl_tokens.json`에는 자격 증명이 들어 있으며 Git에서 제외됩니다. Token, 전화번호, `openclaw.json`, 로컬 상태 파일을 Issue나 Pull Request에 공개하지 마세요.

## 사용 범위 및 재배포 안내

이 프로젝트의 공식 버전은 무료입니다. 저장소, 스크립트, 배포 안내와 Release 다운로드를 포함합니다.

저자의 명시적 서면 허가 없이 이 프로젝트를 유료 자료, 내부판, 독점판, 회원 혜택, 유료 강의, 유료 배포 또는 업데이트 서비스로 재포장하지 마세요. 무관한 계정, 그룹, 채널에 옮겨 트래픽이나 유입을 유도하거나, 저자 및 저작권 표시를 삭제하고 원작으로 주장하거나, 저자 이름, 아바타, QR 코드, 프로젝트 이름으로 공식 승인을 가장하는 행위도 금지됩니다.

위반 시 삭제 요청이 이뤄질 수 있으며, 저자는 업데이트를 중단하거나 저장소를 보관 또는 삭제할 수 있습니다. 전체 규칙은 [NOTICE.md](../NOTICE.md)를 확인하세요.

## 링크

- [Releases](https://github.com/L0NE-6/AutoClaw-Daily/releases)
- [Issues](https://github.com/L0NE-6/AutoClaw-Daily/issues)
- [소스와 전체 중국어 문서](../README.md)
