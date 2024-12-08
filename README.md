# Library Management System API

This is a simple library management system API built using Flask, SQLAlchemy, JWT Authentication, and Marshmallow for serialization. The system provides functionality for managing books, members, and borrowing records. It uses role-based access control to restrict certain routes to specific users.

## Architecture and Design

- **Framework**: Flask (for the web framework)
- **Database**: SQLite (with SQLAlchemy as the ORM)
- **Authentication**: JSON Web Tokens (JWT) for secure user authentication
- **Serialization**: Marshmallow for data validation and serialization
- **Rate Limiting**: Flask-Limiter to restrict the number of requests
- **Role-Based Access**: Role-based authentication where users can have different roles like `admin`, `librarian`, or `user`

### Key Features

- **Authentication**: Secure authentication using JWT tokens.
- **Role-Based Access Control**: Admins can manage all records, librarians can manage books, and users can borrow books.
- **CRUD Operations**: Ability to create, read, update, and delete books, members, and borrowing records.
- **Rate Limiting**: Requests are rate-limited to avoid abuse.

---

## Setup and Installation

### Prerequisites

1. Python 3.8 or above
2. Pip for installing Python dependencies

### Steps to Set Up

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/library-management-system.git
   cd library-management-system
   ```

2. **Create a Virtual Environment (Optional but Recommended)**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**

   Create a `.env` file in the root directory and add the following variables:

   ```env
   JWT_SECRET=your_jwt_secret_key
   SQLALCHEMY_DATABASE_URI=sqlite:///library.db
   SQLALCHEMY_TRACK_MODIFICATIONS=False
   JWT_ACCESS_TOKEN_EXPIRES=3600
   ```

5. **Initialize the Database**
   Run the application once to create the database and seed the initial roles and admin member.

   ```bash
   python run.py
   ```

6. **Start the Application**
   Run the application with:

   ```bash
   python run.py
   ```

7. The API will be available at `http://127.0.0.1:5000`.

---

## API Endpoints

### 1. **Login**

- **URL**: `/api/auth/login`
- **Method**: `POST`
- **Description**: Authenticate a user and get a JWT token.
- **Request Body**:
  ```json
  {
    "email": "admin@example.com",
    "password": "password"
  }
  ```
- **Response**:
  ```json
  {
    "access_token": "your_jwt_token"
  }
  ```

### 2. **Create a Book**

- **URL**: `/api/books/create`
- **Method**: `POST`
- **Headers**:
  - `Authorization`: `Bearer {your_jwt_token}`
- **Body**:
  ```json
  {
    "title": "The Great Gatsby",
    "rating": 5,
    "author": "F. Scott Fitzgerald",
    "available_copies": 10
  }
  ```
- **Response**:
  ```json
  {
    "id": 1,
    "title": "The Great Gatsby",
    "rating": 5,
    "author": "F. Scott Fitzgerald",
    "available_copies": 10,
    "added_by": 1
  }
  ```

### 3. **Get All Books**

- **URL**: `/api/books/`
- **Method**: `GET`
- **Headers**:
  - `Authorization`: `Bearer {your_jwt_token}`
- **Response**:
  ```json
  {
    "books": [
      {
        "id": 1,
        "title": "The Great Gatsby",
        "rating": 5,
        "author": "F. Scott Fitzgerald",
        "available_copies": 10,
        "added_by": 1
      },
      ...
    ]
  }
  ```

### 4. **Get Borrowed Books**

- **URL**: `/api/borrowed_books/`
- **Method**: `GET`
- **Headers**:
  - `Authorization`: `Bearer {your_jwt_token}`
- **Response**:
  ```json
  {
    "borrowed_books": [
      {
        "book_id": 1,
        "member_id": 1,
        "borrowed_at": "2024-12-08T14:00:00",
        "due_date": "2024-12-22T14:00:00"
      },
      ...
    ]
  }
  ```

### 5. **Create a Member**

- **URL**: `/api/members/`
- **Method**: `POST`
- **Headers**:
  - `Authorization`: `Bearer {your_jwt_token}`
- **Body**:
  ```json
  {
    "username": "john_doe",
    "email": "john.doe@example.com",
    "password": "securepassword123",
    "role_id": 1
  }
  ```
- **Response**:
  ```json
  {
    "id": 1,
    "username": "john_doe",
    "email": "john.doe@example.com",
    "role_id": 1
  }
  ```

---

## Authentication and Authorization

- **JWT Authentication**: Each request that requires authentication should include a valid JWT token in the `Authorization` header.

  Example:

  ```bash
  Authorization: Bearer {your_jwt_token}
  ```
