"""Blogly application."""

from flask import Flask, request, redirect, render_template

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blogly.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'testtest'
app.config['TESTING'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

from flask_debugtoolbar import DebugToolbarExtension
toolbar = DebugToolbarExtension(app)

from models import db, connect_db, User
connect_db(app)
# db.drop_all()
# db.create_all()

users = [
    {
        "id": 1,
        "full_name": "Adam Adam"
    },
    {
        "id": 2,
        "full_name": "Steve Steve"
    }
]

@app.route("/")
def show_home():
    # GET /
    # Redirect to list of users. (We’ll fix this in a later step).
    return redirect("/users")

@app.route("/users")
def show_user_list():
    # GET /users
    # Show all users.
    # Make these links to view the detail page for the user.
    # Have a link here to the add-user form.

    users = User.query.all()
    return render_template('users/users.html', users=users)

@app.route("/users/new")
def show_new_user_form():
    # GET /users/new
    # Show an add form for users

    return render_template('users/new_user_form.html')

@app.route("/users/new", methods=["POST"])
def do_add_new_user():
    # POST /users/new
    # Process the add form, adding a new user and going back to /users

    first_name = request.form['first_name'] if 'first_name' in request.form else None
    last_name = request.form['last_name'] if 'last_name' in request.form else None
    image_url = request.form['image_url'] if 'image_url' in request.form else None

    print(first_name, last_name, image_url)
    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)

    db.session.add(new_user)
    db.session.commit()
    
    return redirect("/users")

@app.route("/users/<int:user_id>")
def show_user_info(user_id):
    # GET /users/[user-id]
    # Show information about the given user.
    # Have buttons to edit the info, delete the user, or show the full list.

    state = "view"
    # user = User.query.get_or_404(user_id)
    user = users[0]
    return render_template('users/edit_user_form.html', user=user, state=state)

@app.route("/users/<int:user_id>/edit")
def show_edit_user_form(user_id):
    # GET /users/[user-id]/edit
    # Have a cancel button that returns to the detail page for a user, and a save button that updates the user.

    state = "edit"
    user = users[0]

    # user = User.query.get_or_404(user_id)
    return render_template('users/edit_user_form.html', user=user, state=state)

@app.route("/users/<int:user_id>/edit", methods=["POST"])
def do_edit_user(user_id):
    # POST /users/[user-id]/edit
    # Process the edit form, returning the user to the /users page.

    user = users[0]
    user.first_name = request.form['first_name'] if 'first_name' in request.form else ""
    user.last_name = request.form['last_name'] if 'last_name' in request.form else ""
    user.image_url = request.form['image_url'] if 'image_url' in request.form else ""

    # db.session.add(user)
    # db.session.commit()

    return redirect("/users")

@app.route("/users/delete", methods=["POST"])
def do_delete_user():
    # POST /users/[user-id]/delete
    # Delete the user.

    # user = User.query.get_or_404(user_id)
    # db.session.delete(user)
    # db.session.commit()

    return redirect("/users")

@app.route("/users/<int:user_id>/delete", methods=["POST"])
def do_delete_user2(user_id):
    # POST /users/[user-id]/delete
    # Delete the user.

    # user = User.query.get_or_404(user_id)
    # db.session.delete(user)
    # db.session.commit()

    return redirect("/users")
