<div align="center">

# 🐾 AutoClaw Daily

**AutoClaw 国内版 / 国际版 每日签到 · 单文件青龙脚本 · 多账号**

<img src="https://img.shields.io/github/v/release/L0NE-6/AutoClaw-Daily?style=flat-square&label=Release&color=2ea44f" />
<img src="https://img.shields.io/github/stars/L0NE-6/AutoClaw-Daily?style=flat-square&label=Stars&color=FFC75F" />
<img src="https://img.shields.io/badge/Python-3.8%2B-3776AB?style=flat-square&logo=python&logoColor=white" />
<img src="https://img.shields.io/badge/%E9%9D%92%E9%BE%99%E9%9D%A2%E6%9D%BF-%E5%8D%95%E6%96%87%E4%BB%B6%E8%BF%90%E8%A1%8C-4EAA25?style=flat-square" />
<img src="https://img.shields.io/badge/GitHub%20Actions-%E6%94%AF%E6%8C%81-2088FF?style=flat-square&logo=githubactions&logoColor=white" />
<img src="https://img.shields.io/badge/%E5%A4%9A%E8%B4%A6%E5%8F%B7-%E6%8D%A2%E8%A1%8C%E6%88%96%20%26%20%E5%88%86%E9%9A%94-8957E5?style=flat-square" />
<img src="https://img.shields.io/badge/License-MIT-F472B6?style=flat-square" />

</div>

---

## ✨ 这是什么

AutoClaw 每日签到：国内版走 `daily_signin` 任务接口并支持 Token 自动续期；国际版从桌面端本机登录态提取 Token，工具会自动校验地区，避免国内/国际混用。

> 🎯 一句话：**配好 Token，剩下的交给它。**
>
> 📦 单文件自包含：不需要额外模块，青龙上传脚本、填好环境变量就能跑。
>
> ☁️ 除了青龙，也可以直接跑在 **GitHub Actions** 上，零服务器定时执行（见下文部署方式二）。

核心特性：

- ✅ **国内版签到**：`daily_signin` 通用任务接口，自动处理「今天已签到」
- 🔐 **Token 自动续期**：失效自动用 refresh_token 换新并保存
- 🌍 **国际版本机提取**：从桌面端登录态读 Token 并校验国际版可用性
- 👥 **多账号** + 📢 **多渠道推送** + 🐧 **青龙 / Actions 双部署**

## 📦 文件说明

| 文件 | 作用 |
|---|---|
| `autoclaw_login.py` | 国内版短信登录 / 国际版本机登录态提取 |
| `autoclaw_cn_daily.py` | 国内版每日签到 |
| `autoclaw_intl_daily.py` | 国际版每日签到 |

## ⬇️ 下载

