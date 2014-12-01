#-*- coding: utf-8 -*-
import md5

from bottle import request, redirect, url

from share.framework.bottle.engines import db
from share.framework.bottle import MethodView, view, render_template
from share.framework.bottle.restful import backends

from zeus.models import AccountModel, EmailModel
from .forms import LoginForm, SignUpForm, DisplaySuccessForm


class SigninView(MethodView):
    @view('www/signin.html')
    def get(self):
        form = LoginForm(request.params)
        display_form = DisplaySuccessForm(request.params)
        return {
            'form': form,
            'display_form': display_form,
        }

    def post(self):
        form = LoginForm(request.forms)
        display_form = DisplaySuccessForm(request.params)
        if not form.validate():
            return render_template(
                'www/signin.html', error=u'用户不存在或者密码错误')

        if not display_form.validate():
            return render_template(
                'www/signin.html', error=u'请求参数错误')

        data = form.data
        success = display_form.data.get('success')
        account = EmailModel.query.filter(
            EmailModel.email == data['email'],
            EmailModel.password_hash == md5.new(
                data['password_hash']).hexdigest()
        ).first()
        if not account:
            return render_template(
                'www/signin.html', error=u'用户不存在或者密码错误')

        request.session['ukey'] = account.ukey
        return redirect(success or url('apollo:www.main'))


class SignUpView(MethodView):
    @view('www/signup.html')
    def get(self):
        display_form = DisplaySuccessForm(request.params)
        return {
            'display_form': display_form
        }

    def post(self):
        form = SignUpForm(request.forms)
        display_form = DisplaySuccessForm(request.params)
        if not form.validate():
            return render_template('www/signup.html')

        if not display_form.validate():
            return render_template(
                'www/signup.html', error=u'请求参数错误')

        success = display_form.data.get('success')

        try:
            account = AccountModel.create(**form.data)
            db.session.commit()
        except Exception as e:
            return render_template('www/signup.html', error=e)

        request.session['ukey'] = account.ukey
        backends.apollo.user.post(
            ukey=account.ukey, nickname=account.nickname)
        return redirect(success or url('apollo:www.main'))
