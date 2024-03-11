from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask import render_template, url_for, redirect, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
from perfect_recipe.models import User
from perfect_recipe.ext.database import db

def init_app(app):
    bcrypt = Bcrypt(app)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "login"

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()

        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()

            if user:
                if bcrypt.check_password_hash(user.password, form.password.data):
                    login_user(user, remember=True)
                    flash('Logado com sucesso!', category='success')
                    return redirect(url_for('index'))
                else:
                    flash('Erro ao tentar fazer login!', category='error')
            else:
                flash('Username não existe!', category='error')

        return render_template('login.html', form=form, user=current_user)


    @app.route('/register', methods=['GET', 'POST'])
    def register():
        form = RegisterForm()

        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data)
            new_user = User(username=form.username.data, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('Conta criada!', category='success')
            return redirect(url_for('login'))
        elif request.method == 'POST':
            flash('Já existe uma conta cadastrada com esse username!', category='error')

        return render_template('register.html', form=form, user=current_user)

    @app.route('/logout', methods=['GET', 'POST'])
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('login'))

class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=50)], render_kw={"class": "form-control","placeholder": "example@email.com"})

    password = PasswordField(validators=[InputRequired(), Length(min=4, max=50)], render_kw={"class": "form-control", "placeholder": "Password"})

    submit = SubmitField("Register", render_kw={"class": "btn btn-primary"})

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username=username.data).first()

        if existing_user_username:
            raise ValidationError("O username já existe, escolha outro")

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=50)], render_kw={"class": "form-control", "placeholder": "example@email.com"})

    password = PasswordField(validators=[InputRequired(), Length(min=4, max=50)], render_kw={"class": "form-control", "placeholder": "Password"})

    submit = SubmitField("Login", render_kw={"class": "btn btn-primary"})