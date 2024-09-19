db = db.getSiblingDB('frontend_db');

db.createCollection('Books');
db.Users.createIndex({ email: 1 }, { unique: true });
db.Books.createIndex({ title: 1, author: 1 }, { unique: true });
db.BorrowedBooks.createIndex({ book_id: 1 }, { unique: true });

db.Books.insertMany([
  {
    _id: 'f32c1dac-5d38-46b1-aa89-be8ed3534c90',
    title: 'Clean Code',
    author: 'Robert C. Martin',
    publisher: 'Prentice Hall',
    category: 'Technology',
    is_borrowed: false,
    created_at: ISODate(),
  },
  {
    _id: '5af948fa-0dc5-474b-8678-546ce76f2dff',
    title: 'The Pragmatic Programmer',
    author: 'Andrew Hunt',
    publisher: 'Addison-Wesley',
    category: 'Technology',
    is_borrowed: false,
    created_at: ISODate(),
  },
  {
    _id: 'c13eb1e4-e1b7-4217-b9a8-d99f7a00e326',
    title: 'Harry Potter and the Sorcerers Stone',
    author: 'J.K. Rowling',
    publisher: 'Bloomsbury',
    category: 'Fiction',
    is_borrowed: false,
    created_at: ISODate(),
  },
  {
    _id: '00b43d16-c1c7-4c2a-8cce-b8084536d635',
    title: 'A Brief History of Time',
    author: 'Stephen Hawking',
    publisher: 'Bantam Books',
    category: 'Science',
    is_borrowed: false,
    created_at: ISODate(),
  },
  {
    _id: '54242adc-58d9-4eed-97d2-72605088f93a',
    title: 'Deep Learning',
    author: 'Ian Goodfellow',
    publisher: 'MIT Press',
    category: 'Technology',
    is_borrowed: false,
    created_at: ISODate(),
  },
]);
