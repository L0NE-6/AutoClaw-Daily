# 🐾 AutoClaw Daily

Daily check-in automation for the China and international AutoClaw services. The project uses single-file Python scripts, supports multiple accounts, and can refresh China-version credentials automatically.

[简体中文](../README.md) · [English](README.en.md) · [繁體中文](README.zh-Hant.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Português (BR)](README.pt-BR.md)

For the complete Chinese documentation, see [../README.md](../README.md).

## Highlights

- Runs `daily_signin` for AutoClaw China and reports an already-completed check-in as an idempotent state.
- Refreshes China-version access tokens with `refresh_token` and persists the rotated credentials locally.
- Extracts an international token from the desktop client's `openclaw.json` and validates that it works for the international region.
- Reads point ledgers after check-in and verifies same-day activity rewards by `metadata.event_type`.
- Supports multiple accounts with newline or `&` separators and optional PushPlus, Bark, WeCom, DingTalk, or Qinglong notifications.

## Quick Start with Qinglong

```bash
python3 -m pip install -r requirements.txt
```

Upload `autoclaw_cn_daily.py` and/or `autoclaw_intl_daily.py`, add the account variables in Qinglong, then create a task that uses the panel runner:

```text
35 8 * * * task autoclaw_cn_daily.py
35 8 * * * task autoclaw_intl_daily.py
```

China-version login:

```bash
python autoclaw_login.py --verify
```

International token extraction, after signing in to the desktop app:

```bash
python autoclaw_login.py --extract-intl
```

## GitHub Actions

Create repository secrets under **Settings → Secrets and variables → Actions**, then run **AutoClaw Daily** manually from the Actions tab.

```text
AUTOCLAW_CN_TOKENS
AUTOCLAW_INTL_TOKENS
PUSHPLUS_TOKEN          # optional
BARK_URL                # optional
WECOM_WEBHOOK           # optional
DINGTALK_WEBHOOK        # optional
DINGTALK_SECRET         # optional
```

The workflow is manual by default. To enable its commented schedule, edit `.github/workflows/daily.yml`; cron uses UTC.

## Key Environment Variables

| Variable | Meaning |
| :--- | :--- |
| `AUTOCLAW_CN_TOKENS` | China accounts in `token`, `token\|refresh_token\|device_id`, or `note\|token\|refresh_token\|device_id` form |
| `AUTOCLAW_INTL_TOKENS` | International accounts in the same supported field layout; desktop extraction usually provides only `token` |
| `PUSHPLUS_TOKEN`, `BARK_URL`, `WECOM_WEBHOOK`, `DINGTALK_WEBHOOK`, `DINGTALK_SECRET` | Optional notification channels |
| `QL_URL`, `QL_TOKEN` | Optional Qinglong notification endpoint and legacy panel token |

Use newlines or `&` between accounts. Do not put `|` inside an account note.

## Success and Privacy

A check-in succeeds only when the task endpoint returns a success marker/reward or reports that today's check-in already exists. Activity rewards are confirmed separately by reading the point ledger. A failed activity trigger does not rewrite the check-in result.

Generated `autoclaw_cn_tokens.json` and `autoclaw_intl_tokens.json` files contain credentials and are ignored by Git. Never publish tokens, phone numbers, `openclaw.json`, or local state files in an issue or pull request.

## Project Links

- [Releases](https://github.com/L0NE-6/AutoClaw-Daily/releases)
- [Issues](https://github.com/L0NE-6/AutoClaw-Daily/issues)
- [Source and complete Chinese guide](../README.md)
