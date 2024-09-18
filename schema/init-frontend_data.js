db = db.getSiblingDB('frontend_db');

db.createCollection('Books');
db.Users.createIndex({ email: 1 }, { unique: true });
db.Books.createIndex({ title: 1, author: 1 }, { unique: true });
db.BorrowedBooks.createIndex({ book_id: 1 }, { unique: true });

db.Books.insertMany([
  {
    title: 'Clean Code',
    author: 'Robert C. Martin',
    publisher: 'Prentice Hall',
    category: 'Technology',
    is_borrowed: false,
    created_at: ISODate(),
  },
  {
    title: 'The Pragmatic Programmer',
    author: 'Andrew Hunt',
    publisher: 'Addison-Wesley',
    category: 'Technology',
    is_borrowed: false,
    created_at: ISODate(),
  },
  {
    title: 'Harry Potter and the Sorcerers Stone',
    author: 'J.K. Rowling',
    publisher: 'Bloomsbury',
    category: 'Fiction',
    is_borrowed: false,
    created_at: ISODate(),
  },
  {
    title: 'A Brief History of Time',
    author: 'Stephen Hawking',
    publisher: 'Bantam Books',
    category: 'Science',
    is_borrowed: false,
    created_at: ISODate(),
  },
  {
    title: 'Deep Learning',
    author: 'Ian Goodfellow',
    publisher: 'MIT Press',
    category: 'Technology',
    is_borrowed: false,
    created_at: ISODate(),
  },
]);
