#-*- coding: utf-8 -*-
import md5

from bottle import request, redirect, url

from share.engines import db
from share.framework.bottle import MethodView, view, render_template

from zeus.models import EmailModel
from .forms import LoginForm, SignUpForm


class SigninView(MethodView):
    @view('www/signin.html')
    def get(self):
        return {}

    def post(self):
        form = LoginForm(request.forms)
        if not form.validate():
            return

        data = form.data
        account = EmailModel.query.filter(
            EmailModel.email == data['email'],
            EmailModel.password == md5.new(data['password']).hexdigest()
        )
        if not account:
            return

        request.session['ukey'] = account.ukey
        return redirect(data['success'] or url('apollo:www.main'))


class SignUpView(MethodView):
    @view('www/signup.html')
    def get(self):
        return {}

    def post(self):
        form = SignUpForm(request.forms)
        if not form.validate():
            return render_template('www/signup.html')

        try:
            EmailModel.create(**form.data)
            db.session.commit()
        except:
            return render_template('www/signup.html', error='')

        return redirect(url('heracles:www.main'))
