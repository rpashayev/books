from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import user, book

@app.route('/books')
def show_books():
    books = book.Book.show_all_books()
    return render_template('books.html', all_books=books)

@app.route('/books/new', methods=['POST'])
def add_book():
    book.Book.save_book(request.form)
    return redirect('/books')

@app.route('/books/<int:book_id>')
def one_book(book_id):
    id = {
        'id': book_id
    }
    one_book = book.Book.show_one_book(id)
    all_users = user.User.show_unfav_users(id)
    return render_template('one_book.html', book = one_book, users = all_users)

@app.route('/books/edit', methods=['POST'])
def add_user_to_book():
    user.User.save_favorite(request.form)
    return redirect('/books/'+request.form['book_id'])
