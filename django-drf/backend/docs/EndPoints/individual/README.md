# Individual API Documentation

## Overview

The Individual API provides endpoints for managing user profiles. It allows authenticated users to retrieve and update their individual profile information. The creation of profiles is managed by the system and is not exposed through this API.

## Endpoints

### 1. List Individuals

- **URL:** `/profile/individual/`
- **Method:** `GET`
- **Permissions:** Authenticated users only.
- **Description:** Retrieves a list of individual profiles associated with the authenticated user.
- **Response:** Returns a list of individual profiles in JSON format.
- **Response Code:** 200 OK

### 2. Retrieve Individual Profile

- **URL:** `/profile/individual/{id}/`
- **Method:** `GET`
- **Permissions:** Authenticated users only.
- **Description:** Retrieves the details of a specific individual profile based on the provided `id`.
- **Response:** Returns the individual profile details in JSON format.
- **Response Codes:**
  - **200 OK:** Successful retrieval.
  - **404 Not Found:** If the profile does not exist or does not belong to the authenticated user.

### 3. Update Individual Profile

- **URL:** `/profile/individual/{id}/`
- **Method:** `PUT`
- **Permissions:** Authenticated users only; the user must be the profile owner.
- **Description:** Updates the details of a specific individual profile.
- **Request Body:** Requires a JSON payload conforming to the `UpdateIndividualSerializer` schema.
- **Response Codes:**
  - **200 OK:** Returns the updated individual profile in JSON format.
  - **400 Bad Request:** If the request body is invalid.
  - **403 Forbidden:** If the authenticated user is not the owner of the profile.
 - **404 Not Found:** If the profile does not exist.
