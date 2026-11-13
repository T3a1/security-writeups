## Methodology

1. **Discovery of Backup File**
   - Explored the `ftp` subpath at `https://ctf.juice.cyber.epitest.eu/ftp`.
   - Identified a backup file named `coupons_2013.md.bak`, which may contain sensitive or outdated sales data.

2. **Downloading the Backup File**
   - Downloaded the `coupons_2013.md.bak` file directly from the `ftp` subpath.
   - Confirmed the successful retrieval of the file, which triggered the challenge flag.

### Tools Used
- **Browser**: For navigating to the `ftp` subpath and downloading the file.

---

## Vulnerabilities

- **Vulnerability Type**: Sensitive Data Exposure (CWE-200), Backup File Exposure
- **Affected Component**: `ftp` subpath, `coupons_2013.md.bak` file
- **Severity Level**: **Medium**
  - Exposes potentially sensitive sales data, which could be leveraged by attackers to gain insights into business operations or exploit other vulnerabilities.

---

## Risks

- **Business Impact**:
  - **Information Leakage**: Exposure of sensitive sales data such as coupon codes, customer information, or internal promotions, which could aid attackers in further exploits.
  - **Reputational Damage**: Loss of customer trust due to perceived negligence in securing backup or outdated files.
  - **Operational Risks**: Potential misuse of exposed sales data to disrupt services or gain unauthorized access to promotional systems.

---

## Actions

### Mitigation Strategies
- **Secure File Management**: Ensure backup files are not accessible in public directories. Store them securely with restricted access.
- **Regular Audits**: Conduct regular audits of public-facing directories to identify and remove any unintentionally exposed files.
- **Access Controls**: Implement strict access controls for directories containing sensitive or backup files.

### Remediation Fixes
- **Remove Exposed Files**: Immediately remove any backup or sensitive files from public directories.
- **Automated Scanning**: Use automated tools to scan for and alert on exposed backup or sales data files.
- **File Naming Conventions**: Avoid using predictable or common backup file extensions (e.g., `.bak`) in public directories.

### Best Security Practices
- **Security Awareness Training**: Train developers and administrators on the risks of exposing backup files and the importance of secure file management.
- **Incident Response Plan**: Develop and maintain an incident response plan to quickly address and mitigate exposures of sensitive data.
- **Penetration Testing**: Include checks for exposed backup files in regular penetration testing to identify and secure unintended exposures.
