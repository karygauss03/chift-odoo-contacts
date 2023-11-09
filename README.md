# chift-odoo-contacts

## Overview

This project aims to develop a synchronization script for managing contacts in the Odoo environment. The script is responsible for inserting new contacts, updating changed existing contacts, and deleting removed contacts in a Postgres database. Additionally, two secure APIs are implemented for interacting with the database: one for retrieving the list of existing contacts and another for getting a contact by ID. Authentication for these APIs is handled through JWT tokens, with a provided create user API and login API to generate tokens.

## Technologies Used

- FastAPI framework
- Postgres database

## API Endpoints

### 1. Login API

- **Path**: `/login` (POST Method)
- **Description**: Authenticates the user and generates a JWT token.
- **Request Body**:

  ```json
  {
    "username": "your_email",
    "password": "your_password"
  }
- **Response**:

    ```json
        {
            "access_token": "ACCESS_TOKEN",
            "token_type": "bearer"
        }
    ```

### 2. Create User API

- **Path**: `/user` (POST Method)
- **Description**: Creates a new user for authentication.
- **Request Body**:

  ```json
  {
    "email": "new_email",
    "password": "new_password"
  }
  ````

- **Response Body**:

    ```json
    {
        "id": "new_id",
        "email": "new_email",
        "message": "User created successfully!",
        "status": 201
    }
    ```

### 3. Get Contacts API

- **Path**: `/contacts/` (GET Method)
- **Description**: Retrieves the list of existing contacts.
- **Authentication**: Requires a valid JWT token.

### 4. Get Contact by ID API

- **Path**: `/contacts/{id}` (GET Method)
- **Description**: Retrieves a contact by ID.
- **Authentication**: Requires a valid JWT token.
