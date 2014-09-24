# -*- coding: utf-8 -*-

from wtforms.validators import Regexp


class Ukey(Regexp):
    """
    校验是否是合法的 ukey.

    """

    def __init__(self, message=None):
        super(Ukey, self).__init__(r'^[0-9a-z]{7}$', message=message)

    def __call__(self, form, field):
        if self.message is None:
            self.message = '非法的ukey'

        super(Ukey, self).__call__(form, field)


ukey = Ukey
