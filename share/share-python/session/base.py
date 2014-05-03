#-*- coding: utf-8 -*-
import uuid


from share.utils import const


def new_session_id():
    return uuid.uuid3(
        uuid.UUID(const.namespace), uuid.uuid4().hex).hex


class Session(dict):
    def __init__(self, request, session_id=None, timeout=0,
                 use_cookies=False):
        self.session_id = session_id
        if not self.session_id:
            self.session_id = new_session_id()
        try:
            uuid.UUID(self.session_id)
        except ValueError:
            self.session_id = new_session_id()

        self.request = request
        self.timeout = timeout
        self.use_cookies = use_cookies
        request.session = self
