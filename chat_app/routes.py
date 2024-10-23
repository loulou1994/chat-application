from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required

from chat_app import app, db
from chat_app.forms import LoginForm, SignupForm
from chat_app.models import User

@app.route('/', methods=['GET', 'POST'])
def home():
    if current_user.is_authenticated:
        return redirect(url_for('chat'))

    form = LoginForm()

    if form.validate_on_submit():
        query_user = db.select(User).filter_by(email=form.email.data)
        user = db.session.execute(query_user).first()

        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password', category='info')
            return redirect(url_for('home'))

        login_user(user)
        return redirect(url_for('chat'))
    
    if form.errors != {}:
        error_string = form.formatErrorString(
            'Error occured during validation with the following fields: ')
        flash(error_string, category='danger')

    return render_template('index.html', form=form)


@app.route('/signup', methods=["GET", "POST"])
def signup():
    form = SignupForm()

    if form.validate_on_submit():
        
        pass

    return render_template('signup.html', form=form)


@app.route('/chat')
@login_required
def chat():
    return render_template('chat.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

# @socketio.on("my event")
# def handle_envt(data):
#     print(f'received json: {str(data)}')
