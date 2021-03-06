from flask import Flask, jsonify, request, render_template, redirect, session, flash
from models import connect_db, db, User
from forms import UserForm, LoginForm
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///users"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"

connect_db(app)
db.create_all()


@app.route('/')
def show_home():
    return redirect('/register')


@app.route('/register', methods=['GET', 'POST'])
def register_user():
    form = UserForm()
    form.username.label.text = 'Username'
    form.password.label.text = 'Password'
    form.email.label.text = 'Email'
    form.first_name.label.text = 'First name'
    form.last_name.label.text = 'Last name'

    if form.validate_on_submit():
        username = form.username.data

        password = form.password.data

        email = form.email.data

        first_name = form.first_name.data

        last_name = form.last_name.data

        new_user = User.register(
            username, password, email, first_name, last_name)

        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append('Username taken.  Please pick another')
            return render_template('register.html', form=form)
        session['user_id'] = new_user.username
        flash('Welcome! Successfully Created Your Account!', "success")
        return redirect('/secret')
    # import pdb
    # pdb.set_trace()
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_user():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            flash(f"Welcome Back, {user.username}!")
            session['user_id'] = user.username
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors = ['Invalid username/password.']

    return render_template('login.html', form=form)


@app.route('/users/<username>')
def show_secret(username):
    user = User.query.get_or_404(username)
    if session.get('user_id'):
        return render_template('user.html', user=user)
    return redirect('/')


@app.route('/logout')
def logout_user():
    session.pop('user_id')
    flash("Bye")
    return redirect('/')
