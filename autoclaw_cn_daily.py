#!/usr/bin/env python3
"""
🐾 AutoClaw 国内版 每日签到 - 青龙脚本
------------------------------------------------------------

📌 功能
   AutoClaw 桌面端「每日签到」Banner 走的是通用任务接口：
   · POST {userapi}/autoclaw-proxy/proxy/autoclaw-task-complete  {"task_id":"daily_signin"}
   · GET  {userapi}/autoclaw-proxy/proxy/autoclaw-task-list       失败归因（只读）
   token 过期（code 400000 / 410000）时自动用 refresh_token 续期。

🔑 环境变量
   AUTOCLAW_CN_TOKENS  【必填】多账号用换行或 & 分隔：
       token
       token|refresh_token
       token|refresh_token|device_id
       备注|token|refresh_token|device_id
     token 为国内版 userapi 的登录态（JWT，带不带 Bearer 都行）

   推送通道（均可选）：PUSHPLUS_TOKEN / BARK_URL / WECOM_WEBHOOK / DINGTALK_WEBHOOK / DINGTALK_SECRET

⌨️ 命令
   python autoclaw_cn_daily.py               正常签到
   python autoclaw_cn_daily.py --refresh-only 只续期并保存
   python autoclaw_cn_daily.py --only 2      只跑第 2 个账号
   python autoclaw_cn_daily.py --no-notify   不推送

📄 依赖：requests
"""
import base64
import hashlib
import hmac
import json
import os
import platform as host_platform
import sys
import time
import uuid

import requests

import urllib3
urllib3.disable_warnings()

try:
    sys.stdout.reconfigure(errors="replace")
except Exception:
    pass

USERAPI = "https://autoglm-acceleration-api.zhipuai.cn"
TASK_COMPLETE_PATH = "/autoclaw-proxy/proxy/autoclaw-task-complete"
TASK_LIST_PATH = "/autoclaw-proxy/proxy/autoclaw-task-list"
REFRESH_PATH = "/userapi/v1/refresh"
REFRESH_FALLBACK_PATH = "/userapi/v1/agent-refresh"
TASK_ID = "daily_signin"

APP_ID = "100003"
APP_KEY = "38d2391985e2369a5fb8227d8e6cd5e5"
CLIENT_VERSION = "1.18.5"
AUTH_EXPIRED_CODES = (410000, 400000)
STORE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "autoclaw_cn_tokens.json")

ONLY = None
REFRESH_ONLY = False
NO_NOTIFY = False


def log(msg):
    print("%s %s" % (time.strftime("[%H:%M:%S]"), msg), flush=True)


def mask(text, keep=6):
    text = str(text or "")
    if len(text) <= keep + 4:
        return text
    return text[:keep] + "****" + text[-4:]


def split_accounts(raw):
    out = []
    for chunk in (raw or "").replace("&", "\n").splitlines():
        chunk = chunk.strip().strip('"\'')
        if chunk and not chunk.startswith("#"):
            out.append(chunk)
    return out


def strip_bearer(token):
    token = (token or "").strip()
    if token.lower().startswith("bearer "):
        return token[7:].strip()
    return token


def first_text(*values):
    for value in values:
        if isinstance(value, str) and value.strip():
            return value.strip()
        if isinstance(value, (int, float)):
            return str(value)
    return ""


def request(method, url, headers=None, body=None, timeout=20, retries=3):
    last = None
    for attempt in range(retries):
        try:
            session = requests.Session()
            session.trust_env = False
            return session.request(method, url, headers=headers or {},
                                   json=body if body is not None else None,
                                   timeout=timeout, verify=False)
        except Exception as error:
            last = error
            if attempt + 1 < retries:
                time.sleep(1.5 * (attempt + 1))
    raise RuntimeError("请求失败: %s" % last)


def json_of(response):
    try:
        return response.json()
    except Exception:
        return {}


