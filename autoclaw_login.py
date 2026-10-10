#!/usr/bin/env python3
"""
🐾 AutoClaw 登录 / Token 获取工具
------------------------------------------------------------
国内版：手机号 + 短信验证码登录，直接拿 token 对
国际版：从桌面端本机登录态文件里提取 token（OAuth 需要浏览器验证码，不走脚本）

用法:
  python autoclaw_login.py                          # 国内版短信登录
  python autoclaw_login.py PHONE              # 指定手机号
  python autoclaw_login.py PHONE CODE       # 指定手机号+验证码
  python autoclaw_login.py --note 主号              # 指定备注名
  python autoclaw_login.py --verify                 # 登录后校验
  python autoclaw_login.py --extract-intl           # 国际版：从本机登录态提取
  python autoclaw_login.py --extract-intl --path /path/to/openclaw.json

输出:
  国内版 → 备注|token|refresh_token|device_id   （追加到 AUTOCLAW_CN_TOKENS）
  国际版 → 备注|token                            （追加到 AUTOCLAW_INTL_TOKENS）

仅依赖 requests。
"""
import hashlib
import json
import os
import re
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

CN_BASE = "https://autoglm-acceleration-api.zhipuai.cn"
INTL_BASE = "https://autoglm-api.autoglm.ai"
SEND_CODE_PATH = "/userapi/v1/agent-send-code"
LOGIN_PATH = "/userapi/v1/agent-login/"
TASK_LIST_PATH = "/autoclaw-proxy/proxy/autoclaw-task-list"
OPENCLAW_FILE = os.path.join(os.path.expanduser("~"), ".openclaw-autoclaw", "openclaw.json")

APP_ID = "100003"
APP_KEY = "38d2391985e2369a5fb8227d8e6cd5e5"
CLIENT_VERSION = "1.18.5"
AUTH_EXPIRED_CODES = (410000, 400000)


def log(msg):
    print("%s %s" % (time.strftime("[%H:%M:%S]"), msg), flush=True)


def mask_phone(phone):
    phone = str(phone or "")
    return phone[:3] + "****" + phone[-4:] if len(phone) >= 7 else phone


def normalize_phone(raw):
    text = re.sub(r"[\s\-]", "", str(raw or "").strip())
    if text.startswith("+86"):
        text = text[3:]
    elif text.startswith("86") and len(text) == 13:
        text = text[2:]
    if not re.fullmatch(r"1[3-9]\d{9}", text):
        raise ValueError("手机号格式不对，需要 11 位中国大陆号码")
    return text


def normalize_code(raw):
    text = str(raw or "").strip()
    if not re.fullmatch(r"\d{6}", text):
        raise ValueError("验证码格式不对，需要 6 位数字")
    return text


def strip_bearer(token):
    token = str(token or "").strip()
    return token[7:].strip() if token.lower().startswith("bearer ") else token


def signed_headers(token=""):
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
        "X-Tm": "mac" if sys.platform == "darwin" else "win",
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


def request(method, url, headers=None, body=None, timeout=20, retries=2):
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


def first_text(*values):
    for value in values:
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def send_code(phone):
    log("📤 发送短信验证码到 %s ..." % mask_phone(phone))
    device_id = os.urandom(32).hex()
    response = request("POST", CN_BASE + SEND_CODE_PATH, headers=signed_headers(),
                       body={"phone": phone, "source_id": "autoclaw", "device_id": device_id})
    payload = json_of(response)
    code = payload.get("code")
    if code != 0:
        raise RuntimeError("发码失败（code=%s）：%s" % (code, first_text(payload.get("msg"), payload.get("message"))))
    delivered = (payload.get("data") or {}).get("result") is True
    if not delivered:
        raise RuntimeError("发码失败：上游返回 result=false")
    log("✅ 验证码已发送")
    return device_id


def login_with_code(phone, code, device_id):
    log("🔐 提交验证码登录 ...")
    response = request("POST", CN_BASE + LOGIN_PATH, headers=signed_headers(),
                       body={"phone": phone, "code": code, "platform": "web",
                             "source_id": "autoclaw", "device_id": device_id})
    payload = json_of(response)
    status = payload.get("code")
    if status != 0:
        raise RuntimeError("登录失败（code=%s）：%s" % (status, first_text(payload.get("msg"), payload.get("message"))))
    data = payload.get("data") or {}
    token = strip_bearer(first_text(data.get("access_token"), data.get("accessToken")))
    if not token:
        raise RuntimeError("登录成功但响应缺少 access_token")
    return {
        "token": token,
        "refresh_token": strip_bearer(first_text(data.get("refresh_token"), data.get("refreshToken"))),
        "device_id": device_id,
    }


