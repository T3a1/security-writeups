### **Methodology**

1. **Observation of Language Files**
   - Noticed that changing the language triggers a request to `/assets/n18n/fr_FR.json`.
   - Understood that each language has its own JSON file.

2. **Discovery of Additional Language Files**
   - Used browser DevTools to inspect visible language files.
   - To uncover hidden or extra language files, performed a brute-force search using the globbing pattern `*_??.json`.
   - Found a positive response for the file `tlh_AA.json`.

3. **Accessing the Extra Language File**
   - Successfully accessed the page `/assets/n18n/tlh_AA.json` and retrieved the flag.

4. **Tools Used**
   - **Browser DevTools** (for inspecting network requests and language files)
   - **Manual Brute-Force** (to discover hidden language files)

---
### **Vulnerabilities**

1. **Vulnerability Name**
   - **Broken Access Control** — Insecure file enumeration (CWE-22)

2. **Affected Components**
   - **Language Localization System** (specifically the `/assets/n18n/` directory)

3. **Severity Level**
   - **Medium**
     - Allows unauthorized access to sensitive or hidden language files, potentially exposing internal data or flags.

---
### **Risks**

1. **Business Impact**
   - **Information Disclosure**: Sensitive or internal data embedded in language files may be exposed.
   - **Unauthorized Access**: Attackers can discover and access hidden or extra language files, leading to further exploitation.
   - **Reputational Damage**: Public disclosure of internal data can harm the organization's reputation.

2. **Exploitation Potential**
   - Attackers can use this technique to discover additional endpoints or files, which may contain sensitive information or flags.
   - The vulnerability can be chained with other attacks (e.g., directory traversal) for further exploitation.

---
### **Actions**

#### **Risk Mitigation Strategies**
- **Input Validation**: Validate and sanitize all file paths to prevent insecure file enumeration.
- **Access Control**: Implement strict access controls to restrict access to sensitive directories and files.
- **Directory Listing Protection**: Disable directory listing to prevent users from browsing directory contents.

#### **Remediation Fixes**
- **Server-Side Fixes**:
  - Add middleware to validate and sanitize file paths before processing.
  - Implement strict access controls to prevent unauthorized access to language files.
- **File Permissions**: Restrict read permissions on sensitive directories to authorized users only.

#### **Best Security Practices**
- **Principle of Least Privilege**: Ensure users and processes have only the minimum permissions necessary.
- **Regular Audits**: Conduct regular security audits to identify and fix similar vulnerabilities.
- **Secure Coding Practices**: Follow secure coding guidelines to prevent common vulnerabilities like insecure file enumeration.
