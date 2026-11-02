# 🐾 AutoClaw Daily

Automação de check-in diário para as versões chinesa e internacional do AutoClaw. O projeto usa scripts Python de arquivo único, aceita várias contas e renova credenciais da versão chinesa automaticamente.

[简体中文](../README.md) · [English](README.en.md) · [繁體中文](README.zh-Hant.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Português (BR)](README.pt-BR.md)

A documentação completa em chinês está em [../README.md](../README.md).

## Recursos

- Executa `daily_signin` para o AutoClaw chinês e trata um check-in já concluído como estado idempotente.
- Renova tokens da versão chinesa com `refresh_token` e salva localmente as credenciais rotacionadas.
- Extrai um token internacional do `openclaw.json` do aplicativo desktop e valida seu uso na região internacional.
- Lê o extrato de pontos após o check-in e confirma recompensas de atividade do dia por `metadata.event_type`.
- Suporta várias contas separadas por linha ou `&`, além de notificações opcionais por PushPlus, Bark, WeCom, DingTalk ou Qinglong.

## Início rápido no Qinglong

```bash
python3 -m pip install -r requirements.txt
```

Envie `autoclaw_cn_daily.py` e/ou `autoclaw_intl_daily.py`, cadastre as variáveis no painel e crie tarefas usando o executor do Qinglong:

```text
35 8 * * * task autoclaw_cn_daily.py
35 8 * * * task autoclaw_intl_daily.py
```

Login da versão chinesa e extração do token internacional:

```bash
python autoclaw_login.py --verify
python autoclaw_login.py --extract-intl
```

## GitHub Actions

Crie os Secrets em **Settings → Secrets and variables → Actions** e execute `AutoClaw Daily` manualmente na aba Actions.

```text
AUTOCLAW_CN_TOKENS
AUTOCLAW_INTL_TOKENS
PUSHPLUS_TOKEN          # opcional
BARK_URL                # opcional
WECOM_WEBHOOK           # opcional
DINGTALK_WEBHOOK        # opcional
DINGTALK_SECRET         # opcional
```

O workflow é manual por padrão. Para ativar o agendamento comentado, edite `.github/workflows/daily.yml`; o cron usa UTC.

## Variáveis principais

| Variável | Uso |
| :--- | :--- |
| `AUTOCLAW_CN_TOKENS` | Contas chinesas em `token`, `token\|refresh_token\|device_id` ou `note\|token\|refresh_token\|device_id` |
| `AUTOCLAW_INTL_TOKENS` | Contas internacionais; a extração desktop normalmente fornece apenas `token` |
| `PUSHPLUS_TOKEN`, `BARK_URL`, `WECOM_WEBHOOK`, `DINGTALK_WEBHOOK`, `DINGTALK_SECRET` | Canais de notificação opcionais |
| `QL_URL`, `QL_TOKEN` | Endpoint opcional de notificação e token legado do painel Qinglong |

Separe contas por linha ou `&`. Não use `|` dentro da observação da conta.

## Critério de sucesso e privacidade

O check-in só é confirmado quando a API retorna um marcador de sucesso/recompensa ou informa que o check-in do dia já existe. Recompensas de atividade são verificadas separadamente no extrato de pontos; uma falha no gatilho de atividade não altera o resultado principal.

`autoclaw_cn_tokens.json` e `autoclaw_intl_tokens.json` contêm credenciais e são ignorados pelo Git. Não publique tokens, telefone, `openclaw.json` ou arquivos de estado local em issues ou pull requests.

## Links

- [Releases](https://github.com/L0NE-6/AutoClaw-Daily/releases)
- [Issues](https://github.com/L0NE-6/AutoClaw-Daily/issues)
- [Código e guia completo em chinês](../README.md)
