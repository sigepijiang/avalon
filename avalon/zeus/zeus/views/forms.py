#-*- coding: utf-8 -*-

from wtforms import Form, validators
from wtforms import StringField, PasswordField


class LoginForm(Form):
    email = StringField(validators=[validators.Required()])
    password = PasswordField(validators=[validators.Required()])
    display = StringField(default='form')
