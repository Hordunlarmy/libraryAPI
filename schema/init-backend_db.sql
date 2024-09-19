----------------------------------------------------
--  Backend/Admin Database Initialization
----------------------------------------------------
CREATE DATABASE IF NOT EXISTS backend_db;
USE backend_db;

CREATE TABLE IF NOT EXISTS Users (
    id CHAR(36) PRIMARY KEY NOT NULL UNIQUE,
    email VARCHAR(255) UNIQUE NOT NULL,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS Books (
    id CHAR(36) PRIMARY KEY NOT NULL UNIQUE,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    publisher VARCHAR(255),
    category VARCHAR(255),
    is_borrowed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (title, author)
);

CREATE TABLE IF NOT EXISTS BorrowedBooks (
    id CHAR(36) PRIMARY KEY NOT NULL UNIQUE,
    user_id CHAR(36) NOT NULL,
    book_id CHAR(36) NOT NULL,
    borrow_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    return_date TIMESTAMP NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE,
    FOREIGN KEY (book_id) REFERENCES Books(id) ON DELETE CASCADE,
    UNIQUE (user_id, book_id)
);

-- Indexes for Books table
CREATE INDEX idx_books_title ON Books(title);
CREATE INDEX idx_books_author ON Books(author);
CREATE INDEX idx_books_publisher ON Books(publisher);
CREATE INDEX idx_books_category ON Books(category);

