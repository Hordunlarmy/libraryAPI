<picture> <source media="(prefers-color-scheme: dark)" srcset="https://i.imgur.com/6OBbKFo.jpeg"> <source media="(prefers-color-scheme: light)" srcset="https://i.imgur.com/6OBbKFo.jpeg"> <img alt="README image" src="https://i.imgur.com/6OBbKFo.jpeg"> </picture>

# Library Management System

## Overview

This project consists of two independent API services designed to manage a library's book catalog and user interactions. The application is dockerized for ease of deployment and consistent environments.

## Table of Contents

- [Introduction](#introduction)
- [Frontend API](#frontend-api)
- [Backend/Admin API](#backendadmin-api)
- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Testing](#testing)

## Introduction

The Library Management System comprises two separate APIs:

1. **Frontend API**: For user-facing functionalities, including browsing books and borrowing them.
2. **Backend/Admin API**: For administrative tasks like managing the book catalog and user data.

## Frontend API

The Frontend API allows users to:

- **Enroll**: Register a new user with their email, first name, and last name.
- **List All Books**: Retrieve a list of all available books.
- **Get Book by ID**: Fetch details of a specific book using its ID.
- **Filter Books**: Search for books based on:
  - Publisher (e.g., Wiley, Apress, Manning)
  - Category (e.g., Fiction, Technology, Science)
- **Borrow Books**: Borrow a book by its ID and specify the borrowing period in days.

## Backend/Admin API

The Backend/Admin API enables administrators to:

- **Add New Books**: Insert new books into the catalog.
- **Remove Books**: Delete books from the catalog.
- **List Users**: Retrieve a list of all users enrolled in the library.
- **List Users and Borrowed Books**: Fetch details of users and the books they have borrowed.
- **List Unavailable Books**: Show books that are currently borrowed and when they will be available again.

## Installation

### Prerequisites

- Docker
- Docker Compose

### Clone the Repository

```bash
git clone https://github.com/Hordunlarmy/libraryAPI
cd libraryAPI
docker compose up --build -d
```

## Usage

- **Frontend API**: Accessible at `http://cowrywise.hordun.tech:8001/`
- **Backend/Admin API**: Accessible at `http://cowrywise.hordun.tech:8002/`

### Frontend API Endpoints

- **Enroll**: `POST /api/users/enroll`

  - **Request Body**:
    ```json
    {
      "email": "user@example.com",
      "first_name": "John",
      "last_name": "Doe"
    }
    ```

- **List All Books**: `GET /api/books`

  - **Query Parameters**: None

- **Get Book by ID**: `GET /api/books/{id}`

  - **Path Parameter**:
    - `id`: The ID of the book.

- **Filter Books**: `GET /api/books/filter`

  - **Query Parameters**:
    - `publisher`: Filter books by publisher (e.g., Wiley, Apress, Manning).
    - `category`: Filter books by category (e.g., Fiction, Technology, Science).

- **Borrow Books**: `POST /api/borrow`
  - **Request Body**:
    ```json
    {
      "book_id": "book_id_here",
      "user_id": "user_id here",
      "borrow_days": 7
    }
    ```

### Backend/Admin API Endpoints

- **Add New Books**: `POST /api/books`

  - **Request Body**:
    ```json
    {
      "title": "Book Title",
      "author": "Author Name",
      "publisher": "Publisher Name",
      "category": "Category"
    }
    ```

- **Remove Books**: `DELETE /api/books/{id}`

  - **Path Parameter**:
    - `id`: The ID of the book to be removed.

- **List Users**: `GET /api/users`

  - **Query Parameters**: None

- **List Users and Borrowed Books**: `GET /api/users/books`

  - **Query Parameters**: None

- **List Unavailable Books**: `GET /api/books/unavailable`
  - **Query Parameters**: None

## API Documentation

API documentation is available at:

[<img src="https://run.pstmn.io/button.svg" alt="Run In Postman" style="width: 128px; height: 32px;">](https://documenter.getpostman.com/view/34544809/2sAXqs6Mip)

## Testing

To run tests, use the following command:

```bash
docker-compose exec frontend pytest
docker-compose exec backend pytest
```
