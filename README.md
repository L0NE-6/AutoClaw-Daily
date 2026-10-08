<div align="center">

# 🐾 AutoClaw Daily

**AutoClaw 国内版 / 国际版 每日签到 · 单文件青龙脚本 · 多账号**

<img src="https://img.shields.io/badge/Python-3.8%2B-3776AB?style=flat-square&logo=python&logoColor=white" />
<img src="https://img.shields.io/badge/%E9%9D%92%E9%BE%99%E9%9D%A2%E6%9D%BF-%E5%8D%95%E6%96%87%E4%BB%B6%E8%BF%90%E8%A1%8C-4EAA25?style=flat-square" />
<img src="https://img.shields.io/badge/%E5%A4%9A%E8%B4%A6%E5%8F%B7-%E6%8D%A2%E8%A1%8C%E6%88%96%20%26%20%E5%88%86%E9%9A%94-2088FF?style=flat-square" />
<img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" />

</div>

---

## ✨ 这是什么

AutoClaw 每日签到：国内版走 `daily_signin` 任务接口并支持 Token 自动续期；国际版从桌面端本机登录态提取 Token。

## 📦 文件说明

| 文件 | 作用 |
|---|---|
| `autoclaw_login.py` | 国内版短信登录 / 国际版本机登录态提取 |
| `autoclaw_cn_daily.py` | 国内版每日签到 |
| `autoclaw_intl_daily.py` | 国际版每日签到 |

## 🔑 先获取 Token

国内版（手机验证码）：

```bash
python autoclaw_login.py
```

国际版（先在桌面端完成登录，再提取本机登录态）：

```bash
python autoclaw_login.py --extract-intl
```

## 🧩 环境变量（支持多账号）

> 多账号用 **换行** 或 **`&`** 分隔，两种可以混用。`|` 是单条账号内部的字段分隔符，备注里不要再写 `|`。

| 环境变量 | 单条格式 |
|---|---|
| `AUTOCLAW_CN_TOKENS` | `token\|refresh_token\|device_id` / `备注\|token\|refresh_token\|device_id` |
| `AUTOCLAW_INTL_TOKENS` | `token` / `备注\|token` |

## 🚀 青龙部署

1. 安装依赖：`pip install -r requirements.txt`
2. 把签到脚本上传到青龙（或把整个仓库放进脚本目录）。
3. 在「环境变量」里添加上面的变量，值按单条格式填写。
4. 新建定时任务，参考：

```cron
35 8 * * * python autoclaw_cn_daily.py
35 8 * * * python autoclaw_intl_daily.py
```

## ⚙️ 常用参数

- `--verify`：登录后校验一次
- `--refresh-only`：只刷新 Token
- `--extract-intl`：从本机登录态提取国际版 Token
- `--only 2` / `--no-notify`：单账号 / 关推送

## 📢 推送（可选）

支持 `PUSHPLUS_TOKEN`、`BARK_URL`、`WECOM_WEBHOOK`、`DINGTALK_WEBHOOK`、`DINGTALK_SECRET`；青龙面板自带通知也会自动尝试。配了哪个用哪个，都没配就只打日志。

## ⚠️ 注意事项

- 国内版续期结果写入 `autoclaw_cn_tokens.json`，不要删。
- 国际版提取的 Token 没有 refresh_token，失效后在桌面端重新登录再提取一次。
- 国内版与国际版 Token 不通用。

## 🔒 安全

- 环境变量和运行期生成的 JSON 缓存都包含账号凭据，不要提交到公开仓库、不要外发。
- 仓库里的 `.gitignore` 已排除缓存文件；如果自己改过目录结构，请确认缓存文件没有被 `git add`。

## 📄 License

MIT © 2026 [L0NE-6](https://github.com/L0NE-6)
