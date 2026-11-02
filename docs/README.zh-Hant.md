# 🐾 AutoClaw Daily

AutoClaw 國內版與國際版每日簽到自動化。專案採用單檔 Python 腳本，支援多帳號，並可自動續期國內版憑證。

[简体中文](../README.md) · [English](README.en.md) · [繁體中文](README.zh-Hant.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Português (BR)](README.pt-BR.md)

完整中文文件請見 [../README.md](../README.md)。

## 核心能力

- 呼叫 `daily_signin` 完成國內版每日簽到，並將「今天已簽到」視為冪等狀態。
- 使用 `refresh_token` 更新國內版存取權杖，並把輪替後憑證寫入本機。
- 從桌面端 `openclaw.json` 提取國際版權杖，並校驗其是否適用國際區。
- 簽到後讀取積分流水，以 `metadata.event_type` 核對當天活動福利。
- 支援換行或 `&` 分隔多帳號，以及 PushPlus、Bark、企業微信、釘釘與青龍通知。

## 青龍最短配置

```bash
python3 -m pip install -r requirements.txt
```

上傳 `autoclaw_cn_daily.py` 或 `autoclaw_intl_daily.py`，設定帳號變數，並使用面板執行器建立任務：

```text
35 8 * * * task autoclaw_cn_daily.py
35 8 * * * task autoclaw_intl_daily.py
```

國內版登入與國際版提取：

```bash
python autoclaw_login.py --verify
python autoclaw_login.py --extract-intl
```

## GitHub Actions

在 **Settings → Secrets and variables → Actions** 建立需要的 Secrets，再從 Actions 頁面手動執行 `AutoClaw Daily`。

```text
AUTOCLAW_CN_TOKENS
AUTOCLAW_INTL_TOKENS
PUSHPLUS_TOKEN          # 選填
BARK_URL                # 選填
WECOM_WEBHOOK           # 選填
DINGTALK_WEBHOOK        # 選填
DINGTALK_SECRET         # 選填
```

工作流預設只允許手動觸發；若要啟用註解中的排程，請編輯 `.github/workflows/daily.yml`，cron 使用 UTC。

## 關鍵環境變數

| 變數 | 用途 |
| :--- | :--- |
| `AUTOCLAW_CN_TOKENS` | 國內版帳號，支援 `token`、`token\|refresh_token\|device_id`、`備註\|token\|refresh_token\|device_id` |
| `AUTOCLAW_INTL_TOKENS` | 國際版帳號；桌面端提取通常只有 `token` |
| `PUSHPLUS_TOKEN`、`BARK_URL`、`WECOM_WEBHOOK`、`DINGTALK_WEBHOOK`、`DINGTALK_SECRET` | 選填推送通道 |
| `QL_URL`、`QL_TOKEN` | 選填青龍通知位址與舊版面板 Token |

多帳號使用換行或 `&` 分隔；備註內不要包含 `|`。

## 成功判據與隱私

簽到介面必須回傳成功標記或獎勵，或明確表示今天已簽到。活動福利另行以積分流水確認；活動觸發失敗不會覆寫主簽到結論。

`autoclaw_cn_tokens.json` 與 `autoclaw_intl_tokens.json` 含憑證且已被 Git 忽略。請勿在 Issue 或 Pull Request 公開 Token、手機號、`openclaw.json` 或本機狀態檔。

## 使用邊界與轉載聲明

本專案的官方版本免費，包括倉庫、腳本、部署說明與 Release 下載。

未經作者明確書面許可，不得將本專案包裝為付費資源、內部版、獨家版、會員權益、收費課程、付費部署或包更新服務；不得搬運到無關帳號、群組或頻道進行漲粉、截流或引流；不得刪除作者與版權資訊後冒充原創；不得使用作者暱稱、頭像、收款碼或專案名稱製造官方授權背書假象。

違規時，作者可要求下架相關內容，並可暫停更新、封存或刪除倉庫。完整規則見 [NOTICE.md](../NOTICE.md)。

## 專案連結

- [Releases](https://github.com/L0NE-6/AutoClaw-Daily/releases)
- [Issues](https://github.com/L0NE-6/AutoClaw-Daily/issues)
- [原始碼與完整中文文件](../README.md)
