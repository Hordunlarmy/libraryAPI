------------------------------------------------
--    Backend/Admin Database Data Population
------------------------------------------------
USE backend_db;

INSERT INTO Books (title, author, publisher, category) VALUES 
('Clean Code', 'Robert C. Martin', 'Prentice Hall', 'Technology'),
('The Pragmatic Programmer', 'Andrew Hunt', 'Addison-Wesley', 'Technology'),
('Harry Potter and the Sorcerers Stone', 'J.K. Rowling', 'Bloomsbury', 'Fiction'),
('A Brief History of Time', 'Stephen Hawking', 'Bantam Books', 'Science'),
('Deep Learning', 'Ian Goodfellow', 'MIT Press', 'Technology');
