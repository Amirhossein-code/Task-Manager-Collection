# ⚖️ Task Manager

### 🔺 Description

The Task Manager is a user-friendly application that helps users efficiently manage their tasks by defining tasks, setting prerequisites, and allocating necessary resources.

### 🔺 Features

- **User Authentication:** Secure login and sign up using email and password credentials.
- **Task Management:** Define tasks based on individual requirements.
- **Prerequisites:** Set task prerequisites for proper sequencing and dependencies.
- **Resource Allocation:** Allocate resources to tasks for smooth execution.
- **Task Privacy:** Keep each user's tasks private and visible only to themselves.

### :accessibility: Authentication

The Task Manager uses a custom authentication backend supporting email and password authentication. It employs JWT authentication with Simple JWT for secure and seamless user authentication.

**🉑 Resetting Password**

- Users initiate password reset by providing their email.
- An email with a reset link is sent to the user's email address.
- Users click the link to enter a new password and reset it.
- Token in the link authenticates the user for password reset.

### ⚙️ Tech Stack Used

**🌀 Backend:** Python, Django, Django Rest Framework, Smtp4dev, Docker, PostgreSQL