def verify(base_url, token):
    log("🔎 校验 token（%s）..." % ("国际版" if base_url == INTL_BASE else "国内版"))
    try:
        response = request("GET", base_url + TASK_LIST_PATH, headers=signed_headers(token))
        payload = json_of(response)
        code = payload.get("code")
        if response.status_code == 200 and code == 0:
            log("✅ token 可用")
            return True
        if code in AUTH_EXPIRED_CODES or response.status_code == 401:
            log("⚠️ token 不被该地区接受（登录态失效或地区不符）")
            return False
        log("⚠️ 校验返回 HTTP %s / code=%s" % (response.status_code, code))
    except Exception as error:
        log("⚠️ 校验异常：%s" % error)
    return False


def extract_openclaw_token(path):
    with open(path, encoding="utf-8") as handle:
        data = json.load(handle)
    providers = ((data.get("models") or {}).get("providers") or {})
    if not isinstance(providers, dict):
        raise RuntimeError("openclaw.json 结构不符：缺少 models.providers")
    for provider in providers.values():
        models = provider.get("models") if isinstance(provider, dict) else None
        if not isinstance(models, list):
            continue
        for model in models:
            headers = model.get("headers") if isinstance(model, dict) else None
            if not isinstance(headers, dict):
                continue
            for name in ("X-Authorization", "x-authorization"):
                token = strip_bearer(headers.get(name))
                if token:
                    return token
    raise RuntimeError("openclaw.json 里没有找到 X-Authorization token（请先在桌面端登录）")


def run_extract(args):
    note = ""
    path = OPENCLAW_FILE
    if "--note" in args:
        try:
            note = args[args.index("--note") + 1]
        except Exception:
            note = ""
    if "--path" in args:
        try:
            path = args[args.index("--path") + 1]
        except Exception:
            path = OPENCLAW_FILE
    print("╔══════════════════════════════════════════╗")
    print("║ 🐾 AutoClaw 国际版 Token 提取             ║")
    print("╚══════════════════════════════════════════╝")
    token = extract_openclaw_token(path)
    log("✅ 已从 %s 提取到 token" % path)
    verify(INTL_BASE, token)
    env_line = "%s|%s" % (note or "AutoClaw国际", token)
    print("\n" + "-" * 50)
    print("✅ 将下面这行追加到 AUTOCLAW_INTL_TOKENS")
    print("-" * 50)
    print(env_line)
    print("-" * 50)
    print("ℹ️ 该来源只有 token、没有 refresh_token，无法自动续期；失效后在桌面端重新登录再提取一次。")
    return 0


def main():
    args = sys.argv[1:]
    if "--extract-intl" in args:
        return run_extract(args)

    do_verify = "--verify" in args
    note = ""
    if "--note" in args:
        try:
            note = args[args.index("--note") + 1]
        except Exception:
            note = ""
    positional = []
    skip_next = False
    for index, item in enumerate(args):
        if skip_next:
            skip_next = False
            continue
        if item == "--note":
            skip_next = True
            continue
        if item.startswith("--"):
            continue
        positional.append(item)

    print("╔══════════════════════════════════════════╗")
    print("║ 🐾 AutoClaw 国内版 短信登录               ║")
    print("╚══════════════════════════════════════════╝")

    phone = normalize_phone(positional[0]) if positional else ""
    code = positional[1] if len(positional) > 1 else ""
    if not phone:
        phone = normalize_phone(input("📱 请输入手机号: ").strip())
    device_id = send_code(phone)
    code = normalize_code(code) if code else normalize_code(input("📩 请输入收到的验证码: ").strip())

    credentials = login_with_code(phone, code, device_id)
    log("✅ 登录成功")
    if do_verify:
        verify(CN_BASE, credentials["token"])

    env_line = "%s|%s|%s|%s" % (note or phone, credentials["token"],
                                credentials["refresh_token"], credentials["device_id"])
    print("\n" + "-" * 50)
    print("✅ 将下面这行追加到 AUTOCLAW_CN_TOKENS")
    print("-" * 50)
    print(env_line)
    print("-" * 50)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n已取消")
        sys.exit(130)
    except Exception as error:
        print("❌ %s" % error)
        sys.exit(1)
