### **Methodology**

1. **Reconnaissance**
   - Identified the challenge as a persisted XSS attack performed through an HTTP header, without using the frontend.

2. **Hidden Endpoint Discovery**
   - Opened DevTools and used `Ctrl+Shift+F` to search through all loaded JavaScript files.
   - Searching for `/rest/` revealed all available API endpoints, including `/rest/saveLoginIp`.
   - Examining the surrounding code revealed that this endpoint reads the `True-Client-IP` header and stores its value as the user's last login IP address.

3. **Exploit**
   - Sent a `GET` request to `/rest/saveLoginIp` from the browser console, injecting the XSS payload directly in the `True-Client-IP` header:
     ```js
     fetch('/rest/saveLoginIp', {
       method: 'GET',
       headers: {
         'Authorization': 'Bearer ' + localStorage.getItem('token'),
         'True-Client-IP': '<iframe src="javascript:alert(`xss`)">'
       },
       credentials: 'include'
     }).then(r => r.json()).then(console.log)
     ```
   - The server stored the header value directly in the database as `lastLoginIp` without any sanitization.

4. **Validation**
   - When an admin views the user list, the stored payload executes in the browser and the challenge was marked as solved.

5. **Tools Used**
   - **Browser DevTools** (`Ctrl+Shift+F` for JS source search, console)
   - **JavaScript `fetch` API** (for sending the crafted request with the malicious header)

---
### **Vulnerabilities**

1. **Vulnerability Name**
   - **Stored/Persisted Cross-Site Scripting (XSS) via HTTP Header Injection** (CWE-79)

2. **Affected Components**
   - **`/rest/saveLoginIp` Endpoint**, `True-Client-IP` header, `lastLoginIp` field in the Users database table

3. **Severity Level**
   - **High**
     - The server trusts and stores user-controlled HTTP header values without any validation or sanitization.
     - The stored payload executes in the admin panel, giving the attacker a direct path to administrative session hijacking.

---
### **Risks**

1. **Business Impact**
   - **Administrative Session Hijacking**: The XSS payload is displayed in the admin user list and executes when any administrator views it, allowing theft of the admin session token.
   - **Privilege Escalation**: Compromising an admin session grants full control over the application, including access to all user data.
   - **Data Breach**: Sensitive user data (emails, order history, payment information) is exposed once admin access is obtained.
   - **Reputational Damage**: A stored XSS that specifically targets administrators is a critical vulnerability that severely damages user and stakeholder trust.

2. **Exploitation Potential**
   - Any authenticated user can trigger this attack by sending a single crafted request.
   - The payload is persistent and will execute every time an admin loads the user list, without any further attacker interaction.

---
### **Actions**

#### **Risk Mitigation Strategies**
- Never trust or directly store the value of user-controlled HTTP headers (such as `X-Forwarded-For`, `True-Client-IP`) without validation and sanitization.
- Validate that IP address fields contain only valid IP address formats before storing them in the database.
- Apply output encoding when rendering stored IP addresses or other user-controlled values in HTML contexts.

#### **Remediation Fixes**
- Add server-side validation on `/rest/saveLoginIp` to ensure the `True-Client-IP` header contains only a valid IPv4 or IPv6 address before storing it.
- Sanitize the `lastLoginIp` field when rendering it in the admin panel using a strict output encoding library.
- Implement a Content Security Policy (CSP) header to limit the impact of any XSS that bypasses sanitization.

#### **Best Security Practices**
- HTTP headers are user-controlled inputs and must be treated with the same level of distrust as form fields or query parameters.
- Apply input validation at the point of ingestion, not just at the point of display.
- Regularly audit endpoints that handle non-standard HTTP headers, as these are commonly overlooked during security reviews.
- **Reference**: [OWASP XSS Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)
