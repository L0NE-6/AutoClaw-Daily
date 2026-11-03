<div align="center">

<sub><strong>L0NE-6 · DAILY SIGNAL</strong></sub>

# 🐾 AutoClaw Daily

**AutoClaw 国内版与国际版每日签到，单文件脚本、多账号与 Token 自动续期。**

[简体中文](README.md) · [English](docs/README.en.md) · [繁體中文](docs/README.zh-Hant.md) · [日本語](docs/README.ja.md) · [한국어](docs/README.ko.md) · [Português (BR)](docs/README.pt-BR.md)

<p>
  <img src="https://img.shields.io/github/v/release/L0NE-6/AutoClaw-Daily?style=for-the-badge&label=Release&color=2ea44f&logo=github" alt="Release" />
  <img src="https://img.shields.io/github/stars/L0NE-6/AutoClaw-Daily?style=for-the-badge&label=Stars&color=FFC75F&logo=github" alt="Stars" />
  <img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.8+" />
  <img src="https://img.shields.io/badge/%E9%9D%92%E9%BE%99-%E5%8D%95%E6%96%87%E4%BB%B6-4EAA25?style=for-the-badge" alt="Qinglong" />
  <img src="https://img.shields.io/badge/GitHub%20Actions-Supported-2088FF?style=for-the-badge&logo=githubactions&logoColor=white" alt="GitHub Actions" />
  <img src="https://img.shields.io/badge/License-MIT-F472B6?style=for-the-badge" alt="MIT License" />
  <a href="https://github.com/L0NE-6/AutoClaw-Daily/releases"><img src="https://img.shields.io/badge/%E2%AC%87%20Download-Releases-2ea44f?style=for-the-badge&logo=github" alt="Download Releases" /></a>
</p>