def signed_headers(token):
    timestamp = str(int(time.time()))
    sign = hashlib.md5(("%s&%s&%s" % (APP_ID, timestamp, APP_KEY)).encode("utf-8")).hexdigest()
    headers = {
        "Content-Type": "application/json",
        "Accept": "*/*",
        "X-Version": CLIENT_VERSION,
        "X-Product": "autoclaw",
        "X-Client-Type": "pc",
        "X-Harness-Type": "zcode",
        # 平台标识只认官方桌面端的 win / mac；Linux（容器）回落 win，发 linux 会被部分账号 403
        "X-Tm": "mac" if host_platform.system().lower() == "darwin" else "win",
        "X-Lang": "zh-CN",
        "X-Channel": "official",
        "X-Auth-Appid": APP_ID,
        "X-Auth-TimeStamp": timestamp,
        "X-Auth-Sign": sign,
        "X-Trace-Id": uuid.uuid4().hex,
    }
    if token:
        headers["authorization"] = "Bearer %s" % token
    return headers


# ---------- token 存储与续期 ----------

def token_fp(token):
    return hashlib.sha256(token.encode("utf-8")).hexdigest()[:16]


def load_store():
    try:
        with open(STORE_FILE, encoding="utf-8") as handle:
            data = json.load(handle)
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def save_store(store):
    try:
        with open(STORE_FILE, "w", encoding="utf-8") as handle:
            json.dump(store, handle, ensure_ascii=False, indent=2)
    except Exception as error:
        log("⚠️ token 存储写入失败: %s" % error)


def apply_store(account):
    store = load_store()
    keys = [token_fp(account["refresh"])] if account.get("refresh") else []
    keys.append(token_fp(account["access"]))
    for key in keys:
        saved = store.get(key)
        if isinstance(saved, dict) and saved.get("access"):
            account["access"] = saved["access"]
            account["refresh"] = saved.get("refresh") or account.get("refresh", "")
            account["device_id"] = saved.get("device_id") or account.get("device_id", "")
            return True
    return False


def persist(account):
    store = load_store()
    store[token_fp(account.get("refresh") or account["access"])] = {
        "access": account["access"],
        "refresh": account.get("refresh", ""),
        "device_id": account.get("device_id", ""),
        "note": account.get("note", ""),
        "at": int(time.time()),
    }
    save_store(store)


def refresh_account(account):
    refresh = account.get("refresh", "")
    if not refresh:
        raise RuntimeError("账号没有 refresh_token，无法续期")
    for path in (REFRESH_PATH, REFRESH_FALLBACK_PATH):
        body = {"refresh_token": refresh, "source_id": "autoclaw"}
        if account.get("device_id"):
            body["device_id"] = account["device_id"]
        response = request("POST", USERAPI + path, headers=signed_headers(account["access"]), body=body)
        payload = json_of(response)
        code = payload.get("code")
        if code == 400002 and path == REFRESH_PATH:
            continue                     # 签名校验失败 → 降级 agent-refresh
        data = payload.get("data") if isinstance(payload.get("data"), dict) else {}
        access = strip_bearer(first_text(data.get("access_token"), data.get("accessToken"),
                                         data.get("token")))
        if response.status_code == 200 and code == 0 and access:
            account["access"] = access
            new_refresh = strip_bearer(first_text(data.get("refresh_token"), data.get("refreshToken")))
            if new_refresh:
                account["refresh"] = new_refresh
            persist(account)
            log("   🔄 token 已续期并保存")
            return True
        message = first_text(payload.get("msg"), payload.get("message")) or ("HTTP %s" % response.status_code)
        raise RuntimeError("续期失败 code=%s msg=%s" % (code, message))
    raise RuntimeError("续期失败：refresh 与 agent-refresh 均未通过")


# ---------- 上游协议 ----------

def call_task_complete(account):
    return request("POST", USERAPI + TASK_COMPLETE_PATH,
                   headers=signed_headers(account["access"]),
                   body={"task_id": TASK_ID})


