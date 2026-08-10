## Methodology

1. **Discovery of Suspicious File**
   - Located a `package-json.bak` file in the `ftp` subpath, suggesting it might contain sensitive or outdated configuration data.
   - Downloaded the file using a **Poison Null Byte** attack to bypass extension restrictions.

2. **Analysis of Dependencies**
   - Examined the `package-json.bak` file and identified a suspicious dependency: `epilogue-js`.
   - Recognized that `epilogue-js` does not exist in public repositories, while the legitimate `epilogue` package does, indicating a **typosquatting** attack.

3. **Exploiting the Typosquatting Vulnerability**
   - Hypothesized that the system might be vulnerable to dependency confusion or typosquatting attacks due to the presence of the malicious `epilogue-js` package.
   - Submitted `epilogue-js 0.7` via the feedback section to trigger the vulnerability and confirm the exploit.

4. **Validation**
   - Received the challenge flag, confirming the successful exploitation of the typosquatting vulnerability.

### Tools Used
- **Poison Null Byte Attack**: To bypass file extension restrictions and download the `package-json.bak` file.
- **Dependency Analysis**: To identify and analyze suspicious packages in the configuration file.

---

## Vulnerabilities

- **Vulnerability Type**: Typosquatting (CWE-1035)
- **Affected Component**: Dependency management system, `package.json` configuration
- **Severity Level**: **High**
  - Allows attackers to exploit misspelled or malicious package names to execute arbitrary code or gain unauthorized access.

---

## Risks

- **Business Impact**:
  - **Malicious Code Execution**: Attackers can inject malicious code into the application by exploiting typosquatted packages.
  - **Supply Chain Attack**: Compromised dependencies can propagate through the software supply chain, affecting multiple systems.
  - **Data Breach**: Execution of malicious code may lead to unauthorized access to sensitive data.
  - **Reputational Damage**: Loss of customer trust due to perceived security weaknesses in dependency management.

---

## Actions

### Mitigation Strategies
- **Dependency Verification**: Implement strict verification processes for all dependencies, ensuring they are sourced from trusted repositories.
- **Automated Scanning**: Use automated tools to scan for typosquatted or malicious packages in dependency files.
- **Manual Review**: Conduct manual reviews of dependency lists to identify and remove suspicious or misspelled packages.

### Remediation Fixes
- **Dependency Pinning**: Pin dependencies to specific versions and use lock files to prevent unexpected updates.
- **Private Registry**: Use a private package registry to control and validate all dependencies.
- **Security Patching**: Regularly update and patch dependencies to mitigate known vulnerabilities.

### Best Security Practices
- **Regular Security Audits**: Conduct periodic security audits and penetration tests to identify and address vulnerabilities in dependency management.
- **Developer Training**: Train developers on secure coding practices, with a focus on dependency security and typosquatting awareness.
- **Incident Response Plan**: Develop and maintain an incident response plan to quickly address and mitigate supply chain attacks and security breaches.
