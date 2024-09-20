# App Endpoints Documentation

The Task API provides endpoints for managing tasks associated with individual user profiles. Authenticated users can create, retrieve, update, and delete their tasks, ensuring that each task is tied to the correct user.

## Table of contents

- [Task Endpoints](#task-endpoints)
- [Category Endpoints](#category-endpoints)

## Task Endpoints

### 1. List Tasks

- **URL:** `/app/tasks/`
- **Method:** `GET`
- **Permissions:** Authenticated users only.
- **Description:** Retrieves a list of tasks associated with the authenticated user's profile.
- **Response:** Returns a list of tasks in JSON format.
- **Response Codes:**
  - **200 OK:** Successful retrieval.

### 2. Create Task

- **URL:** `/app/tasks/`
- **Method:** `POST`
- **Permissions:** Authenticated users only.
- **Description:** Creates a new task associated with the authenticated user's profile.
- **Request Body:** Requires a JSON payload conforming to the `CreateTaskSerializer` schema.
- **Response Codes:**
  - **201 Created:** Returns the created task in JSON format.
  - **400 Bad Request:** If the request body is invalid.

### 3. Retrieve Task

- **URL:** `/app/tasks/{id}/`
- **Method:** `GET`
- **Permissions:** Authenticated users only.
- **Description:** Retrieves the details of a specific task based on the provided `id`.
- **Response:** Returns the task details in JSON format.
- **Response Codes:**
  - **200 OK:** Successful retrieval.
  - **404 Not Found:** If the task does not exist or does not belong to the authenticated user.

### 4. Update Task

- **URL:** `/app/tasks/{id}/`
- **Method:** `PATCH`
- **Permissions:** Authenticated users only; the user must be the task owner.
- **Description:** Updates the details of a specific task. Only fields specified in the request body will be updated.
- **Request Body:** Requires a JSON payload conforming to the `TaskSerializer` schema.
- **Response Codes:**
  - **200 OK:** Returns the updated task in JSON format.
  - **400 Bad Request:** If the request body is invalid.
  - **404 Not Found:** If the task does not exist or does not belong to the authenticated user.

### 5. Update Task (Full Update)

- **URL:** `/tasks/{id}/`
- **Method:** `PUT`
- **Permissions:** Authenticated users only; the user must be the task owner.
- **Description:** Replaces the entire task with the provided `id` with the new data.
- **Request Body:** Requires a JSON payload conforming to the `TaskSerializer` schema.
- **Response Codes:**
  - **200 OK:** Returns the updated task in JSON format.
  - **400 Bad Request:** If the request body is invalid.
  - **404 Not Found:** If the task does not exist or does not belong to the authenticated user.

### 6. Delete Task

- **URL:** `/app/tasks/{id}/`
- **Method:** `DELETE`
- **Permissions:** Authenticated users only; the user must be the task owner.
- **Description:** Deletes a specific task based on the provided `id`.
- **Response Codes:**
  - **204 No Content:** Successful deletion, no content returned.
  - **404 Not Found:** If the task does not exist or does not belong to the authenticated user.

## Category Endpoints

### 1. List Categories

- **URL:** `/app/categories/`
- **Method:** `GET`
- **Permissions:** Authenticated users only.
- **Description:** Retrieves a list of categories associated with the authenticated user's profile.
- **Response:** Returns a list of categories in JSON format.
- **Response Codes:**
  - **200 OK:** Successful retrieval.

### 2. Create Category

- **URL:** `/app/categories/`
- **Method:** `POST`
- **Permissions:** Authenticated users only.
- **Description:** Creates a new category associated with the authenticated user's profile.
- **Request Body:** Requires a JSON payload conforming to the `CategorySerializer` schema.
- **Response Codes:**
  - **201 Created:** Returns the created category in JSON format.
  - **400 Bad Request:** If the request body is invalid.

### 3. Retrieve Category

- **URL:** `/app/categories/{id}/`
- **Method:** `GET`
- **Permissions:** Authenticated users only.
- **Description:** Retrieves the details of a specific category based on the provided `id`.
- **Response:** Returns the category details in JSON format.
- **Response Codes:**
  - **200 OK:** Successful retrieval.
  - **404 Not Found:** If the category does not exist or does not belong to the authenticated user.

### 4. Update Category (Partial Update)

- **URL:** `/app/categories/{id}/`
- **Method:** `PATCH`
- **Permissions:** Authenticated users only; the user must be the category owner.
- **Description:** Updates the details of a specific category. Only fields specified in the request body will be updated.
- **Request Body:** Requires a JSON payload conforming to the `CategorySerializer` schema.
- **Response Codes:**
  - **200 OK:** Returns the updated category in JSON format.
  - **400 Bad Request:** If the request body is invalid.
  - **404 Not Found:** If the category does not exist or does not belong to the authenticated user.

### 5. Update Category (Full Update)

- **URL:** `/app/categories/{id}/`
- **Method:** `PUT`
- **Permissions:** Authenticated users only; the user must be the category owner.
- **Description:** Replaces the entire category with the provided `id` with the new data.
- **Request Body:** Requires a JSON payload conforming to the `CategorySerializer` schema.
- **Response Codes:**
  - **200 OK:** Returns the updated category in JSON format.
  - **400 Bad Request:** If the request body is invalid.
  - **404 Not Found:** If the category does not exist or does not belong to the authenticated user.

### 6. Delete Category

- **URL:** `/app/categories/{id}/`
- **Method:** `DELETE`
- **Permissions:** Authenticated users only; the user must be the category owner.
- **Description:** Deletes a specific category based on the provided `id`.
- **Response Codes:**
  - **204 No Content:** Successful deletion, no content returned.
  - **404 Not Found:** If the category does not exist or does not belong to the authenticated user.