def task_list_hint(account):
    try:
        response = request("GET", USERAPI + TASK_LIST_PATH, headers=signed_headers(account["access"]))
        payload = json_of(response)
        if payload.get("code") not in (0, None):
            return ""
        rows = payload.get("data")
        if not isinstance(rows, list):
            return ""
        for row in rows:
            if isinstance(row, dict) and row.get("task_id") == TASK_ID and row.get("completed") is True:
                return "任务清单显示今日已完成"
    except Exception:
        pass
    return ""


def do_checkin(account):
    response = call_task_complete(account)
    payload = json_of(response)
    code = payload.get("code")

    if code in AUTH_EXPIRED_CODES or response.status_code == 401:
        if account.get("refresh"):
            refresh_account(account)
            response = call_task_complete(account)
            payload = json_of(response)
            code = payload.get("code")
        if code in AUTH_EXPIRED_CODES or response.status_code == 401:
            return False, "登录态已过期，请重新登录该账号"

    if response.status_code != 200:
        return False, "签到接口返回 HTTP %s" % response.status_code
    if code not in (0, None):
        message = first_text(payload.get("msg"), payload.get("message")) or "签到失败"
        return False, "签到失败 code=%s %s" % (code, message)

    data = payload.get("data") if isinstance(payload.get("data"), dict) else {}
    already = data.get("already_completed") is True
    reported = data.get("success") is True
    reward = data.get("reward_points") or 0
    try:
        reward = int(reward)
    except Exception:
        reward = 0

    if reward > 0 or (reported and not already):
        return True, "签到成功，获得 %d 积分" % reward
    if already:
        return False, "今天已签到"
    hint = task_list_hint(account)
    return False, "签到未领取（%s）" % (hint or "上游未返回成功标记")


# ---------- 推送 ----------

def post_json(url, payload, timeout=20):
    session = requests.Session()
    session.trust_env = False
    return session.post(url, json=payload, timeout=timeout, verify=False)


def _env(name):
    return os.environ.get(name, "").strip()


def notify_pushplus(title, content):
    token = _env("PUSHPLUS_TOKEN")
    if not token:
        return False
    try:
        text = (content[:18000] + "\n...(已截断)") if len(content) > 18000 else content
        answer = post_json("https://www.pushplus.plus/send",
                           {"token": token, "title": title, "content": text, "template": "txt"})
        return str(json_of(answer).get("code")) == "200"
    except Exception:
        return False


def notify_bark(title, content):
    endpoint = _env("BARK_URL").rstrip("/")
    if not endpoint:
        return False
    try:
        answer = post_json(endpoint, {"title": title, "body": content, "group": "AutoClaw"})
        return json_of(answer).get("code") == 200
    except Exception:
        return False


def notify_wecom(title, content):
    hook = _env("WECOM_WEBHOOK")
    if not hook:
        return False
    if not hook.startswith("http"):
        hook = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=" + hook
    try:
        answer = post_json(hook, {"msgtype": "text",
                                  "text": {"content": ("%s\n%s" % (title, content))[:2000]}})
        return json_of(answer).get("errcode") == 0
    except Exception:
        return False


def notify_dingtalk(title, content):
    hook = _env("DINGTALK_WEBHOOK")
    if not hook:
        return False
    try:
        secret = _env("DINGTALK_SECRET")
        if secret:
            stamp = str(int(time.time() * 1000))
            digest = hmac.new(secret.encode(), ("%s\n%s" % (stamp, secret)).encode(),
                              hashlib.sha256).digest()
            hook += ("&" if "?" in hook else "?") + "timestamp=%s&sign=%s" % (
                stamp, requests.utils.quote(base64.b64encode(digest)))
        answer = post_json(hook, {"msgtype": "text",
                                  "text": {"content": "%s\n%s" % (title, content)}})
        return json_of(answer).get("errcode") == 0
    except Exception:
        return False


