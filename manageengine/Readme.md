
```
import requests
import urllib3
import base64
import json

SERVER = "https://epc-srv.faradis.net:8383"
USERNAME = "admin"
PASSWORD = "H8;ev1nK_H7xJ1"
VERIFY_SSL = False

if not VERIFY_SSL:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = f"{SERVER.rstrip('/')}/api/1.4/desktop/authentication"
pwd_b64 = base64.b64encode(PASSWORD.encode("utf-8")).decode("utf-8")
payload = {
    "username": USERNAME,
    "password": pwd_b64,
    "auth_type": "local_authentication"
}
headers = {"Content-Type": "application/json"}

resp = requests.post(url, json=payload, headers=headers, verify=VERIFY_SSL, timeout=20)

try:
    body = resp.json()
except ValueError:
    print("⚠️ پاسخ غیر JSON:", resp.text)
    exit(1)

if "two_factor_data" in body.get("message_response", {}).get("authentication", {}):
    print("✅ ارتباط با سرور برقرار شد — 2FA فعال است. سرور پاسخ می‌دهد.")
else:
    print("❌ ارتباط برقرار نشد یا 2FA فعال نیست. پاسخ سرور:")
    print(json.dumps(body, indent=2, ensure_ascii=False))

```
