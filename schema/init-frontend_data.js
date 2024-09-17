db = db.getSiblingDB('frontend_db');

db.createCollection('Books');

db.Books.insertMany([
  {
    _id: 1,
    title: 'Clean Code',
    author: 'Robert C. Martin',
    publisher: 'Prentice Hall',
    category: 'Technology',
    is_borrowed: false,
    return_date: null,
  },
  {
    _id: 2,
    title: 'The Pragmatic Programmer',
    author: 'Andrew Hunt',
    publisher: 'Addison-Wesley',
    category: 'Technology',
    is_borrowed: false,
    return_date: null,
  },
  {
    _id: 3,
    title: 'Harry Potter and the Sorcerers Stone',
    author: 'J.K. Rowling',
    publisher: 'Bloomsbury',
    category: 'Fiction',
    is_borrowed: false,
    return_date: null,
  },
  {
    _id: 4,
    title: 'A Brief History of Time',
    author: 'Stephen Hawking',
    publisher: 'Bantam Books',
    category: 'Science',
    is_borrowed: false,
    return_date: null,
  },
  {
    _id: 5,
    title: 'Deep Learning',
    author: 'Ian Goodfellow',
    publisher: 'MIT Press',
    category: 'Technology',
    is_borrowed: false,
    return_date: null,
  },
]);
