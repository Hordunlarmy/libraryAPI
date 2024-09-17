----------------------------------------------------
--  Backend/Admin Database Initialization
----------------------------------------------------
CREATE DATABASE IF NOT EXISTS backend_db;
USE backend_db;

CREATE TABLE IF NOT EXISTS Admins (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS Users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(255) UNIQUE NOT NULL,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS Books (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    publisher VARCHAR(255),
    category VARCHAR(255),
    is_borrowed BOOLEAN DEFAULT FALSE,
    return_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS BorrowedBooks (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    book_id INT NOT NULL,
    borrow_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    return_date TIMESTAMP NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE,
    FOREIGN KEY (book_id) REFERENCES Books(id) ON DELETE CASCADE
);

-- Indices to improve query performance
CREATE INDEX idx_books_title ON Books(title);
CREATE INDEX idx_books_author ON Books(author);
CREATE INDEX idx_books_publisher ON Books(publisher);
CREATE INDEX idx_books_category ON Books(category);