[✨ 30 秒速览](#quick-overview) · [🚀 青龙部署](#quick-boot) · [☁️ Actions](#actions) · [🔐 获取 Token](#credentials) · [🔧 环境变量](#environment) · [✅ 成功判据](#result) · [❓ FAQ](#faq) · [🚫 使用边界](#usage-policy) · [✦ 星轨](#star-trail)

</div>

---

<a id="quick-overview"></a>

<a id="usage-policy"></a>
## 🚫 使用边界与转载声明

> [!IMPORTANT]
> **官方版本永久免费。** 未经作者书面许可，禁止付费包装、搬运引流、冒充作者，或使用作者身份与二维码制造官方授权假象。违规内容可能被要求下架；作者可暂停更新、归档或删除仓库及相关 Release。

本项目仓库、脚本、部署说明和 Release 下载始终免费公开。未经作者明确书面许可，禁止将本项目包装为付费资源、内部版、独家版、会员权益、收费课程、付费部署或包更新服务；禁止搬运到其他账号、群组、频道、网盘、电商或付费平台进行涨粉、截流、倒卖和引流；禁止删除作者与版权信息后冒充原创；禁止使用作者昵称、头像、二维码和项目名称制造官方授权假象。

> 如需商业合作、品牌授权、联合分发或使用作者名义提供付费服务，请先取得作者明确书面授权。完整规则、收款码防诈骗说明和违规处理方式见 **[NOTICE.md](NOTICE.md)**。

> 官方仓库和 Release 始终免费。第三方以“下载费 / 激活费 / 内部版 / 代部署 / 会员门槛”等名义收费，均与作者无关，请停止付款并保留证据。

> 对上述违规行为，作者有权要求立即停止传播、删除内容并下架相关商品或页面；并可视情况暂停更新、归档或删除本仓库及相关 Release、向平台投诉或采取进一步必要措施。

<a id="support"></a>

---

## ✨ 30 秒速览

| 维度 | 说明 |
| :--- | :--- |
| **用途** | 完成 AutoClaw 国内版、国际版每日签到，并读取当天活动积分流水。 |
| **输入** | 国内版 `AUTOCLAW_CN_TOKENS`；国际版 `AUTOCLAW_INTL_TOKENS`；推送变量可选。 |
| **输出** | 分账号签到报告、积分奖励、当天活动福利流水与合计，并推送到已配置渠道。 |
| **部署** | 青龙面板、GitHub Actions，或本地 Python 运行。 |
| **依赖** | Python 3.8+，仅需 `requests`。 |
| **成功判据** | 以任务接口成功标记和奖励回执为准；“今天已签到”按幂等状态处理；活动福利以积分流水回读确认。 |

<a id="signals"></a>

## 🎯 核心能力

- ✅ **国内版签到**：调用 `daily_signin` 通用任务接口，正确处理“今天已签到”。
- 🔁 **国内版自动续期**：使用 `refresh_token` 换取新 Token，并写入本地令牌库。
- 🌍 **国内 / 国际隔离**：登录工具会校验 Token 所属地区，避免两边凭据混用。
- 🧾 **活动福利复核**：签到后读取当天积分流水；未到账时按客户端启动口径触发一次并再次回读。
- 👥 **多账号与推送**：换行或 `&` 分隔账号；支持 PushPlus、Bark、企业微信、钉钉与青龙通知。
- ☁️ **青龙 / Actions**：一个签到脚本即可上传青龙；仓库同时提供手动触发的 Actions 工作流。

## 🧩 工作方式

AutoClaw 的每日签到实际调用通用任务接口：

```text
POST /autoclaw-proxy/proxy/autoclaw-task-complete
{"task_id": "daily_signin"}
```

国内版可使用短信登录取得 `token`、`refresh_token` 与 `device_id`。国际版通过桌面端 `openclaw.json` 中的 `X-Authorization` 提取 Token；该提取来源通常只有短期 Token，失效后需重新登录桌面端并再次提取。

Weekly Perks 一类“活跃即发”活动没有独立领取接口。脚本会先查当天积分流水；未发现活动入账时，再调用客户端启动同款 `POST /userapi/v1/user-info` 触发，并以 `metadata.event_type` 为主复核。活动触发失败只作为附加说明，不会把主签到结论改写成失败。

## 📦 文件说明

| 文件 | 用途 |
| :--- | :--- |
| `autoclaw_login.py` | 国内版短信登录；国际版本机 Token 提取 |
| `autoclaw_cn_daily.py` | 国内版每日签到与活动福利复核 |
| `autoclaw_intl_daily.py` | 国际版每日签到与活动福利复核 |
| `requirements.txt` | Python 依赖清单 |

<a id="quick-boot"></a>

## 🚀 青龙部署

1. 在青龙安装依赖：`python3 -m pip install -r requirements.txt`。
2. 将需要的签到脚本上传到青龙「脚本管理」。
3. 在「环境变量」添加对应的 Token 变量。
4. 新建定时任务，用青龙运行器执行脚本，确保面板变量被注入。

```text
# 每天北京时间 08:35，可分别启用
35 8 * * * task autoclaw_cn_daily.py
35 8 * * * task autoclaw_intl_daily.py
```

<a id="actions"></a>

## ☁️ GitHub Actions

1. Fork 或导入仓库到自己的账号。
2. 在 **Settings → Secrets and variables → Actions** 新建所需 Secrets。
3. 打开 **Actions → AutoClaw Daily → Run workflow** 手动验证。
4. 工作流默认仅手动触发；需要定时时，在 `.github/workflows/daily.yml` 取消 `schedule:` 两行注释。cron 使用 UTC，北京时间需减 8 小时。

| Secret | 必填 | 说明 |
| :--- | :---: | :--- |
| `AUTOCLAW_CN_TOKENS` | 可选 | 国内版账号；只跑国际版时可留空 |
| `AUTOCLAW_INTL_TOKENS` | 可选 | 国际版账号；只跑国内版时可留空 |
| `PUSHPLUS_TOKEN` / `BARK_URL` | 可选 | PushPlus / Bark 推送 |
| `WECOM_WEBHOOK` / `DINGTALK_WEBHOOK` / `DINGTALK_SECRET` | 可选 | 企业微信 / 钉钉推送 |

> 工作流以 Python 3.11 安装 `requirements.txt`，国内版与国际版步骤依次执行；未配置对应账号时，该脚本会提示变量缺失。

<a id="credentials"></a>

## 🔐 获取 Token

**国内版：短信验证码登录**

```bash
python autoclaw_login.py
python autoclaw_login.py --verify
python autoclaw_login.py 13800000000 123456 --note 主号
```

工具输出一行 `备注|token|refresh_token|device_id`，粘贴到 `AUTOCLAW_CN_TOKENS`。

**国际版：桌面端登录态提取**

```bash
python autoclaw_login.py --extract-intl
python autoclaw_login.py --extract-intl --path /path/to/openclaw.json --note 国际主号
```

先在 AutoClaw 桌面端完成登录。工具读取本机 `~/.openclaw-autoclaw/openclaw.json` 并校验国际版可用性，输出 `备注|token`。

<a id="environment"></a>

## 🔧 环境变量与参数

多账号用换行或 `&` 分隔。单条账号内部使用 `|` 分隔字段，备注中不要包含 `|`。

| 环境变量 | 支持的格式 | 说明 |
| :--- | :--- | :--- |
| `AUTOCLAW_CN_TOKENS` | `token` / `token\|refresh_token\|device_id` / `备注\|token\|refresh_token\|device_id` | 国内版账号 |
| `AUTOCLAW_INTL_TOKENS` | `token` / `token\|refresh_token\|device_id` / `备注\|token\|refresh_token\|device_id` | 国际版账号；桌面提取通常只得到 `token` |
| `PUSHPLUS_TOKEN` | Token | PushPlus |
| `BARK_URL` | 完整 Bark 地址 | Bark |
| `WECOM_WEBHOOK` | Webhook 或 key | 企业微信 |
| `DINGTALK_WEBHOOK` / `DINGTALK_SECRET` | Webhook / 加签密钥 | 钉钉 |
| `QL_URL` / `QL_TOKEN` | 面板地址 / 旧版面板 Token | 青龙通知，可选 |

| 命令 | 作用 |
| :--- | :--- |
| `python autoclaw_cn_daily.py --refresh-only` | 只续期并保存 Token |
| `python autoclaw_intl_daily.py --refresh-only` | 只续期并保存 Token |
| `python autoclaw_cn_daily.py --only 2` | 只跑第 2 个账号 |
| `python autoclaw_*_daily.py --no-notify` | 关闭本轮推送 |
| `python autoclaw_login.py --verify` | 国内版登录后校验 |

<a id="result"></a>

## ✅ 成功判据与输出

- 签到接口需要返回成功标记或明确奖励，或明确报告“今天已签到”。
- 当天活动福利以积分流水的 `autoclaw_user_active` / `autoclaw_user_signup_day` 前缀为主动判据，并展示多笔入账合计。
- 活动福利触发或流水读取失败只作为附加说明，不反转已经确认的签到结果。
- 报告按账号输出，失败会保留上游状态、业务码或异常原因，便于定位。

```text
[08:35:01] 👤 [1] 主号  token=eyJhbGci****abcd
[08:35:02]    ✅ 签到成功，获得 100 积分
[08:35:02]    🎁 今日活动福利：20000 + 500，合计 20500
[08:35:03] 账号1 主号: ✅ 签到成功，获得 100 积分
```

<a id="data-privacy"></a>

## 🗂️ 数据文件与隐私

| 文件 | 内容 | 是否提交 |
| :--- | :--- | :---: |
| `autoclaw_cn_tokens.json` | 国内版续期后的凭据 | 否，已忽略 |
| `autoclaw_intl_tokens.json` | 国际版续期后的凭据 | 否，已忽略 |

- 仓库不内置账号、手机号、Token 或设备信息。
- 登录态由环境变量或 GitHub Secrets 注入。
- 请勿将 Token、`openclaw.json` 内容或运行数据文件提交到仓库、Issue 或 Pull Request。

<a id="faq"></a>

## ❓ 常见问题

**国际版为什么需要桌面端提取？**
国际版使用 Zai / Google OAuth，登录工具不代替浏览器完成验证码流程；从桌面端登录态提取更直接。

**国际版 Token 会过期吗？**
会。桌面提取通常没有 `refresh_token`，失效后重新登录桌面端并再次提取。

**国内版与国际版 Token 可以共用吗？**
不可共用。登录工具会按地区校验，脚本也使用不同的账号变量。

**活动福利没到账，签到算失败吗？**
不算。脚本会读取流水并尝试客户端启动同款触发，最终把签到与活动福利分别报告。

<a id="release"></a>

## 📦 版本与发布
- 当前发布版：`v1.0.5`（2026-11-04，文档发行版；脚本逻辑仍为 `v1.0.4`）。

每次更新单独发布 Release，附完整包、签到脚本单文件与 `SHA256SUMS.txt`。下载页：[Releases](https://github.com/L0NE-6/AutoClaw-Daily/releases)。

## ⚠️ 说明

本项目用于学习与个人自动化。请遵守对应平台的服务条款，并自行承担运行风险。

## ☕ 支持与反馈

脚本完全免费，支持不影响任何功能。

- [提交 Issue](https://github.com/L0NE-6/AutoClaw-Daily/issues)：请附运行日志、复现步骤与脱敏后的报错。
- [发起 Pull Request](https://github.com/L0NE-6/AutoClaw-Daily/pulls)：直接贡献修复或文档改进。
- [点一个 Star](https://github.com/L0NE-6/AutoClaw-Daily)：让项目被更多需要的人看见。

<p align="center">
  <img src="assets/donate-wechat.png" width="240" alt="微信赞赏码" />
  &nbsp;&nbsp;&nbsp;&nbsp;
  <img src="assets/donate-alipay.jpg" width="240" alt="支付宝收款码" />
</p>
<p align="center"><sub>微信支付（左） · 支付宝（右）</sub></p>

> ⚠️ 收款码仅用于向作者自愿赞赏。任何第三方以代下载、代部署、内部资源或会员群为由收费，均与作者无关，请停止付款并保留证据。

<a id="star-trail"></a>

## ✦ 星轨 Star Trail

> 每一条签到记录都是一个信号；每一次 Star，都是这条星轨继续向前的亮度。

<a href="https://star-history.com/#L0NE-6/AutoClaw-Daily&Date">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=L0NE-6/AutoClaw-Daily&type=Date&theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=L0NE-6/AutoClaw-Daily&type=Date&theme=light" />
    <img alt="AutoClaw Daily Star Trail" src="https://api.star-history.com/svg?repos=L0NE-6/AutoClaw-Daily&type=Date&theme=light" />
  </picture>
</a>

---

<div align="center">
  <sub>L0NE-6 · DAILY SIGNAL</sub>
  <br />
  <a href="https://github.com/L0NE-6/AutoClaw-Daily/releases">Releases</a>
  ·
  <a href="https://github.com/L0NE-6/AutoClaw-Daily/issues">Issues</a>
  ·
  <a href="https://github.com/L0NE-6/AutoClaw-Daily">Star</a>
</div>