不想用 git？直接到 **[Releases](https://github.com/L0NE-6/AutoClaw-Daily/releases)** 下载：

- 完整包 zip（脚本 + 登录工具 + README + Actions 工作流 + 收款码）
- 各脚本单文件（青龙只需要上传签到脚本）
- `SHA256SUMS.txt` 完整性校验

## 🚀 部署方式一：青龙面板（三步）

| 步骤 | 操作 |
| :---: | :--- |
| 1 | 安装依赖：`pip install -r requirements.txt`（或 `pip3 install requests`） |
| 2 | 把签到脚本上传到青龙「脚本管理」，或把仓库放进脚本目录 |
| 3 | 「环境变量」里添加 Token，新建定时任务（见下方 cron 示例） |

```cron
35 8 * * * python autoclaw_cn_daily.py
35 8 * * * python autoclaw_intl_daily.py
```

## ☁️ 部署方式二：GitHub Actions（可选，默认手动触发）

1. Fork 本仓库（或直接使用本仓库，Secrets 只能配在你自己的仓库里）。
2. 打开 **Settings → Secrets and variables → Actions**，添加下表里的 Secrets。
3. 打开 **Actions** 标签页，选择 `AutoClaw Daily`，点 **Run workflow** 手动跑一次验证。
4. 默认只支持**手动触发**（上游仓库不跑定时，避免空跑）；fork 后想定时，把 `.github/workflows/daily.yml` 里 `schedule:` 两行取消注释（cron 用 UTC，北京时间减 8 小时），之后就会按该时间自动执行。

| Secret | 对应环境变量 | 必填 |
|---|---|---|
| `AUTOCLAW_CN_TOKENS` | AUTOCLAW_CN_TOKENS | 国内版，可留空 |
| `AUTOCLAW_INTL_TOKENS` | AUTOCLAW_INTL_TOKENS | 国际版，可留空 |
| `PUSHPLUS_TOKEN` / `BARK_URL` / `WECOM_WEBHOOK` / `DINGTALK_WEBHOOK` / `DINGTALK_SECRET` | 同名推送变量 | 可选 |

> 公开仓库的 Secrets 是加密的，日志里不会回显；脚本也不会把 Token 写进仓库文件。

## 🔑 获取 Token

**国内版：手机验证码登录**

```bash
python autoclaw_login.py
```

输入手机号和收到的 6 位验证码，输出一行 `备注|token|refresh_token|device_id`，粘贴进 `AUTOCLAW_CN_TOKENS`。

**国际版：从桌面端登录态提取**（国际版只有 Zai / Google OAuth，脚本不代跑浏览器验证码）

```bash
python autoclaw_login.py --extract-intl
```

先在 AutoClaw 桌面端完成登录，工具会读取本机 `~/.openclaw-autoclaw/openclaw.json`，取出 Token 并校验国际版可用性，输出一行 `备注|token`，粘贴进 `AUTOCLAW_INTL_TOKENS`。

## 🧩 环境变量（支持多账号）

> 多账号用 **换行** 或 **`&`** 分隔，两种可以混用。`|` 是单条账号内部的字段分隔符，备注里不要再写 `|`。

| 环境变量 | 单条格式 | 说明 |
|---|---|---|
| `AUTOCLAW_CN_TOKENS` | `token\|refresh_token\|device_id` / `备注\|…` | 国内版账号 |
| `AUTOCLAW_INTL_TOKENS` | `token` / `备注\|token` | 国际版账号（无 refresh_token） |

## ⌨️ 命令行参数

| 参数 | 作用 |
|---|---|
| `--verify` | 登录后校验一次 |
| `--refresh-only` | 只刷新 Token |
| `--extract-intl` | 从本机登录态提取国际版 Token |
| `--only 2` / `--no-notify` | 单账号 / 关推送 |

## 📊 运行效果示例

```text
[08:35:01] 👤 [1] 主号  token=eyJhbGci****abcd
[08:35:02]    ✅ 签到成功，获得 100 积分
[08:35:03] 账号1 主号: ✅ 签到成功，获得 100 积分
```

## 🗂️ 数据文件说明

| 文件 | 内容 | 是否提交 |
|---|---|---|
| `autoclaw_cn_tokens.json` | 国内版续期后的 Token | 已忽略 |
| `autoclaw_intl_tokens.json` | 国际版续期后的 Token | 已忽略 |

> 以上文件都包含账号凭据，已在 `.gitignore` 中排除，**不要手动提交**。

## ❓ 常见问题

- **国际版为什么要本机提取？** 它的 OAuth 登录强制要求浏览器端验证码，脚本不代跑；桌面端登录后提取最稳。
- **国际版 Token 会过期吗？** 会，且没有 refresh_token；失效后在桌面端重新登录再提取一次。
- **国内/国际 Token 通用吗？** 不通用，提取工具会自动校验地区。

## 📁 目录结构

```text
AutoClaw-Daily/
├── autoclaw_login.py
├── autoclaw_cn_daily.py
├── autoclaw_intl_daily.py
├── assets/
├── .github/workflows/daily.yml
├── CHANGELOG.md
├── LICENSE
├── README.md
└── requirements.txt
```

## 📦 版本与发布

- 每次更新单独发一个 Release：`v1.0.0` → `v1.0.1` …，历史版本保留可下载。
- 每个 Release 附带：完整包 zip + 各脚本单文件 + `SHA256SUMS.txt`。
- 下载页：<https://github.com/L0NE-6/AutoClaw-Daily/releases>

## 🔒 隐私说明

- 脚本**不含任何账号、手机号、Token 或设备信息**，全部由环境变量（或 GitHub Secrets）注入。
- 运行期生成的数据文件（见「数据文件说明」）都包含凭据，已被 `.gitignore` 排除。
- 请勿把 Token 写进脚本、提交到仓库或发到 Issue 里。

## ⚠️ 免责声明

本项目仅供**学习与个人自动化**使用。请遵守对应平台的服务条款，使用风险自负。

## ☕ 支持与投喂

脚本是**完全免费、无广告、无功能限制**的，仓库与发布包也不含你的任何数据。
如果它确实帮你省了时间，欢迎请我喝杯咖啡 —— **纯自愿，不影响任何功能**。

<p align="center">
  <img src="assets/donate-wechat.png" width="240" alt="微信赞赏码" />
  &nbsp;&nbsp;&nbsp;&nbsp;
  <img src="assets/donate-alipay.jpg" width="240" alt="支付宝收款码" />
</p>
<p align="center"><sub>💚 微信支付（左） &nbsp;|&nbsp; 💙 支付宝（右）</sub></p>

> 💡 **不花钱也能帮上忙**：点个 ⭐ Star、提一个带日志的 Issue、发一个 Pull Request，或者把脚本分享给需要的朋友。

## 💬 反馈与贡献

- 提交 [Issue](https://github.com/L0NE-6/AutoClaw-Daily/issues)：报 bug、提需求
- 发起 [Pull Request](https://github.com/L0NE-6/AutoClaw-Daily/pulls)：直接贡献代码

> 提 Issue 时附上**运行日志**和**复现步骤**，定位会快很多。

---

<div align="center">
  <sub>🐾 如果这个脚本帮到你，点个 <b>Star</b> 支持一下，或者到 <a href="#-支持与投喂">支持与投喂</a> 请我喝杯咖啡 ✨</sub>
</div>
