<div align="center">

<sub><strong>L0NE-6 · DAILY SIGNAL</strong></sub>

# 🐾 AutoClaw Daily

**AutoClaw 国内版与国际版每日签到，单文件脚本、多账号、Token 续期、活动流水回读与多渠道通知。**

> 当前版本：**v1.0.6**（2026-11-17） · 核心能力：国内版短信登录、国际版桌面凭据提取、每日签到、活动福利复核

[简体中文](README.md) · [English](docs/README.en.md) · [繁體中文](docs/README.zh-Hant.md) · [日本語](docs/README.ja.md) · [한국어](docs/README.ko.md) · [Português (BR)](docs/README.pt-BR.md)

<p>
  <img src="https://img.shields.io/github/v/release/L0NE-6/AutoClaw-Daily?style=for-the-badge&label=Release&color=2ea44f&logo=github" alt="Release" />
  <img src="https://img.shields.io/github/stars/L0NE-6/AutoClaw-Daily?style=for-the-badge&label=Stars&color=FFC75F&logo=github" alt="Stars" />
  <img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.8+" />
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20Qinglong-4EAA25?style=for-the-badge&logo=linux&logoColor=white" alt="Platform" />
  <img src="https://img.shields.io/github/license/L0NE-6/AutoClaw-Daily?style=for-the-badge&label=License&color=F472B6" alt="License" />
  <a href="https://github.com/L0NE-6/AutoClaw-Daily/releases"><img src="https://img.shields.io/badge/Download-Releases-2ea44f?style=for-the-badge&logo=github" alt="Download" /></a>
</p>

