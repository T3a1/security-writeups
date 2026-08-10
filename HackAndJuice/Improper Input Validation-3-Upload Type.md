## Methodology

1. **Initial Setup**
   - Navigated to the Complaint page and selected a legitimate `.zip` or `.pdf` file.
   - Added a dummy message in the text input field to complete the form.

2. **Intercepting the Upload Request**
   - Started **Burp Suite Interceptor** to capture the HTTP POST request generated upon form submission.
   - Submitted the form and intercepted the request to analyze its structure.

3. **Manipulating the File Extension**
   - Identified the file extension within the POST request.
   - Modified the file extension to an unauthorized or unexpected type (e.g., `.exe`, `.sh`, or another restricted format).

4. **Executing the Exploit**
   - Forwarded the modified request to the server, bypassing client-side type validation.
   - Confirmed the successful upload of the file with the manipulated extension, triggering the challenge flag.

### Tools Used
- **Burp Suite**: For intercepting and modifying HTTP requests.
- **File Preparation**: To create a file for upload.

---

## Vulnerabilities

- **Vulnerability Type**: Improper Input Validation (CWE-20)
- **Affected Component**: File upload endpoint on the Complaint page
- **Severity Level**: **High**
  - Allows attackers to bypass client-side file type restrictions, potentially leading to execution of malicious files or other abuses.

---

## Risks

- **Business Impact**:
  - **Malicious File Execution**: Uploading unauthorized file types could lead to execution of malicious scripts or binaries on the server.
  - **Security Bypass**: Circumventing validation mechanisms undermines the integrity of the upload process.
  - **Data Loss or Corruption**: Unauthorized file types may interfere with system operations or corrupt data.
  - **Reputational Damage**: Loss of customer trust due to perceived security weaknesses in file handling.

---

## Actions

### Mitigation Strategies
- **Server-Side Validation**: Implement strict server-side validation for file types, ensuring client-side checks cannot be bypassed.
- **Input Sanitization**: Validate and sanitize all user-supplied input, including file extensions and content.
- **Whitelisting**: Use a whitelist of allowed file extensions and reject any uploads that do not match.

### Remediation Fixes
- **Secure File Handling**: Use libraries or frameworks that enforce file type restrictions on the server-side.
- **Request Inspection**: Inspect and validate the entire HTTP request, including headers and body, to prevent manipulation.
- **Logging and Monitoring**: Maintain detailed logs of file uploads and monitor for anomalies or abuse.

### Best Security Practices
- **Regular Security Audits**: Conduct periodic security audits and penetration tests to identify and address vulnerabilities in file upload processes.
- **Developer Training**: Train developers on secure coding practices, with a focus on input validation and file security.
- **Incident Response Plan**: Develop and maintain an incident response plan to quickly address and mitigate unauthorized file uploads and security breaches.
