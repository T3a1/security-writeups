### **Methodology**

1. **Reconnaissance**
   - Identified the challenge as a persisted XSS attack performed exclusively through the API, without using the frontend application.
   - The challenge hint states: *"Careless developers might have exposed API methods that the client does not even need."*

2. **Source Code Analysis**
   - Searched the public GitHub repository for the challenge trigger condition.
   - Found in `models/product.ts` that the challenge is triggered when the XSS payload appears in a **product description**:
     ```js
     set (description: string) {
       challengeUtils.solveIf(challenges.restfulXssChallenge, () => {
         return utils.contains(description, '<iframe src="javascript:alert(`xss`)">')
       })
     }
     ```

3. **API Enumeration**
   - Identified that the `/api/Products/:id` endpoint accepts `PUT` requests with a JSON body, allowing product descriptions to be updated directly via the REST API without going through the frontend.

4. **Exploit**
   - Sent a `PUT` request directly to `/api/Products/1` with the XSS payload in the description field:
     ```js
     fetch('/api/Products/1', {
       method: 'PUT',
       headers: {
         'Content-Type': 'application/json',
         'Authorization': 'Bearer ' + localStorage.getItem('token')
       },
       body: JSON.stringify({
         description: '<iframe src="javascript:alert(`xss`)">'
       })
     })
     ```

5. **Validation**
   - The server accepted the payload, stored it in the product description, and the challenge was marked as solved.
   - The payload executes when any user views the product, as the frontend renders product descriptions as raw HTML via `bypassSecurityTrustHtml`.

6. **Tools Used**
   - **Browser DevTools** (console)
   - **GitHub Source Code Review** (to locate the vulnerable field and trigger condition)
   - **JavaScript `fetch` API** (for sending the direct API request)

---
### **Vulnerabilities**

1. **Vulnerability Name**
   - **Stored/Persisted Cross-Site Scripting (XSS)** (CWE-79) and **Broken Access Control on REST API** (CWE-284)

2. **Affected Components**
   - **Product API Endpoint** (`PUT /api/Products/:id`), product description field, `bypassSecurityTrustHtml` in `search-result.component.ts`

3. **Severity Level**
   - **High**
     - Any authenticated user can modify product descriptions via the API, even though the frontend does not expose this functionality.
     - The Angular frontend explicitly disables its own XSS sanitization when rendering product descriptions, meaning any stored HTML executes in the browser.

---
### **Risks**

1. **Business Impact**
   - **Mass User Impact**: A payload injected into a product description is displayed to every user who views that product, dramatically increasing the attack surface compared to a user-profile XSS.
   - **Session Hijacking**: The XSS payload can steal session tokens from all affected users, leading to mass account takeover.
   - **Credential Theft and Phishing**: Malicious scripts can redirect users to phishing pages or inject fake login forms to harvest credentials.
   - **Reputational and Legal Damage**: A mass XSS incident affecting customers constitutes a data breach with potential GDPR implications.

2. **Exploitation Potential**
   - Any authenticated user can trigger this attack — no elevated privileges are required.
   - The payload persists in the database and affects every subsequent visitor without further attacker interaction.

---
### **Actions**

#### **Risk Mitigation Strategies**
- Restrict API endpoints to expose only the HTTP methods actually needed by the frontend — a regular customer should not be able to update product descriptions.
- Implement role-based access control (RBAC) on all API endpoints: product updates should require admin privileges.
- Never use `bypassSecurityTrustHtml` in Angular unless the content is fully trusted and sanitized server-side.

#### **Remediation Fixes**
- Remove or restrict the `PUT` method on `/api/Products/:id` for non-admin users by adding proper authorization middleware.
- Replace `bypassSecurityTrustHtml` in `search-result.component.ts` with Angular's default sanitization, or use `DOMPurify` to sanitize HTML before rendering.
- Sanitize product description input server-side using a strict HTML allowlist before storing it in the database.
- Implement a Content Security Policy (CSP) header that disallows inline scripts and restricts script sources.

#### **Best Security Practices**
- Apply the principle of least privilege to API endpoints — expose only what is needed, to whom it is needed.
- Never disable framework-level security mechanisms (like Angular's XSS sanitization) without compensating controls.
- Conduct regular API audits to identify endpoints accessible but unused by the frontend — these are common attack vectors.
- **Reference**: [OWASP XSS Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)
