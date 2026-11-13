## **Methodology**

1. **Initial Observation**:
   - Inspected the website for potential steganography targets.
   - Focused on the "About Us" page due to the presence of a carousel containing 5 images.

2. **Image Download**:
   - Downloaded the first 4 images without issue.
   - Noticed the 5th image was in PNG format, which was unusual compared to the others.

3. **Steganography Analysis**:
   - Researched tools for extracting hidden data from images.
   - Selected **OpenStego** for its capability to handle PNG files.

4. **Data Extraction**:
   - Used OpenStego to extract hidden data from the 5th PNG image.
   - Successfully extracted a hidden PNG file, revealing the "Pickle Rick" image.
   ![image0](./images/0.png)

---

## **Vulnerabilities**

- **Vulnerability**: **Steganography (CWE-1004: Hidden Functionality)**
- **Affected Component**: Website's "About Us" page image carousel
- **Severity Level**: **Medium**

---

## **Risks**

- **Business Impact**:
  - Hidden data can be used to leak sensitive information or embed malicious payloads.
  - Potential reputational damage if unauthorized data is discovered by third parties.

---

## **Actions**

### **Mitigation Strategies**
- **Image Validation**: Implement server-side validation to detect and block steganography in uploaded images.
- **Content Monitoring**: Regularly scan website images for hidden data using automated tools.

### **Remediation Fixes**
- **Image Format Restrictions**: Enforce strict image format policies (e.g., only allow JPEG for non-transparent images).
- **Metadata Stripping**: Automatically strip metadata and hidden layers from uploaded images.

### **Best Security Practices**
- **User Awareness**: Train staff to recognize and report suspicious image files.
- **Automated Scanning**: Integrate steganography detection tools into the CI/CD pipeline for website updates.

---