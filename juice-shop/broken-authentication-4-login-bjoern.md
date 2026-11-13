### **Methodology**

1. **Account Discovery**
   - Logged in as an admin and navigated to the `/administration` panel.
   - Found Björn Kimminich's Gmail address listed among the registered users.

2. **Source Code Analysis**
   - The challenge is tagged as `Code Analysis`, suggesting the password could be found in the application's source code.
   - Accessed the publicly available Juice Shop GitHub repository and searched for hardcoded credentials.
   - Found Bjoern's password stored in cleartext directly in the source code (not hashed).

3. **Authentication**
   - Used the discovered email address and the cleartext password found in the source code to log in via the standard login form.

4. **Validation**
   - Login succeeded and the challenge was marked as solved.

5. **Tools Used**
   - **Browser** (for navigating the admin panel and login form)
   - **GitHub Source Code Review** (to identify the hardcoded cleartext password)

---
### **Vulnerabilities**

1. **Vulnerability Name**
   - **Hardcoded Credentials in Source Code** (CWE-798) and **Cleartext Storage of Sensitive Information** (CWE-312)

2. **Affected Components**
   - **Application Source Code** (hardcoded user credentials) and **User Authentication System** (`POST /rest/user/login`)

3. **Severity Level**
   - **High**
     - A password stored in cleartext in a publicly accessible repository can be discovered by anyone who reads the code.
     - Hardcoded credentials cannot be rotated without a code change and redeployment.

---
### **Risks**

1. **Business Impact**
   - **Account Takeover**: Any person with read access to the repository can log in as the affected user without any technical exploitation.
   - **Privilege Escalation**: If the compromised account has elevated privileges (admin, moderator), the attacker gains full control over the application.
   - **Reputational Damage**: Storing passwords in cleartext in a public repository is a fundamental security failure that severely damages user and stakeholder trust.
   - **Compliance Risks**: Cleartext storage of credentials may violate data protection regulations and industry standards (e.g., PCI-DSS, GDPR).

2. **Exploitation Potential**
   - No technical skill is required — the attack is limited to reading the source code and using the found credentials.
   - Automated secret-scanning tools (e.g., GitHub secret scanning, `truffleHog`) can detect such leaks instantly.

---
### **Actions**

#### **Risk Mitigation Strategies**
- Never store passwords or any credentials in source code, configuration files, or version control history.
- Use environment variables or a dedicated secrets manager (e.g., HashiCorp Vault, AWS Secrets Manager) to manage sensitive credentials.
- Hash all user passwords with a strong algorithm (bcrypt, Argon2) before storing them in the database.

#### **Remediation Fixes**
- Immediately rotate the exposed credentials and invalidate all active sessions for the affected account.
- Remove the hardcoded credentials from the source code and purge them from git history using `git filter-repo` or BFG Repo-Cleaner.
- Replace the hardcoded value with a reference to an environment variable or secrets manager.

#### **Best Security Practices**
- Integrate secret-scanning tools (e.g., `git-secrets`, `truffleHog`, GitHub Advanced Security) into CI/CD pipelines to prevent credential commits.
- Enforce a policy of zero hardcoded secrets across all repositories.
- Passwords must always be stored as strong one-way hashes — cleartext or weakly encrypted storage is never acceptable.
- **Reference**: [OWASP Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)
