from flask_app.config.mysqlconnector import connectToMySQL
from flask_app.models import book


class User:
    DB = 'books_schema'
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
        self.books = []

    @classmethod
    def show_all_users(cls):
        all_users = []
        query = '''
            SELECT *
            FROM users;
        '''
        result = connectToMySQL(cls.DB).query_db(query)
        for user in result:
            all_users.append(cls(user))
        return all_users
    
    @classmethod
    def show_one_user(cls, data):
        query = '''
            SELECT *
            FROM users
            LEFT JOIN favorites ON favorites.user_id = users.id
            LEFT JOIN books ON books.id = favorites.book_id
            WHERE users.id = %(id)s;
        '''
        results = connectToMySQL(cls.DB).query_db(query, data)
        user = cls(results[0])
        
        for row in results:
            book_info = {
                'id': row['books.id'],
                'title': row['title'],
                'num_of_pages': row['num_of_pages'],
                'created_at': row['books.created_at'],
                'updated_at': row['books.updated_at']
            }
            user.books.append(book.Book(book_info))
        return user

    @classmethod
    def show_unfav_users(cls, data):
        unfav_users = []
        query = '''
            SELECT *
            FROM users
            WHERE users.id NOT IN (
                SELECT user_id
                FROM favorites
                WHERE book_id = %(id)s
                );
        '''
        result = connectToMySQL(cls.DB).query_db(query, data)
        for user in result:
            unfav_users.append(cls(user))
        return unfav_users

    @classmethod
    def save_user(cls, data):
        query = '''
            INSERT INTO users(name)
            VALUES ( %(name)s );
        '''
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def save_favorite(cls, data):
        query = '''
            INSERT INTO favorites(user_id, book_id)
            VALUES ( %(user_id)s, %(book_id)s );
        '''
        return connectToMySQL(cls.DB).query_db(query, data)