#-*- coding: utf-8 -*-

from wtforms import Form, validators
from wtforms import StringField, PasswordField


class DisplaySuccessForm(Form):
    display = StringField()
    success = StringField()


class LoginForm(Form):
    email = StringField(validators=[validators.Required()])
    password_hash = PasswordField(validators=[validators.Required()])
    success = StringField()


class SignUpForm(Form):
    email = StringField(validators=[validators.Required()])
    password_hash = PasswordField(validators=[validators.Required()])
    nickname = StringField()
