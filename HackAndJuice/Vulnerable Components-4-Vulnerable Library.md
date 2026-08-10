## Methodology

1. **Discovery of Backup File**
   - Located a `package.json.bak` file in the `ftp` directory at `https://ctf.juice.cyber.epitest.eu/ftp`.
   - Downloaded the file using a **Poison Null Byte** attack to bypass extension restrictions.

2. **Analysis of Dependencies**
   - Inspected the `package.json.bak` file to identify outdated or vulnerable libraries.
   - Found that the `express-jwt:0.1.3` library is listed as a dependency, known for critical security vulnerabilities.

3. **Exploiting the Vulnerability**
   - Recognized that the presence of this vulnerable library could be leveraged to exploit the system.
   - Submitted the library name and version (`express-jwt:0.1.3`) via the feedback section to trigger the vulnerability and confirm the exploit.

4. **Validation**
   - Received the challenge flag, confirming the successful identification and exploitation of the vulnerable library.

### Tools Used
- **Poison Null Byte Attack**: To bypass file extension restrictions and download the `package.json.bak` file.
- **Dependency Analysis**: To identify and analyze vulnerable libraries in the configuration file.

---

## Vulnerabilities

- **Vulnerability Type**: Use of Vulnerable Third-Party Component (CWE-1104)
- **Affected Component**: `express-jwt:0.1.3` library
- **Severity Level**: **Critical**
  - Allows attackers to exploit known vulnerabilities in the library, potentially leading to unauthorized access, data breaches, or other malicious activities.

---

## Risks

- **Business Impact**:
  - **Unauthorized Access**: Exploitation of the vulnerable library could allow attackers to bypass authentication and gain unauthorized access to the system.
  - **Data Breach**: Potential exposure of sensitive data, leading to regulatory penalties and loss of customer trust.
  - **System Compromise**: Attackers could execute arbitrary code or manipulate system behavior, leading to further compromise.
  - **Reputational Damage**: Loss of credibility and customer confidence due to the use of outdated and vulnerable components.

---

## Actions

### Mitigation Strategies
- **Dependency Updates**: Regularly update all third-party libraries and dependencies to their latest secure versions.
- **Vulnerability Scanning**: Use automated tools to scan for known vulnerabilities in dependencies and address them promptly.
- **Secure Coding Practices**: Follow secure coding guidelines to minimize the risk of introducing vulnerabilities through third-party components.

### Remediation Fixes
- **Patch Management**: Implement a patch management process to ensure timely updates and patches for all software components.
- **Library Whitelisting**: Maintain a whitelist of approved libraries and versions, rejecting any that do not meet security standards.
- **Security Audits**: Conduct regular security audits to identify and remediate vulnerable components.

### Best Security Practices
- **Regular Security Audits**: Schedule periodic security audits and penetration tests to identify and address vulnerabilities in third-party components.
- **Developer Training**: Train developers on secure coding practices, with a focus on dependency management and vulnerability awareness.
- **Incident Response Plan**: Develop and maintain an incident response plan to quickly address and mitigate exploits related to vulnerable libraries.
