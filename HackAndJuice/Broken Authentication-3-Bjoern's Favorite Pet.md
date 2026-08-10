### **Methodology**

1. **Reconnaissance**
   - Identified the challenge as resetting Bjoern's password by answering his security question: *"Name of your favorite pet?"*.
   - Determined that Bjoern is a real person — **Björn Kimminich**, the creator of OWASP Juice Shop.

2. **OSINT — Social Network Investigation**
   - Investigated Björn Kimminich's public social media profiles (Twitter, GitHub, LinkedIn).
   - No direct mention of a pet name was found on these platforms.

3. **OSINT — YouTube Research**
   - Searched YouTube for videos featuring Björn Kimminich demonstrating Juice Shop.
   - Found a talk in which he live-creates the `bjoern@owasp.org` account, entering his security answer in front of the camera.
   - The security answer was visible on screen: **`Zaya`**.

4. **Password Reset**
   - Navigated to the Forgot Password page and entered `bjoern@owasp.org`.
   - Submitted `Zaya` as the answer to the security question and successfully reset the password.

5. **Validation**
   - The password reset succeeded and the challenge was marked as solved.

6. **Tools Used**
   - **Browser** (for accessing the password reset flow)
   - **OSINT** (YouTube research on Björn Kimminich's public talks)

---
### **Vulnerabilities**

1. **Vulnerability Name**
   - **Broken Authentication — Security Answer Exposed via OSINT** (CWE-287)

2. **Affected Components**
   - **Password Reset System** (specifically the security question mechanism for `bjoern@owasp.org`)

3. **Severity Level**
   - **Medium**
     - Allows any attacker to reset the account password by finding the security answer through public video content.
     - No brute force or technical exploitation is required — only passive reconnaissance.

---
### **Risks**

1. **Business Impact**
   - **Account Takeover**: An attacker who views publicly available video content can reset the account password and gain full access.
   - **Data Breach**: Access to an admin or privileged account (such as the creator's) can expose all user data and application internals.
   - **Reputational Damage**: Compromise of a high-profile account (especially the application creator's) severely damages trust in the platform.

2. **Exploitation Potential**
   - The attack requires no technical skill — only the ability to search YouTube.
   - The vulnerability affects any account whose security answer was inadvertently disclosed in a public recording, demo, or screenshot.

---
### **Actions**

#### **Risk Mitigation Strategies**
- Replace security questions with more secure reset methods such as time-limited email tokens or TOTP-based verification.
- Ensure that demonstrations, tutorials, and live demos never reveal real credentials or security answers, even for test accounts.
- Implement rate limiting on the password reset endpoint to slow enumeration attempts.

#### **Remediation Fixes**
- Replace the security question reset flow with an email-based token reset link that expires after 15-30 minutes.
- Rotate and invalidate any credentials or security answers that have been exposed in public content.
- Add a lockout mechanism after 3-5 failed answer attempts to prevent brute force.

#### **Best Security Practices**
- Security question answers should be treated as secrets with the same sensitivity as passwords — never disclose them, even in a demo context.
- Use Multi-Factor Authentication (MFA) as the primary account recovery mechanism.
- Regularly audit public content (videos, screenshots, documentation) for inadvertent credential or secret exposure.
- **Reference**: [OWASP Forgot Password Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet.html)
