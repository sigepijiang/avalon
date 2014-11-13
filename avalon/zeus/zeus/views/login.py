#-*- coding: utf-8 -*-
import md5

from bottle import request, redirect, url

from share.framework.bottle.engines import db
from share.framework.bottle import MethodView, view, render_template
from share.framework.bottle.restful import backends

from zeus.models import AccountModel, EmailModel
from .forms import LoginForm, SignUpForm


class SigninView(MethodView):
    @view('www/signin.html')
    def get(self):
        form = LoginForm(request.params)
        return {'form': form}

    def post(self):
        form = LoginForm(request.forms)
        if not form.validate():
            return render_template(
                'www/signin.html', error=u'用户不存在或者密码错误')

        data = form.data
        print data
        account = EmailModel.query.filter(
            EmailModel.email == data['email'],
            EmailModel.password_hash == md5.new(
                data['password_hash']).hexdigest()
        ).first()
        if not account:
            return render_template(
                'www/signin.html', error=u'用户不存在或者密码错误')

        request.session['ukey'] = account.ukey
        return redirect(data.get('success') or url('apollo:www.main'))


class SignUpView(MethodView):
    @view('www/signup.html')
    def get(self):
        return {}

    def post(self):
        form = SignUpForm(request.forms)
        if not form.validate():
            return render_template('www/signup.html')

        try:
            account = AccountModel.create(**form.data)
            db.session.commit()
        except Exception as e:
            print e
            return render_template('www/signup.html', error=e)

        request.session['ukey'] = account.ukey
        backends.apollo.user.post(
            ukey=account.ukey, nickname=account.nickname)
        return redirect(url('apollo:www.main'))