[🚫 使用边界](#usage-policy) · [✨ 30 秒速览](#overview) · [🧭 这是什么](#what-is-this) · [🔁 工作原理](#protocol) · [🔑 凭据](#credentials) · [🚀 本地](#local) · [🐧 青龙](#qinglong) · [☁️ Actions](#actions) · [⌨️ CLI](#cli-output) · [🧾 结果码](#result-codes) · [✅ 成功判据](#success) · [🧪 测试](#tests) · [🧱 设计原则](#design) · [🔒 隐私](#privacy) · [📁 目录](#layout) · [📦 版本](#release) · [⚠️ 免责声明](#disclaimer) · [☕ 赞赏](#donate) · [💬 反馈与 Star](#feedback)

</div>

---

<a id="usage-policy"></a>
## 🚫 使用边界与转载声明

> [!IMPORTANT]
> **官方版本永久免费。** 未经作者书面许可，禁止付费包装、搬运引流、冒充作者，或使用作者身份与二维码制造官方授权假象。

本项目仓库、脚本、部署说明和 Release 下载始终免费公开。未经作者明确书面许可，禁止将其包装为付费资源、内部版、独家版、会员权益、收费课程、付费部署或包更新服务；禁止搬运到其他账号、群组、频道、网盘、电商或付费平台进行涨粉、截流、倒卖和引流。

如需商业合作、品牌授权、联合分发或使用作者名义提供付费服务，请先取得作者明确书面授权。完整规则见 [NOTICE.md](NOTICE.md)。

---

<a id="overview"></a>
## ✨ 30 秒速览

| 维度 | 说明 |
| :--- | :--- |
| **做什么** | 完成 AutoClaw 国内版、国际版每日签到，并复核当天活动积分流水。 |
| **输入** | `AUTOCLAW_CN_TOKENS`、`AUTOCLAW_INTL_TOKENS`，以及可选推送变量。 |
| **输出** | 分账号签到结果、奖励积分、当天活动流水、多笔入账合计和推送摘要。 |
| **部署** | Windows、Linux、青龙面板、GitHub Actions。 |
| **依赖** | Python 3.8+，主流程仅需 `requests`。 |
| **成功判据** | 签到任务返回成功或明确“今日已完成”；活动福利必须由当天积分流水复核。 |

---

<a id="what-is-this"></a>
## 🧭 这是什么

仓库包含三个独立工具：

- `autoclaw_cn_daily.py`：国内版签到、Token 续期、活动福利流水复核。
- `autoclaw_intl_daily.py`：国际版签到、Token 续期、活动福利流水复核。
- `autoclaw_login.py`：国内版短信登录，以及国际版桌面客户端凭据提取与地区校验。

国内版和国际版使用不同 API 基址、账号变量和登录态。脚本不会把一个地区的凭据发送到另一个地区。

---

<a id="protocol"></a>
## 🔁 协议、工作原理与回读

国内版基址为 `https://autoglm-acceleration-api.zhipuai.cn`，国际版基址为 `https://autoglm-api.autoglm.ai`。

```text
POST /autoclaw-proxy/proxy/autoclaw-task-complete
{"task_id": "daily_signin"}

GET  /autoclaw-proxy/proxy/autoclaw-task-list
GET  /agent-assetmgr/api/v1/ledgers_std?asset_type=point&wallet_type=all
POST /userapi/v1/user-info
```

签到接口成功后，脚本读取当天积分流水。活动福利以 `metadata.event_type` 的以下前缀为主要判据：

- `autoclaw_user_active`
- `autoclaw_user_signup_day`

如果流水尚未出现当天活动入账，脚本会使用客户端启动同款 `POST /userapi/v1/user-info` 触发一次并再次读取。多笔活动入账会全部收集并展示合计。活动福利复核失败只作附加说明，不反转已经确认的签到结果。

Token 续期使用：

```text
POST /userapi/v1/refresh
POST /userapi/v1/agent-refresh
```

---

<a id="credentials"></a>
## 🔑 凭据与环境变量

多账号用换行或 `&` 分隔。每条账号内部用 `|` 分隔字段，备注中不要包含 `|`。

| 变量 | 支持的格式 | 说明 |
| :--- | :--- | :--- |
| `AUTOCLAW_CN_TOKENS` | `token` / `token\|refresh_token\|device_id` / `备注\|token\|refresh_token\|device_id` | 国内版账号 |
| `AUTOCLAW_INTL_TOKENS` | `token` / `token\|refresh_token\|device_id` / `备注\|token\|refresh_token\|device_id` | 国际版账号 |
| `PUSHPLUS_TOKEN` | Token | PushPlus |
| `BARK_URL` | 完整地址 | Bark |
| `WECOM_WEBHOOK` | Webhook 或 key | 企业微信 |
| `DINGTALK_WEBHOOK` | Webhook | 钉钉 |
| `DINGTALK_SECRET` | 密钥 | 钉钉加签 |
| `QL_URL` / `QL_TOKEN` | 面板地址 / 旧版 Token | 青龙通知 |

国内版登录：

```bash
python autoclaw_login.py
python autoclaw_login.py --verify
python autoclaw_login.py 13800000000 123456 --note 主号
```

国际版桌面凭据提取：

```bash
python autoclaw_login.py --extract-intl
python autoclaw_login.py --extract-intl --path /path/to/openclaw.json --note 国际主号
```

---

<a id="local"></a>
## 🚀 本地快速开始

```bash
python -m pip install -r requirements.txt
```

配置国内版：

```text
AUTOCLAW_CN_TOKENS=主号|ACCESS_TOKEN|REFRESH_TOKEN|DEVICE_ID
```

配置国际版：

```text
AUTOCLAW_INTL_TOKENS=国际主号|ACCESS_TOKEN
```

先执行一个账号验证：

```bash
python autoclaw_cn_daily.py --only 1
python autoclaw_intl_daily.py --only 1
```

只续期不签到：

```bash
python autoclaw_cn_daily.py --refresh-only
python autoclaw_intl_daily.py --refresh-only
```

---

<a id="qinglong"></a>
## 🐧 青龙面板

```bash
python3 -m pip install -r requirements.txt
```

将需要的脚本上传到青龙「脚本管理」，在环境变量中填写账号，再创建任务：

```text
# 每天北京时间 08:35，可分别启用
35 8 * * * task autoclaw_cn_daily.py
35 8 * * * task autoclaw_intl_daily.py
```

续期后的凭据分别写入 `autoclaw_cn_tokens.json` 和 `autoclaw_intl_tokens.json`。两个文件均已被 `.gitignore` 屏蔽，青龙脚本目录需要可写且可持久化。

---

<a id="actions"></a>
## ☁️ GitHub Actions

工作流位于 [`.github/workflows/daily.yml`](.github/workflows/daily.yml)。当前仅启用 `workflow_dispatch`，定时段保持注释；启用时需把北京时间换算成 UTC。

| Secret | 必填 | 说明 |
| :--- | :---: | :--- |
| `AUTOCLAW_CN_TOKENS` | 可选 | 国内版账号，只跑国际版时可留空 |
| `AUTOCLAW_INTL_TOKENS` | 可选 | 国际版账号，只跑国内版时可留空 |
| `PUSHPLUS_TOKEN` / `BARK_URL` | 可选 | PushPlus / Bark |
| `WECOM_WEBHOOK` | 可选 | 企业微信 |
| `DINGTALK_WEBHOOK` / `DINGTALK_SECRET` | 可选 | 钉钉与加签 |

工作流使用 Python 3.11，国内版和国际版步骤依次执行。未配置对应账号时，该步骤会输出变量缺失提示。

---

<a id="cli-output"></a>
## ⌨️ CLI 与输出

| 命令 | 作用 |
| :--- | :--- |
| `python autoclaw_cn_daily.py` | 国内版完整签到 |
| `python autoclaw_intl_daily.py` | 国际版完整签到 |
| `python autoclaw_*_daily.py --refresh-only` | 只续期并保存 Token |
| `python autoclaw_*_daily.py --only 2` | 只处理第二个账号 |
| `python autoclaw_*_daily.py --no-notify` | 关闭本轮推送 |
| `python autoclaw_login.py --verify` | 国内版登录态校验 |

输出按账号分块，包含脱敏 Token、签到动作、奖励积分、当天活动流水和最终摘要。报告中的活动福利与签到状态分开显示。

---

<a id="result-codes"></a>
## 🧾 结果码

| 结果 | 含义 |
| :--- | :--- |
| 签到成功 | 任务接口返回成功标记，或本次有明确奖励 |
| 今日已完成 | 服务端明确返回幂等状态，按成功处理 |
| 活动已入账 | 当天积分流水命中活动前缀，并显示入账合计 |
| 活动待复核 | 签到完成，但活动流水未出现或触发失败 |
| 登录退出码 `0` | 登录、校验或提取完成 |
| 登录退出码 `130` | 用户中断 |
| 登录退出码 `1` | 参数、网络、凭据或校验失败 |
| 日任务进程退出码 `0` | 进程正常结束；逐账号结论仍以报告为准 |

---

<a id="success"></a>
## ✅ 成功判据

签到成功的必要证据是任务接口返回成功标记、明确奖励，或服务端明确表示今日已完成。

活动福利另有一套判据：当天积分流水中出现 `autoclaw_user_active*` 或 `autoclaw_user_signup_day*` 事件，并读取到奖励数值。活动触发成功但没有流水时，报告为“活动待复核”，不能写成已到账。

HTTP 200 单独出现不等于签到成功，也不等于积分到账。

---

<a id="tests"></a>
## 🧪 测试

```bash
python -m unittest discover -s tests -v
python -m py_compile autoclaw_cn_daily.py autoclaw_intl_daily.py autoclaw_login.py
git diff --check
```

现有 2 项登录契约测试覆盖验证码整数归一化和桌面登录接口，包括 `/userapi/v1/agent-login`、`platform=win` 与 access token 解析。测试使用假 HTTP 响应，不发送真实短信或签到请求。

---

<a id="design"></a>
## 🧱 设计原则

- **地区隔离**：国内版与国际版使用独立基址、变量和凭据文件。
- **动作与流水分离**：签到结果和活动福利分别判定。
- **幂等**：今日已完成按成功状态处理，不重复提交。
- **凭据轮换**：续期后立即保存新 Token，避免丢失。
- **账号隔离**：单账号异常不会中断其他账号。
- **最小依赖**：签到主流程只依赖 `requests`。

---

<a id="privacy"></a>
## 🔒 隐私与数据边界

- 仓库不包含账号、手机号、Token 或设备信息。
- 日志中的 Token 始终脱敏。
- `autoclaw_cn_tokens.json`、`autoclaw_intl_tokens.json` 和桌面 `openclaw.json` 不应提交。
- 请只在本地环境变量、青龙环境变量或 GitHub Secrets 中保存凭据。
- 提交 Issue 前请移除手机号、设备 ID、完整 Token 和 Cookie。

---

<a id="layout"></a>
## 📁 目录结构

```text
AutoClaw-Daily/
├── .github/workflows/daily.yml
├── assets/
├── docs/
├── tests/
├── autoclaw_cn_daily.py
├── autoclaw_intl_daily.py
├── autoclaw_login.py
├── CHANGELOG.md
├── LICENSE
├── NOTICE.md
├── requirements.txt
└── README.md
```

---

<a id="release"></a>
## 📦 版本与发布

- 当前版本：`v1.0.6`，修复国内版短信登录路径、验证码类型和桌面平台参数。
- 历史版本保留在 [Releases](https://github.com/L0NE-6/AutoClaw-Daily/releases)。
- 每次发布包含完整包、脚本单文件与校验文件。
- 变更记录见 [CHANGELOG.md](CHANGELOG.md)。

---

<a id="disclaimer"></a>
## ⚠️ 免责声明

本项目用于个人学习与合法自动化实践。使用者应自行确认账号、服务条款和部署环境；因误配置、凭据泄露、服务策略变化或账号异常产生的风险由使用者自行承担。

---

<a id="donate"></a>
## ☕ 支持与投喂：微信与支付宝赞赏码

脚本完全免费，赞赏纯自愿，不影响任何功能。

<p align="center">
  <img src="assets/donate-wechat.png" width="260" alt="微信赞赏码" />
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <img src="assets/donate-alipay.jpg" width="260" alt="支付宝收款码" />
</p>

<p align="center"><sub>微信支付（左） · 支付宝（右）</sub></p>

> [!WARNING]
> 收款码仅用于向作者自愿赞赏。任何第三方以代下载、代部署、内部资源、会员群或官方授权为由收费，均与作者无关。

---

<a id="feedback"></a>
## 💬 反馈与贡献：Star History

- [Issues](https://github.com/L0NE-6/AutoClaw-Daily/issues)
- [Pull Requests](https://github.com/L0NE-6/AutoClaw-Daily/pulls)
- [Releases](https://github.com/L0NE-6/AutoClaw-Daily/releases)

<a href="https://star-history.com/#L0NE-6/AutoClaw-Daily&Date">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=L0NE-6/AutoClaw-Daily&type=Date&theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=L0NE-6/AutoClaw-Daily&type=Date&theme=light" />
    <img alt="AutoClaw Daily Star History" src="https://api.star-history.com/svg?repos=L0NE-6/AutoClaw-Daily&type=Date&theme=light" />
  </picture>
</a>

<div align="center">

[⭐ Star](https://github.com/L0NE-6/AutoClaw-Daily) · [🍴 Fork](https://github.com/L0NE-6/AutoClaw-Daily/fork) · L0NE-6 · DAILY SIGNAL

</div>
