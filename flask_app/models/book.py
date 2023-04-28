from flask_app.config.mysqlconnector import connectToMySQL
from flask_app.models import user

class Book:
    DB = 'books_schema'
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.pages = data['num_of_pages']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
        self.users = []
    
    @classmethod
    def show_all_books(cls):
        all_books = []
        query = '''
            SELECT *
            FROM books;
        '''
        result = connectToMySQL(cls.DB).query_db(query)
        for book in result:
            all_books.append(cls(book))
        return all_books
    
    @classmethod
    def show_one_book(cls, data):
        query = '''
            SELECT *
            FROM books
            LEFT JOIN favorites ON favorites.book_id = books.id
            LEFT JOIN users ON users.id = favorites.user_id
            WHERE books.id = %(id)s;
        '''
        results = connectToMySQL(cls.DB).query_db(query, data)
        book = cls(results[0])
        
        for row in results:
            user_info = {
                'id': row['users.id'],
                'name': row['name'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
            }
            book.users.append(user.User(user_info))
        return book
    
    @classmethod
    def show_unfav_books(cls, data):
        unfav_books = []
        query = '''
            SELECT *
            FROM books
            WHERE books.id NOT IN (
                SELECT book_id
                FROM favorites
                WHERE user_id = %(id)s
                );
        '''
        result = connectToMySQL(cls.DB).query_db(query, data)
        for book in result:
            unfav_books.append(cls(book))
        return unfav_books
    
    @classmethod
    def save_book(cls, data):
        query = '''
            INSERT INTO books
            (title, num_of_pages)
            VALUES ( %(title)s, %(pages)s)
        '''
        
        return connectToMySQL(cls.DB).query_db(query, data)
    
