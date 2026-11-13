## Methodology

1. **Reconnaissance** — Identified the challenge as bypassing the redirect allowlist to redirect users to an arbitrary external URL.
    
2. **Source code analysis (OSINT)** — Found the redirect validation logic in `lib/insecurity.ts` on the public GitHub repository:
    

```javascript
export const redirectAllowlist = new Set([
  'https://github.com/juice-shop/juice-shop',
  'https://blockchain.info/address/1AbKfgvw9psQ41NbLi8kufDQTezwG8DRZm',
  'https://explorer.dash.org/address/Xr556RzuwX6hg5EGpkybbv5RanJoZN17kW',
  'https://etherscan.io/address/0x0f933ab9fcaaa782d0279c300d73750e1311eae6',
  'http://shop.spreadshirt.com/juiceshop',
  'http://shop.spreadshirt.de/juiceshop',
  'https://www.stickeryou.com/products/owasp-juice-shop/794',
  'http://leanpub.com/juice-shop'
])

export const isRedirectAllowed = (url: string) => {
  let allowed = false
  for (const allowedUrl of redirectAllowlist) {
    allowed = allowed || url.includes(allowedUrl)
  }
  return allowed
}
```

3. **Vulnerability identification** — The validation uses `url.includes(allowedUrl)` instead of checking for an exact match or validating the URL's origin. This means any URL that merely **contains** an allowlisted string anywhere in it will pass the check — including as a query parameter.
    
4. **Bypass construction** — Crafted a redirect URL where the target is an arbitrary domain, but the allowlisted URL is appended as a query parameter:
    

```
https://ctf.juice.cyber.epitest.eu/redirect?to=https://google.com?x=https://github.com/juice-shop/juice-shop
```

- The `to` parameter points to `https://google.com` (arbitrary target)
- The query parameter `?x=https://github.com/juice-shop/juice-shop` causes the full URL string to contain the allowlisted value
- `isRedirectAllowed()` returns `true` because `url.includes('https://github.com/juice-shop/juice-shop')` is `true`

5. **Exploit** — Navigated to the crafted URL in the browser. The server validated the redirect as allowed and redirected to `https://google.com`, triggering the challenge as solved.

**Tools used:** Browser navigation, GitHub source code review.

---

## Vulnerabilities

**Name:** Open Redirect via Allowlist Bypass — CWE-601 (URL Redirection to Untrusted Site)  
**Affected component:** Redirect endpoint (`/redirect`), `isRedirectAllowed()` function in `lib/insecurity.ts`  
**Severity:** Medium

The redirect allowlist validation uses `String.includes()` to check whether the target URL contains an allowlisted domain. This is a substring match, not an origin or exact URL match. An attacker can bypass the allowlist by appending an allowlisted URL as a query parameter to an arbitrary target domain. The server incorrectly validates the redirect as safe and forwards the user to the attacker-controlled destination.

---

## Risks

**Business impact:**

- **Phishing** — Attackers can craft links that appear to originate from the trusted Juice Shop domain but redirect users to malicious sites. Users are more likely to trust a link from a known domain.
- **Credential harvesting** — Redirecting users to convincing phishing pages allows attackers to steal login credentials, especially if the redirect follows a legitimate-looking action.
- **OAuth token theft** — Open redirects are frequently exploited in OAuth flows to steal authorization codes or tokens by hijacking the redirect_uri parameter.
- **Reputational damage** — If the Juice Shop domain is associated with phishing campaigns, customer trust is severely damaged.

---

## Actions

### Mitigation strategies

- Replace the `includes()` substring check with a strict origin/hostname comparison.
- Validate only the hostname/origin of the target URL against the allowlist, not the full URL string.
- Consider removing the open redirect endpoint entirely if it is not strictly necessary.

### Remediation fixes

Replace the current validation with a strict origin check:

```javascript
export const isRedirectAllowed = (url: string) => {
  try {
    const targetOrigin = new URL(url).origin
    for (const allowedUrl of redirectAllowlist) {
      const allowedOrigin = new URL(allowedUrl).origin
      if (targetOrigin === allowedOrigin) return true
    }
    return false
  } catch {
    return false
  }
}
```

This ensures only URLs whose **origin** exactly matches an allowlisted origin are accepted, regardless of query parameters or path.

### Best security practices

- Never use substring matching for security-critical URL validation — always parse and compare URL components (scheme, host, port) individually.
- Log and monitor all redirect requests to detect abuse patterns.
- If a redirect allowlist is necessary, keep it minimal and review it regularly.
- Reference: [OWASP Unvalidated Redirects and Forwards Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Unvalidated_Redirects_and_Forwards_Cheat_Sheet.html)