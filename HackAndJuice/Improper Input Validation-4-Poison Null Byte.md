## Methodology

1. **Initial Attempt**
   - Attempted to access the file directly via `https://ctf.juice.cyber.epitest.eu/ftp/eastere.gg`.
   - Encountered an error due to the file extension not being `.pdf` or `.md`.

2. **Understanding the Restriction**
   - Recognized that the system enforces file extension checks, only allowing `.pdf` or `.md` files to be accessed or downloaded.
   - Attempted to bypass this restriction by appending `.md` to the filename, but received an error indicating the file did not exist.

3. **Exploiting the Null Byte Vulnerability**
   - Researched and identified the **Poison Null Byte** technique, which can truncate strings in certain systems.
   - Crafted a URL with a null byte (`%00`) to terminate the filename early, effectively bypassing the extension check:
     ```
     https://ctf.juice.cyber.epitest.eu/ftp/eastere.gg%2500.md
     ```
   - The `%25` is a URL-encoded `%`, which ensures the null byte (`%00`) is correctly interpreted by the server.

4. **Validation**
   - Successfully accessed and downloaded the `eastere.gg` file by tricking the system into ignoring the appended `.md`.
   - Confirmed the exploitation by receiving the challenge flag and accessing the file content.

### Tools Used
- **URL Encoding**: To craft the malicious URL with a null byte.
- **Browser**: To test and validate the exploit.

---

## Vulnerabilities

- **Vulnerability Type**: Poison Null Byte (CWE-134)
- **Affected Component**: File access/delivery system
- **Severity Level**: **High**
  - Allows unauthorized access to files by bypassing extension-based security checks, potentially exposing sensitive or restricted content.

---

## Risks

- **Business Impact**:
  - **Unauthorized File Access**: Attackers can access files that should be restricted, leading to potential data leaks.
  - **Security Bypass**: Circumvents security controls, undermining the integrity of the file access system.
  - **Reputational Damage**: Loss of customer trust due to perceived security weaknesses in file handling.
  - **Compliance Violations**: Potential non-compliance with data protection regulations if sensitive files are exposed.

---

## Actions

### Mitigation Strategies
- **Input Validation**: Validate and sanitize all user-supplied input, especially filenames and URLs, to prevent null byte injection.
- **Secure File Handling**: Implement strict checks for file extensions and types on the server-side, ensuring they cannot be bypassed.
- **Use of Safe Functions**: Avoid functions or APIs that are vulnerable to null byte poisoning; use secure alternatives for file operations.

### Remediation Fixes
- **Server-Side Extension Checks**: Ensure file extension validation is performed on the server-side and cannot be bypassed by client-side manipulation.
- **Encoding and Decoding**: Properly handle URL encoding/decoding to prevent interpretation of null bytes or other malicious characters.
- **File Access Controls**: Implement robust access controls and permissions for files, restricting access to authorized users only.

### Best Security Practices
- **Regular Security Audits**: Conduct periodic security audits and penetration tests to identify and address vulnerabilities in file handling.
- **Developer Training**: Train developers on secure coding practices, with a focus on input validation and file security.
- **Incident Response Plan**: Develop and maintain an incident response plan to quickly address and mitigate unauthorized file access and security breaches.
