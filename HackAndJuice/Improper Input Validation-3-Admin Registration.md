## Methodology

1. **Initial Reconnaissance**
   - Registered a standard user account to intercept the registration request.
   - Analyzed the intercepted JSON payload to identify all fields and structure.

2. **Identifying the Vulnerability**
   - Observed that the registration request includes a `role` field, which is not explicitly set in the frontend form.
   - Hypothesized that manually adding the `admin` role to the request could grant administrative privileges.

3. **Exploiting the Vulnerability**
   - Modified the intercepted JSON payload to include the `role` field with the value `admin`:
     ```json
     {
         "email": "testte@test.fr",
         "password": "aaaaa",
         "passwordRepeat": "aaaaa",
         "role": "admin",
         "securityQuestion": {
             "id": 1,
             "question": "Your eldest siblings middle name?",
             "createdAt": "2026-02-23T10:19:48.889Z",
             "updatedAt": "2026-02-23T10:19:48.889Z"
         },
         "securityAnswer": "aaaaa"
     }
     ```
   - Forwarded the modified request using **Burp Suite**.

4. **Validation**
   - Confirmed successful registration with admin privileges, as indicated by the challenge flag.

### Tools Used
- **Burp Suite**: For intercepting and modifying HTTP requests.
- **JSON Analysis**: To understand and manipulate the registration payload.

---

## Vulnerabilities

- **Vulnerability Type**: Broken Access Control (CWE-284)
- **Affected Component**: User registration endpoint
- **Severity Level**: **Critical**
  - Allows unauthorized users to register with elevated privileges, bypassing intended access controls.

---

## Risks

- **Business Impact**:
  - **Unauthorized Access**: Attackers can gain admin privileges, enabling them to perform sensitive actions and access restricted data.
  - **Data Breach**: Elevated privileges may lead to exposure or manipulation of sensitive user and system data.
  - **Reputational Damage**: Loss of customer trust due to perceived security weaknesses and potential misuse of admin accounts.
  - **Operational Disruption**: Unauthorized admin actions could disrupt normal system operations and require costly remediation.

---

## Actions

### Mitigation Strategies
- **Input Validation**: Validate and sanitize all input fields, especially those related to roles and privileges.
- **Role Assignment**: Ensure role assignment is handled securely on the server-side, not relying on client-side input.
- **Least Privilege Principle**: Assign the minimum necessary privileges to user accounts by default.

### Remediation Fixes
- **Server-Side Role Assignment**: Implement role assignment logic on the server-side, ignoring any client-provided role fields.
- **Access Control**: Enforce strict access control checks to verify user privileges for all sensitive operations.
- **Audit Logs**: Maintain detailed logs of role changes and administrative actions for monitoring and forensic analysis.

### Best Security Practices
- **Regular Security Audits**: Conduct periodic security audits and penetration tests to identify and address access control vulnerabilities.
- **Developer Training**: Train developers on secure coding practices, with a focus on access control and privilege management.
- **Incident Response Plan**: Develop and maintain an incident response plan to quickly address and mitigate security breaches related to access control.
