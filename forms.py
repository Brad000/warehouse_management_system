from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, Email


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    usertype = SelectField('User Type', choices=[('admin', 'Admin'), ('warehouse', 'Warehouse Operative'), ('manager', 'Manager')])
    submit = SubmitField('Login !!')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),
                                                   Length(min=4, max=20)])
    password = PasswordField('Password',
                             validators=[DataRequired(),
                                         EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Repeat Password')
    email = StringField('Email Address', validators=[Length(min=6, max=35), Email()])
    usertype = SelectField('User Type', choices=[('admin', 'Admin'), ('warehouse', 'Warehouse Operative'), ('manager', 'Manager')])
    submit = SubmitField('Register')
