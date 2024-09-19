------------------------------------------------
--    Backend/Admin Database Data Population
------------------------------------------------
USE backend_db;

INSERT INTO Books (id, title, author, publisher, category) VALUES 
('f32c1dac-5d38-46b1-aa89-be8ed3534c90', 'Clean Code', 'Robert C. Martin', 'Prentice Hall', 'Technology'),
('5af948fa-0dc5-474b-8678-546ce76f2dff', 'The Pragmatic Programmer', 'Andrew Hunt', 'Addison-Wesley', 'Technology'),
('c13eb1e4-e1b7-4217-b9a8-d99f7a00e326', 'Harry Potter and the Sorcerers Stone', 'J.K. Rowling', 'Bloomsbury', 'Fiction'),
('00b43d16-c1c7-4c2a-8cce-b8084536d635', 'A Brief History of Time', 'Stephen Hawking', 'Bantam Books', 'Science'),
('54242adc-58d9-4eed-97d2-72605088f93a', 'Deep Learning', 'Ian Goodfellow', 'MIT Press', 'Technology');