def notify_ql(title, content):
    try:
        from notify import send as panel_send
        panel_send(title, content)
        return True
    except Exception:
        pass
    endpoint = _env("QL_URL").rstrip("/")
    token = _env("QL_TOKEN")
    if not endpoint or not token:
        return False
    try:
        session = requests.Session()
        session.trust_env = False
        answer = session.post(endpoint + "/api/system/notify?token=" + token,
                              json={"title": title, "content": content}, timeout=15, verify=False)
        return str(json_of(answer).get("code")) in ("0", "200")
    except Exception:
        return False


def notify_all(title, content):
    handlers = (notify_pushplus, notify_bark, notify_wecom, notify_dingtalk, notify_ql)
    if not any(handler(title, content) for handler in handlers):
        log("（未配置推送渠道，本次只记录日志）")


# ---------- 账号解析与主流程 ----------

def looks_like_token(value):
    value = (value or "").strip()
    return (value.startswith(("eyJ", "Bearer "))
            or value.count(".") >= 2 or len(value) > 80)


def parse_accounts(raw):
    accounts = []
    for index, line in enumerate(split_accounts(raw), 1):
        parts = [part.strip() for part in line.split("|")]
        note = "账号%d" % index
        token = refresh = device = ""
        if len(parts) >= 4:
            note, token, refresh, device = parts[0], parts[1], parts[2], parts[3]
        elif len(parts) == 3:
            first, second, third = parts
            if looks_like_token(first):
                token, refresh, device = first, second, third
            else:
                note, token, refresh = first, second, third
        elif len(parts) == 2:
            first, second = parts
            if looks_like_token(first) and looks_like_token(second):
                token, refresh = first, second
            elif looks_like_token(second):
                note, token = first, second
            else:
                token, refresh = first, second
        else:
            token = parts[0]
        token = strip_bearer(token)
        if token:
            accounts.append({"note": note, "access": token, "refresh": strip_bearer(refresh),
                             "device_id": device})
    return accounts


def main():
    global ONLY, REFRESH_ONLY, NO_NOTIFY
    args = sys.argv[1:]
    if "--refresh-only" in args:
        REFRESH_ONLY = True
    if "--no-notify" in args:
        NO_NOTIFY = True
    if "--only" in args:
        try:
            ONLY = int(args[args.index("--only") + 1])
        except Exception:
            ONLY = None

    accounts = parse_accounts(os.environ.get("AUTOCLAW_CN_TOKENS", ""))
    if not accounts:
        log("❌ 未配置 AUTOCLAW_CN_TOKENS（多条用换行或 & 分隔；每条: token 或 token|refresh_token|device_id）")
        return

    log("╔════════════════════════════════════╗")
    log("║ 🐾 AutoClaw 国内版 每日签到        ║")
    log("╚════════════════════════════════════╝")
    log("👥 账号数: %d  userapi: %s" % (len(accounts), USERAPI))

    report = []
    for index, account in enumerate(accounts, 1):
        if ONLY and index != ONLY:
            continue
        apply_store(account)
        log("👤 [%d] %s  token=%s" % (index, account["note"], mask(account["access"])))
        if REFRESH_ONLY:
            try:
                refresh_account(account)
                report.append("账号%d %s: ✅ token 续期成功" % (index, account["note"]))
            except Exception as error:
                report.append("账号%d %s: ❌ token 续期失败: %s" % (index, account["note"], error))
            continue
        try:
            success, message = do_checkin(account)
            log("   %s %s" % ("✅" if success else "ℹ️", message))
            report.append("账号%d %s: %s %s" % (index, account["note"], "✅" if success else "ℹ️", message))
        except Exception as error:
            log("   ❌ 异常: %s" % error)
            report.append("账号%d %s: ❌ %s" % (index, account["note"], error))
        time.sleep(1.5)

    summary = "🐾 AutoClaw 国内版签到报告\n" + "\n".join(report) + "\n🕐 " + time.strftime("%Y-%m-%d %H:%M")
    log(summary)
    if not NO_NOTIFY and not REFRESH_ONLY:
        notify_all("🐾 AutoClaw 国内版签到报告", summary)


if __name__ == "__main__":
    main()
