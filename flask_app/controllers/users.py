from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import book, user

@app.route('/')
def index():
    return redirect('/users')

@app.route('/users')
def show_users():
    users = user.User.show_all_users()
    return render_template('users.html', all_users=users)

@app.route('/users/new', methods=['POST'])
def add_user():
    user.User.save_user(request.form)
    return redirect('/')

@app.route('/users/<int:user_id>')
def one_user(user_id):
    id = {
        'id': user_id
    }
    one_user = user.User.show_one_user(id)
    all_books = book.Book.show_unfav_books(id)
    return render_template('one_user.html', user=one_user, books = all_books)

@app.route('/users/edit', methods=['POST'])
def add_book_to_user():
    user.User.save_favorite(request.form)
    return redirect('/users/'+request.form['user_id'])
