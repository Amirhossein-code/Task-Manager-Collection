# Authentication API Documentation

The Authentication API provides endpoints for user registration and token management. It allows users to obtain JWT tokens for secure access to protected resources and to register new accounts.

## Table of Contents

- [Token Endpoints](#token-endpoints)
- [Registration Endpoint](#registration-endpoint)
- [Password Reset Endpoint](#password-reset-endpoint)

## Token Endpoints

### 1. Obtain Token

- **URL:** `/auth/token/`
- **Method:** `POST`
- **Permissions:** No authentication required.
- **Description:** Obtains a JWT token for an authenticated user. The user must provide valid credentials (username and password).
- **Request Body:**
  ```json
  {
    "email": "user_email",
    "password": "user_password"
  }
  ```
- **Response Codes:**
  - **200 OK:** Returns the access and refresh tokens.
  - **401 Unauthorized:** If the credentials are invalid.

### 2. Refresh Token

- **URL:** /auth/token/refresh/
- **Method:** POST
- **Permissions:** Requires a valid refresh token.
- **Description:** Refreshes the access token using the provided refresh token.
- **Request Body:**

```json
{
  "refresh": "your_refresh_token"
}
```

- **Response Codes:**
  - **200 OK:** Returns a new access token.
  - **401 Unauthorized:** If the refresh token is invalid or expired.

## Registration Endpoint

### 1. Register User

- **URL:** /auth/register/
- **Method:** POST
- **Permissions:** No authentication required.
- **Description:** Registers a new user account. The user must provide a username and password, along with any other required fields defined in the UserSerializer.
- **Request Body:**

```json
  {
  "email": "user@example.com"
  "password": "new_password",
  }
```

- **Response Codes:**
  - **201 Created:** Returns the details of the newly created user.
  - **400 Bad Request:** If the request data is invalid.

## Password Reset Endpoint

### 1. Request Password Reset

- **URL:** /auth/reset-password/
- **Method:** POST
- **Permissions:** No authentication required.
- **Description:** Allows a registered user to request a password reset. The user must provide their registered email address. If the email is found, a password reset link containing a token will be sent to the user.
- **Request Body:**
  ```json
  {
    "email": "user@example.com"
  }
  ```
- **Response Codes:**
  - **200 OK:** A message indicating that the password reset link has been sent.
  - **404 Not Found:** If no user with the given email is registered.

## Reset Password Endpoint

### 2. Reset Password

- **URL:** /auth/reset-password/<token>/
- **Method:** POST
- **Permissions:** No authentication required.
- **Description:** This endpoint is used to reset the password after the user clicks the link sent to their email. The token must be provided in the URL, and the new password must be included in the request body.
- **Request Body:**

```json
{
  "password": "new_secure_password"
}
```

- **Response Codes:**
  - **200 OK:** A message indicating that the password has been reset successfully.
  - **400 Bad Request:** If the token is invalid or expired.
