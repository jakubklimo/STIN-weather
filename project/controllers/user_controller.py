from flask import Blueprint, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, EqualTo
from ..service.cookies import create_secure_cookie, read_secure_cookie, delete_secure_cookie, get_user
from ..models.users import db as users_db, User

user_bp = Blueprint('user', __name__)

class LoginForm(FlaskForm):
    user = StringField("User", validators=[InputRequired()], render_kw={"placeholder": "User"})
    password = PasswordField("Password", validators=[InputRequired()], render_kw={"placeholder": "Password"})
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    user = StringField("Uživatelské jméno", validators=[InputRequired()], render_kw={"placeholder": "User"})
    password = PasswordField("Heslo", validators=[InputRequired()], render_kw={"placeholder": "Password"})
    confirm_password = PasswordField("Potvrzení hesla", validators=[InputRequired(), EqualTo('password', message='Hesla se neshodují.')], render_kw={"placeholder": "Confirm password"})
    submit = SubmitField("Register")

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = None

    #Když je formulář správně vyplněn najde se v db uživatel se zadaným jménem, když uživatel existuje a je správné heslo vytvoří se cookie
    if request.method == 'POST':
        if form.validate_on_submit():
            user = get_user(form.user.data)
            if user and user.check_password(form.password.data):
                return create_secure_cookie(user.name)
            else:
                error = 'Neplatné jméno nebo heslo'

    return render_template('login.html', form=form, error=error)

@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    error = None

    #Když je formulář validní a když uživatel s tímto jménem neexistuje vytvoří se nový uživatel
    if form.validate_on_submit():
        if not get_user(form.user.data):
            new_user = User(name=form.user.data, password=form.password.data)
            try:
                users_db.session.add(new_user)
                users_db.session.commit()
            except Exception as e:
                users_db.session.rollback()
                error = "Nepodařilo se zaregistrovat uživatele"
                return render_template('register.html', form=form, error=error)
            return create_secure_cookie(form.user.data)
        else:
            error = 'Uživatel již existuje'

    return render_template('register.html', form=form, error=error)

@user_bp.route('/logout')
def logout():
    return delete_secure_cookie()