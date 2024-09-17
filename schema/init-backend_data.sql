------------------------------------------------
--    Backend/Admin Database Data Population
------------------------------------------------
USE backend_db;

-- Insert sample admins into Backend Admins table
INSERT INTO Admins (username, email) VALUES ('hordun', 'hordun@admin');

-- Insert sample books into Backend Books table
INSERT INTO Books (title, author, publisher, category, is_borrowed) VALUES 
('Clean Code', 'Robert C. Martin', 'Prentice Hall', 'Technology', FALSE),
('The Pragmatic Programmer', 'Andrew Hunt', 'Addison-Wesley', 'Technology', FALSE),
('Harry Potter and the Sorcerer\'s Stone', 'J.K. Rowling', 'Bloomsbury', 'Fiction', FALSE),
('A Brief History of Time', 'Stephen Hawking', 'Bantam Books', 'Science', FALSE),
('Deep Learning', 'Ian Goodfellow', 'MIT Press', 'Technology', FALSE);
