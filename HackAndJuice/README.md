# HackAndJuice

Write-ups documenting the resolution of challenges from **OWASP Juice Shop**, a deliberately insecure web application maintained by the OWASP Foundation and widely used as a benchmark for web application security training. It simulates a realistic e-commerce platform (product catalog, shopping basket, user accounts, admin panel, REST API) in which every component contains a deliberate vulnerability.

## Scope

Challenges are grouped by OWASP Top 10-aligned vulnerability categories, including:

- **Injection** (SQL, NoSQL)
- **Broken Authentication**
- **Broken Access Control**
- **Cross-Site Scripting (XSS)**
- **XML External Entities (XXE)**
- **Sensitive Data Exposure**
- **Cryptographic Issues**
- **Improper Input Validation**
- **Vulnerable Components**
- **Broken Anti-Automation**
- **Unvalidated Redirects**
- **Security through Obscurity**

Juice Shop rates each challenge with a difficulty score from 1 to 6 stars. File names follow the convention `Category-Difficulty-ChallengeName.md`.

## Structure

- Each `.md` file documents one challenge: the vulnerability analyzed, the methodology used to identify and exploit it, and the steps taken to capture the flag.
- The `images/` folder contains supporting screenshots referenced in the write-ups.
- The `to validate/` folder holds write-ups that are still being reviewed or refined.

## Methodology

Each write-up generally follows a consistent structure: reconnaissance, source code or application analysis, exploitation, and verification. Where relevant, source code review of the [public Juice Shop repository](https://github.com/juice-shop/juice-shop) was used to confirm the root cause of a vulnerability rather than relying on black-box testing alone.
