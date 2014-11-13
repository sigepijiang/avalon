#-*- coding: utf-8 -*-

from wtforms import Form, validators
from wtforms import StringField, PasswordField, HiddenField


class DisplaySuccessForm(Form):
    display = HiddenField()
    success = HiddenField()


class LoginForm(Form):
    email = StringField(validators=[validators.Required()])
    password_hash = PasswordField(validators=[validators.Required()])


class SignUpForm(Form):
    email = StringField(validators=[validators.Required()])
    password_hash = PasswordField(validators=[validators.Required()])
    nickname = StringField()
