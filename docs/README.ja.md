# 🐾 AutoClaw Daily

AutoClaw 中国版・国際版の毎日チェックインを自動化する単一ファイル Python ツールです。複数アカウントに対応し、中国版の認証情報は自動更新できます。

[简体中文](../README.md) · [English](README.en.md) · [繁體中文](README.zh-Hant.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Português (BR)](README.pt-BR.md)

完全な中国語ドキュメントは [../README.md](../README.md) を参照してください。

## 主な機能

- `daily_signin` を呼び出して中国版のデイリーチェックインを実行します。
- `refresh_token` で中国版アクセストークンを更新し、ローテーション後の認証情報をローカルへ保存します。
- デスクトップ版の `openclaw.json` から国際版トークンを取得し、国際リージョンで利用できるか検証します。
- チェックイン後にポイント履歴を読み、当日のアクティビティ特典を `metadata.event_type` で確認します。
- 改行または `&` 区切りの複数アカウント、PushPlus、Bark、WeCom、DingTalk、Qinglong 通知に対応します。

## Qinglong 最小構成

```bash
python3 -m pip install -r requirements.txt
```

`autoclaw_cn_daily.py` または `autoclaw_intl_daily.py` をアップロードし、アカウント変数を設定して、パネルのランナーでタスクを作成します。

```text
35 8 * * * task autoclaw_cn_daily.py
35 8 * * * task autoclaw_intl_daily.py
```

中国版ログインと国際版トークン抽出:

```bash
python autoclaw_login.py --verify
python autoclaw_login.py --extract-intl
```

## GitHub Actions

**Settings → Secrets and variables → Actions** で必要な Secrets を作成し、Actions 画面から `AutoClaw Daily` を手動実行します。

```text
AUTOCLAW_CN_TOKENS
AUTOCLAW_INTL_TOKENS
PUSHPLUS_TOKEN          # 任意
BARK_URL                # 任意
WECOM_WEBHOOK           # 任意
DINGTALK_WEBHOOK        # 任意
DINGTALK_SECRET         # 任意
```

ワークフローは既定で手動実行のみです。コメント済みのスケジュールを有効にする場合は `.github/workflows/daily.yml` を編集してください。cron は UTC です。

## 主要な環境変数

| 変数 | 用途 |
| :--- | :--- |
| `AUTOCLAW_CN_TOKENS` | 中国版。`token`、`token\|refresh_token\|device_id`、`note\|token\|refresh_token\|device_id` に対応 |
| `AUTOCLAW_INTL_TOKENS` | 国際版。デスクトップ版からの抽出では通常 `token` のみ |
| `PUSHPLUS_TOKEN`、`BARK_URL`、`WECOM_WEBHOOK`、`DINGTALK_WEBHOOK`、`DINGTALK_SECRET` | 任意の通知設定 |
| `QL_URL`、`QL_TOKEN` | 任意の Qinglong 通知先と旧パネルトークン |

複数アカウントは改行または `&` で区切ります。メモ欄に `|` を含めないでください。

## 成功判定とプライバシー

タスク API が成功マーカーまたは報酬を返した場合、または本日のチェックイン済みを明示した場合に成功と判定します。アクティビティ特典はポイント履歴で別途確認し、特典処理の失敗だけでチェックイン結果を失敗へ変更しません。

`autoclaw_cn_tokens.json` と `autoclaw_intl_tokens.json` には認証情報が含まれ、Git の対象外です。Token、電話番号、`openclaw.json`、ローカル状態ファイルを Issue や Pull Request に公開しないでください。

## 利用範囲と再配布について

本プロジェクトの公式版は無料です。リポジトリ、スクリプト、デプロイ手順、Release ダウンロードを含みます。

作者の明示的な書面許可なく、本プロジェクトを有料リソース、内部版、限定版、会員特典、有料講座、有料デプロイ、更新販売として再パッケージしないでください。無関係なアカウント、グループ、チャンネルへ転載して集客や誘導を行うこと、作者・著作権表示を削除して自作と主張すること、作者名・アバター・QR コード・プロジェクト名を使って公式承認を装うことも禁止します。

違反時は削除要請の対象となる場合があります。作者は更新の停止、リポジトリのアーカイブまたは削除を行うことがあります。完全な規則は [NOTICE.md](../NOTICE.md) を参照してください。

## リンク

- [Releases](https://github.com/L0NE-6/AutoClaw-Daily/releases)
- [Issues](https://github.com/L0NE-6/AutoClaw-Daily/issues)
- [ソースと完全な中国語ガイド](../README.md)
