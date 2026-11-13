### **Methodology**

1. **Sending Dummy HTTP Query**
   - Sent a dummy HTTP query to the Feedbacks root endpoint (`/api/Feedbacks/`).
   - Used Burp Suite to intercept the request.

2. **Interception and Repeater Usage**
   - Intercepted the request and sent it to the **Repeater** tool in Burp Suite.

3. **Spamming Requests**
   - Rapidly spammed the **SEND** button in the Repeater to send multiple queries in a few seconds.
   - The server accepted the requests without validating the CAPTCHA, bypassing the protection mechanism.

4. **Tools Used**
   - **Burp Suite** (for intercepting and sending repeated requests)
   - **Repeater** (for duplicating and spamming requests)

---
### **Vulnerabilities**

1. **Vulnerability Name**
   - **Broken Access Control** — Insufficient CAPTCHA validation (CWE-287)

2. **Affected Components**
   - **Feedback Submission System** (specifically the `/api/Feedbacks/` endpoint)

3. **Severity Level**
   - **Medium**
     - Allows attackers to bypass CAPTCHA protection, enabling automated submission of feedback or other actions.

---
### **Risks**

1. **Business Impact**
   - **Spam and Abuse**: Attackers can submit large volumes of feedback, overwhelming the system or skewing data.
   - **Data Integrity**: Automated submissions can pollute feedback data, making it unreliable.
   - **Reputational Damage**: Excessive spam or abuse can harm the platform's reputation and user experience.

2. **Exploitation Potential**
   - Attackers can use this technique to automate actions that require CAPTCHA validation.
   - The vulnerability can be chained with other attacks (e.g., brute force) for further exploitation.

---
### **Actions**

#### **Risk Mitigation Strategies**
- **Rate Limiting**: Implement rate limiting to prevent users from sending multiple requests in a short time.
- **Server-Side CAPTCHA Validation**: Ensure CAPTCHA validation is enforced server-side and cannot be bypassed.
- **Request Throttling**: Limit the number of requests a user can send within a specific time frame.

#### **Remediation Fixes**
- **Backend Modifications**:
  - Add robust CAPTCHA validation on the server side to ensure requests are legitimate.
  - Implement rate limiting and request throttling to prevent abuse.
- **Logging and Monitoring**: Log and monitor feedback submissions to detect suspicious activity.

#### **Best Security Practices**
- **CAPTCHA Best Practices**: Use modern CAPTCHA solutions (e.g., reCAPTCHA) that are difficult to bypass.
- **Regular Audits**: Conduct regular security audits to identify and fix similar vulnerabilities.
- **User Rate Limiting**: Implement rate limiting to prevent abuse of the feedback system.
