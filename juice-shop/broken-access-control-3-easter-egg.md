### **Methodology**

1. **Discovery of FTP Subpath**
   - Explored the application's directory structure and identified a subpath `/ftp`.
   - Navigated to `/ftp` and observed a file named `eastere.gg`.

2. **Attempted File Access**
   - Clicked on `eastere.gg` to access its content.
   - Received an error due to the file not being in a supported format (e.g., `.md` or `.pdf`).
   - Despite the error, the flag was still exposed and retrieved.

3. **Tools Used**
   - **Browser** (for navigating and accessing the file)
   - **Manual Exploration** (to identify and access the `/ftp` subpath and file)

---
### **Vulnerabilities**

1. **Vulnerability Name**
   - **Broken Access Control** and **Poison Null Byte Injection** (CWE-22 and CWE-125)

2. **Affected Components**
   - **File Access Mechanism** (specifically the `/ftp` subpath and file handling)

3. **Severity Level**
   - **High**
     - Allows unauthorized access to sensitive files, potentially exposing sensitive data or flags.
     - The "Poison Null Byte" technique can bypass file extension checks, leading to arbitrary file access.

---
### **Risks**

1. **Business Impact**
   - **Data Exposure**: Sensitive files (e.g., flags, configuration files) may be exposed to unauthorized users.
   - **Information Disclosure**: Attackers can retrieve internal or proprietary information.
   - **Reputational Damage**: Public disclosure of sensitive data can harm the organization's reputation.
   - **Legal and Compliance Risks**: Unauthorized access to data may violate privacy laws or compliance requirements.

2. **Exploitation Potential**
   - Attackers can exploit this vulnerability to access restricted files or directories.
   - The technique can be chained with other attacks (e.g., directory traversal) for further exploitation.

---
### **Actions**

#### **Risk Mitigation Strategies**
- **Input Validation**: Ensure all file paths are validated and sanitized to prevent null byte injection and path traversal.
- **Access Control**: Implement strict access controls to restrict access to sensitive directories and files.
- **File Extension Checks**: Enforce strict file extension checks on the server side to prevent access to unsupported formats.

#### **Remediation Fixes**
- **Server-Side Fixes**:
  - Add middleware to validate and sanitize file paths before processing.
  - Implement strict file extension checks and reject files with null bytes or invalid characters.
- **Directory Permissions**: Restrict read/write permissions on sensitive directories to authorized users only.

#### **Best Security Practices**
- **Principle of Least Privilege**: Ensure users and processes have only the minimum permissions necessary.
- **Regular Audits**: Conduct regular security audits to identify and fix similar vulnerabilities.
- **Secure Coding Practices**: Follow secure coding guidelines to prevent common vulnerabilities like null byte injection and path traversal.
- **Reference**: [OWASP Path Traversal](https://owasp.org/www-community/attacks/Path_Traversal), [OWASP Null Byte Injection](https://owasp.org/www-community/vulnerabilities/Path_Traversal)
