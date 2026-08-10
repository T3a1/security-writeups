### **Methodology**

1. **Reconnaissance**
   - Identified the challenge as a persisted XSS attack requiring the payload `<iframe src="javascript:alert(`xss`)">` while bypassing a client-side protection mechanism.

2. **Surface Mapping**
   - Navigated to `/#/profile` and attempted to submit the XSS payload directly in the username field.
   - The Angular form encoded the special characters before sending them to the server (e.g., `<` became `%3C`), preventing the payload from being stored as raw HTML.
   - This confirmed the presence of a client-side validation mechanism.

3. **Source Code Analysis**
   - Checked the public GitHub repository to understand how the profile update worked.
   - Found in `models/user.ts` that the challenge `persistedXssUserChallenge` is triggered when the XSS payload appears in the **email field** of a new user:
     ```js
     set (email: string) {
       challengeUtils.solveIf(challenges.persistedXssUserChallenge, () => {
         return utils.contains(email, '<iframe src="javascript:alert(`xss`)">')
       })
     }
     ```

4. **Identifying the Bypass**
   - The client-side protection only exists in the Angular frontend form, which URL-encodes user input before submission.
   - By calling the API directly via `fetch`, the Angular validation is bypassed entirely and raw, unencoded payloads can be sent.

5. **Exploit**
   - Sent a `POST` request directly to `/api/Users` to create a new user with the XSS payload in the email field:
     ```js
     fetch('/api/Users', {
       method: 'POST',
       headers: { 'Content-Type': 'application/json' },
       body: JSON.stringify({
         email: '<iframe src="javascript:alert(`xss`)">',
         password: 'test1234',
         passwordRepeat: 'test1234',
         securityQuestion: { id: 1, question: 'Your eldest siblings middle name?' },
         securityAnswer: 'test'
       })
     })
     ```

6. **Validation**
   - The server accepted the payload without sanitization, stored it in the database, and the challenge was marked as solved.

7. **Tools Used**
   - **Browser DevTools** (Network tab, console)
   - **GitHub Source Code Review** (to identify the vulnerable field)
   - **JavaScript `fetch` API** (for bypassing the Angular form)

---
### **Vulnerabilities**

1. **Vulnerability Name**
   - **Stored/Persisted Cross-Site Scripting (XSS)** (CWE-79)

2. **Affected Components**
   - **User Registration Endpoint** (`POST /api/Users`), email field, client-side Angular form validation

3. **Severity Level**
   - **High**
     - The application relies exclusively on client-side validation, which is trivially bypassed by interacting with the API directly.
     - The server-side code does not sanitize the email field when storing it, allowing arbitrary HTML to be persisted in the database.

---
### **Risks**

1. **Business Impact**
   - **Session Hijacking**: A stored XSS payload in a user's email can execute arbitrary JavaScript when an administrator views the user list, potentially stealing session tokens and leading to account takeover.
   - **Credential Theft**: Malicious scripts can exfiltrate cookies, localStorage data, or intercept form submissions.
   - **Privilege Escalation**: If an admin account is compromised via XSS, the attacker gains full control over the application.
   - **Reputational Damage**: XSS vulnerabilities expose users to phishing, defacement, and malware delivery, severely damaging trust in the application.

2. **Exploitation Potential**
   - Any authenticated user can register a new account with a malicious payload via the API.
   - The payload executes for every admin who views the user management panel, with no further interaction required.

---
### **Actions**

#### **Risk Mitigation Strategies**
- Never rely solely on client-side validation for security — all input validation and sanitization must be enforced server-side.
- Apply output encoding when rendering user-supplied content in HTML contexts.
- Implement a strict Content Security Policy (CSP) to limit the impact of any XSS that bypasses sanitization.

#### **Remediation Fixes**
- Sanitize all user input on the server side before storing it in the database, using a library such as `DOMPurify` (server-side via jsdom) or `sanitize-html` with a strict allowlist.
- Validate the email field format with a proper email regex on the server side, which would reject `<iframe src="...">` as a malformed email.
- Apply `helmet` with a strict CSP header to prevent inline script execution.

#### **Best Security Practices**
- Client-side validation improves UX, but server-side validation is the only real security gate.
- Use parameterized queries and ORM sanitization hooks consistently across all model setters.
- Regularly test API endpoints directly (not just through the UI) as part of security reviews — UI-level protections are always bypassable.
- **Reference**: [OWASP XSS Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)
