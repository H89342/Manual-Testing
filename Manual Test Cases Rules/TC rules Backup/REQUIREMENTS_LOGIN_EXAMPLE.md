# REQUIREMENTS_EXAMPLE.md
> Complete filled-in example of a requirements file for the Login module.
> Use this as a reference when completing your own requirements file.

---

# Requirements: Login

| Field       | Value                          |
|-------------|--------------------------------|
| Module      | Login                          |
| TC Prefix   | AUTH                           |
| Author      | Hang LT                        |
| Date        | 2026-04-20                     |
| Version     | 1.0                            |
| Source      | JIRA-1012 / Figma: Login v3    |
| Status      | Ready for TC Generation        |

### Environment & Constraints

```
Environment: Web

Web browsers:
  - Chrome 120+
  - Firefox 121+
  - Safari 17+

Special constraints:
  - Staging environment only
  - Account lockout resets after 30 minutes
```

### Test Data

```
valid_user_email:     testuser@demo.com
valid_user_password:  TestPass123!
locked_user_email:    locked@demo.com
unregistered_email:   notexist@demo.com
```

### Out of Scope

```
- Social login (Google / Facebook OAuth) — tracked in AUTH-v2
- Admin login — covered in ADMIN module
- Password reset flow — covered in RESET module
```

### Functional Requirements

```
FR-001: User can log in with valid email and password and is redirected to /dashboard.
FR-002: System must display inline error "Invalid email or password" for wrong credentials.
FR-003: System must lock the account and display "Account locked. Contact support." after 5 failed attempts.
FR-004: Email field must reject input without "@" and a domain and show "Enter a valid email address".
FR-005: Password field must be masked by default with a show/hide toggle.
FR-006: "Forgot password" link must redirect to /reset-password.
FR-007: Pressing Enter on the password field must submit the form.
FR-008: POST /api/auth/login must return HTTP 200 and Bearer token on success.
FR-009: POST /api/auth/login must return HTTP 401 with { "error": "Invalid credentials" } on failure.
```

### Non-Functional Requirements

```
NFR-001: Login page must load within 2 seconds on a standard 4G connection.
NFR-002: Error messages must not reveal whether the email is registered in the system.
```

### Acceptance Criteria

```
Given the user is on /login with a valid account
When  they enter correct email and password and click Sign In
Then  they are redirected to /dashboard and a session cookie is set

Given the user enters an incorrect password 5 times
When  they attempt a 6th login
Then  the account is locked and "Account locked. Contact support." is displayed

Given the user submits the login form with an empty email field
When  the form validates
Then  inline error "Email is required" appears below the email field
```

### References

| Type        | Link / Reference                              |
|-------------|-----------------------------------------------|
| Ticket      | JIRA-1012                                     |
| Design      | Figma: Login v3                               |
| API Docs    | /docs/api/auth                                |
| Previous TC | testcases_login_v1.md                         |
