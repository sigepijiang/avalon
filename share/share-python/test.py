#-*- coding: utf-8 -*-
from functools import wraps


class A(object):
    def __init__(self, *args, **kwargs):
        pass

    def __call__(self, func):
        @wraps(func)
        def call_f(self, *args, **kwargs):
            return func(*args, **kwargs)
        return call_f


def d(func):
    setattr(func, 'a', '123')
    return func


def e(func):
    func.b = '123'

    @wraps(func)
    def call_f(*args, **kwargs):
        return func(*args, **kwargs)
    return call_f


class C(object):
    @d
    def a(p):
        print p

    @e
    def b(p):
        print p


@A()
@d
def a(p):
    print p
print a.__dict__, dir(a)
print C().a.__dict__, dir(C().a)
print type(a), type(C().a)

print getattr(a, 'a')
delattr(a, 'a')
print getattr(C().a, 'a')
# delattr(C().a, 'a')

print getattr(C().b, 'b')
delattr(C().b, 'b')
