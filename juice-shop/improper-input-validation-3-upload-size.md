## Methodology

1. **Initial Setup**
   - Navigated to the Complaint page and prepared a legitimate `.zip` or `.pdf` file slightly under the 100KB limit (e.g., 99KB).
   - Filled in a dummy message in the text input field to complete the form.

2. **Intercepting the Upload Request**
   - Started **Burp Suite Interceptor** to capture the HTTP POST request generated upon form submission.
   - Submitted the form and intercepted the request to analyze its structure.

3. **Manipulating the File Size**
   - Identified the file data within the POST request.
   - Appended random data to the file content in the intercepted request, increasing its size beyond the 100KB limit.

4. **Executing the Exploit**
   - Forwarded the modified request to the server, bypassing client-side size validation.
   - Confirmed the successful upload of the oversized file, triggering the challenge flag.

### Tools Used
- **Burp Suite**: For intercepting and modifying HTTP requests.
- **File Preparation**: To create a file close to the size limit.

---

## Vulnerabilities

- **Vulnerability Type**: Improper Input Validation (CWE-20)
- **Affected Component**: File upload endpoint on the Complaint page
- **Severity Level**: **High**
  - Allows attackers to bypass client-side file size restrictions, potentially leading to denial of service or other abuses.

---

## Risks

- **Business Impact**:
  - **Denial of Service**: Uploading oversized files could exhaust server resources, impacting performance and availability.
  - **Storage Abuse**: Unchecked file uploads may consume excessive storage, increasing operational costs.
  - **Security Bypass**: Circumventing validation mechanisms undermines the integrity of the upload process.
  - **Reputational Damage**: Loss of customer trust due to perceived security weaknesses in file handling.

---

## Actions

### Mitigation Strategies
- **Server-Side Validation**: Implement strict server-side validation for file size and type, ensuring client-side checks cannot be bypassed.
- **Input Sanitization**: Validate and sanitize all user-supplied input, including file content and metadata.
- **Resource Limits**: Enforce hard limits on file sizes and monitor for unusual upload patterns.

### Remediation Fixes
- **Secure File Handling**: Use libraries or frameworks that enforce file size and type restrictions on the server-side.
- **Request Inspection**: Inspect and validate the entire HTTP request, including headers and body, to prevent manipulation.
- **Logging and Monitoring**: Maintain detailed logs of file uploads and monitor for anomalies or abuse.

### Best Security Practices
- **Regular Security Audits**: Conduct periodic security audits and penetration tests to identify and address vulnerabilities in file upload processes.
- **Developer Training**: Train developers on secure coding practices, with a focus on input validation and file security.
- **Incident Response Plan**: Develop and maintain an incident response plan to quickly address and mitigate unauthorized file uploads and security breaches.
