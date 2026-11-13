# juice-shop

Write-ups for [OWASP Juice Shop](https://github.com/juice-shop/juice-shop), a
deliberately vulnerable web shop used to practise web security. Each write-up
gives the method used, the vulnerability (with its CWE), its impact, and how to
fix it.

45 challenges solved, from 3 to 6 stars (the Juice Shop difficulty scale).

| Category | Challenge | Difficulty |
|----------|-----------|------------|
| Broken Access Control | [Basket Manipulation](broken-access-control-3-basket-manipulation.md) | ★★★ |
|  | [Easter Egg](broken-access-control-3-easter-egg.md) | ★★★ |
|  | [Feedback Manipulation](broken-access-control-3-feedback-manipulation.md) | ★★★ |
|  | [Product Tampering](broken-access-control-3-product-tampering.md) | ★★★ |
|  | [Review Manipulation](broken-access-control-3-review-manipulation.md) | ★★★ |
| Broken Anti Automation | [CAPTCHA Bypass](broken-anti-automation-3-captcha-bypass.md) | ★★★ |
|  | [Extra Language](broken-anti-automation-3-extra-language.md) | ★★★ |
|  | [Multiple Likes](broken-anti-automation-3-multiple-likes.md) | ★★★ |
| Broken Authentication | [Bjoern's Favorite Pet](broken-authentication-3-bjoerns-favorite-pet.md) | ★★★ |
|  | [GDPR Data Erasure](broken-authentication-3-gdpr-data-erasure.md) | ★★★ |
|  | [Reset Jim's Password](broken-authentication-3-reset-jims-password.md) | ★★★ |
|  | [Login Bjoern](broken-authentication-4-login-bjoern.md) | ★★★★ |
|  | [Reset Bender's Password](broken-authentication-4-reset-benders-password.md) | ★★★★ |
|  | [Reset Bjoern's Password](broken-authentication-5-reset-bjoerns-password.md) | ★★★★★ |
| Cryptographic Issues | [Nested Easter Egg](cryptographic-issues-4-nested-easter-egg.md) | ★★★★ |
|  | [Forged Coupon](cryptographic-issues-6-forged-coupon.md) | ★★★★★★ |
| Improper Input Validation | [Admin Registration](improper-input-validation-3-admin-registration.md) | ★★★ |
|  | [Deluxe Fraud](improper-input-validation-3-deluxe-fraud.md) | ★★★ |
|  | [Payback Time](improper-input-validation-3-payback-time.md) | ★★★ |
|  | [Upload Size](improper-input-validation-3-upload-size.md) | ★★★ |
|  | [Upload Type](improper-input-validation-3-upload-type.md) | ★★★ |
|  | [Poison Null Byte](improper-input-validation-4-poison-null-byte.md) | ★★★★ |
| Injection | [Database Schema](injection-3-database-schema.md) | ★★★ |
|  | [Login Bender](injection-3-login-bender.md) | ★★★ |
|  | [Login Jim](injection-3-login-jim.md) | ★★★ |
|  | [Christmas Special](injection-4-christmas-special.md) | ★★★★ |
|  | [NoSQL DoS](injection-4-nosql-dos.md) | ★★★★ |
|  | [NoSQL Manipulation](injection-4-nosql-manipulation.md) | ★★★★ |
|  | [User Credentials](injection-4-user-credentials.md) | ★★★★ |
| Security through Obscurity | [Privacy Policy Inspection](security-through-obscurity-3-privacy-policy-inspection.md) | ★★★ |
|  | [Steganography](security-through-obscurity-4-steganography.md) | ★★★★ |
| Sensitive Data Exposure | [Login Amy](sensitive-data-exposure-3-login-amy.md) | ★★★ |
|  | [Forgotten Developper Backup](sensitive-data-exposure-4-forgotten-developper-backup.md) | ★★★★ |
|  | [Forgotten Sales Backup](sensitive-data-exposure-4-forgotten-sales-backup.md) | ★★★★ |
|  | [Reset Uvogin's Password](sensitive-data-exposure-4-reset-uvogins-password.md) | ★★★★ |
| Unvalidated Redirects | [Allowlist Bypass](unvalidated-redirects-4-allowlist-bypass.md) | ★★★★ |
| Vulnerable Components | [Legacy Typosquatting](vulnerable-components-4-legacy-typosquatting.md) | ★★★★ |
|  | [Vulnerable Library](vulnerable-components-4-vulnerable-library.md) | ★★★★ |
|  | [Unsigned JWT](vulnerable-components-5-unsigned-jwt.md) | ★★★★★ |
| XSS | [API-only XSS](xss-3-api-only-xss.md) | ★★★ |
|  | [Client-side XSS Protection](xss-3-client-side-xss-protection.md) | ★★★ |
|  | [CSP Bypass](xss-4-csp-bypass.md) | ★★★★ |
|  | [HTTP-Header XSS](xss-4-http-header-xss.md) | ★★★★ |
|  | [Server-side XSS Protection](xss-4-server-side-xss-protection.md) | ★★★★ |
| XXE | [XXE Data Access](xxe-3-xxe-data-access.md) | ★★★ |

`images/` holds the screenshots, `drafts/` the write-ups not finished yet, and
`presentation.odp` the slides of the final presentation.
