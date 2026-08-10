### **Methodology**

1. **Reconnaissance**
   - Identified the challenge as resetting Bjoern's password by answering his security question: *"What's your zip code from your teen years?"*.
   - Determined that Bjoern is **Björn Kimminich**, a real person and the creator of OWASP Juice Shop.

2. **OSINT — Identifying the City of Origin**
   - Researched Björn Kimminich's public profiles (Facebook, LinkedIn, GitHub).
   - Found his Facebook `About` page, which listed his hometown as **Uetersen**, Germany.

3. **Current Zip Code Identification**
   - Looked up the current postal code for Uetersen: **25436**.
   - Submitted `25436` as the security answer — the application rejected it as invalid.

4. **Historical Research — Pre-1993 German Zip Codes**
   - Analyzed why the current zip code was rejected: Germany reformed its postal code system in **1993**, replacing the 4-digit East/West codes with a unified 5-digit system.
   - Researched the pre-1993 West German postal code for Uetersen, which was **W-2082** (also written as `West-2082`).

5. **Password Reset**
   - Submitted `West-2082` as the security answer and successfully reset Bjoern's password.

6. **Validation**
   - The password reset succeeded and the challenge was marked as solved.

7. **Tools Used**
   - **Browser** (for accessing the password reset flow)
   - **OSINT** (Facebook public profile, German postal code history research)

---
### **Vulnerabilities**

1. **Vulnerability Name**
   - **Broken Authentication — Security Answer Discoverable via OSINT** (CWE-287)

2. **Affected Components**
   - **Password Reset System** (specifically the security question mechanism for `bjoern@owasp.org`)

3. **Severity Level**
   - **High**
     - Allows a determined attacker to reset the account password using only public information and historical research.
     - No technical exploitation is required — purely passive reconnaissance.

---
### **Risks**

1. **Business Impact**
   - **Account Takeover**: An attacker with access to public social media profiles and historical reference data can reset the password and gain full account access.
   - **Privilege Escalation**: If the account has administrative privileges, the attacker gains control over the entire application.
   - **Reputational Damage**: Compromise of the application creator's account via a guessable security answer constitutes a critical trust failure.
   - **Data Breach**: Full access to the account exposes all associated personal and transactional data.

2. **Exploitation Potential**
   - The attack requires only knowledge of the target's city of origin and awareness of historical postal code formats.
   - This level of OSINT is accessible to any motivated attacker and cannot be prevented once the information is public.

---
### **Actions**

#### **Risk Mitigation Strategies**
- Replace security questions with more secure password reset mechanisms such as time-limited email tokens or TOTP-based verification.
- Avoid security questions based on facts that can be derived from public records, social media, or historical databases.
- Implement rate limiting on the password reset endpoint to slow enumeration and brute force attempts.

#### **Remediation Fixes**
- Replace the security question reset flow with a tokenized email reset link that expires after 15-30 minutes.
- If security questions are retained, reject questions whose answers are historical facts, geographic data, or otherwise derivable from public records.
- Add an account lockout mechanism after 3-5 failed security answer attempts.

#### **Best Security Practices**
- Security questions based on historical facts, locations, or names are inherently insecure — an attacker with patience and research skills will find the answer.
- NIST SP 800-63B recommends against using knowledge-based authentication for any security-sensitive operation.
- Use Multi-Factor Authentication (MFA) as the standard account recovery mechanism.
- **Reference**: [OWASP Forgot Password Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet.html)
