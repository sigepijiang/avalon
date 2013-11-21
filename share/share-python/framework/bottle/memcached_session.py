# -*- coding: utf-8 -*-
'''
    copid from beaker.session and beaker.middleware
'''
import uuid
import time


def _session_id():
    return uuid.uuid4().hex


class Session(dict):
    def __init__(self, request, id=None, key='avalon.session.id',
                 timeout=None):

        self.request = request
        self.key = key

        self.timeout = timeout
        self.is_new = self.id is None

        if self.is_new:
            self._create_id()
            self['_accessed_time'] = self['_creation_time'] = time.time()
        else:
            try:
                self.load()
            except Exception, e:
                if invalidate_corrupt:
                    util.warn(
                        "Invalidating corrupt session %s; "
                        "error was: %s.  Set invalidate_corrupt=False "
                        "to propagate this exception." % (self.id, e))
                    self.invalidate()
                else:
                    raise

    def has_key(self, name):
        return name in self

    def _set_cookie_values(self, expires=None):
        self.cookie[self.key] = self.id
        if self._domain:
            self.cookie[self.key]['domain'] = self._domain
        if self.secure:
            self.cookie[self.key]['secure'] = True
        self._set_cookie_http_only()
        self.cookie[self.key]['path'] = self._path

        self._set_cookie_expires(expires)

    def _set_cookie_expires(self, expires):
        if expires is None:
            if self.cookie_expires is not True:
                if self.cookie_expires is False:
                    expires = datetime.fromtimestamp(0x7FFFFFFF)
                elif isinstance(self.cookie_expires, timedelta):
                    expires = datetime.utcnow() + self.cookie_expires
                elif isinstance(self.cookie_expires, datetime):
                    expires = self.cookie_expires
                else:
                    raise ValueError("Invalid argument for cookie_expires: %s"
                                     % repr(self.cookie_expires))
            else:
                expires = None
        if expires is not None:
            if not self.cookie or self.key not in self.cookie:
                self.cookie[self.key] = self.id
            self.cookie[self.key]['expires'] = \
                expires.strftime("%a, %d-%b-%Y %H:%M:%S GMT")
        return expires

    def _update_cookie_out(self, set_cookie=True):
        self.request['cookie_out'] = self.cookie[self.key].output(header='')
        self.request['set_cookie'] = set_cookie

    def _set_cookie_http_only(self):
        try:
            if self.httponly:
                self.cookie[self.key]['httponly'] = True
        except Cookie.CookieError, e:
            if 'Invalid Attribute httponly' not in str(e):
                raise
            util.warn('Python 2.6+ is required to use httponly')

    def _create_id(self, set_new=True):
        self.id = _session_id()

        if set_new:
            self.is_new = True
            self.last_accessed = None
        if self.use_cookies:
            self._set_cookie_values()
            sc = set_new == False
            self._update_cookie_out(set_cookie=sc)

    @property
    def created(self):
        return self['_creation_time']

    def _set_domain(self, domain):
        self['_domain'] = domain
        self.cookie[self.key]['domain'] = domain
        self._update_cookie_out()

    def _get_domain(self):
        return self._domain

    domain = property(_get_domain, _set_domain)

    def _set_path(self, path):
        self['_path'] = self._path = path
        self.cookie[self.key]['path'] = path
        self._update_cookie_out()

    def _get_path(self):
        return self._path

    path = property(_get_path, _set_path)

    def _encrypt_data(self, session_data=None):
        """Serialize, encipher, and base64 the session dict"""
        session_data = session_data or self.copy()
        if self.encrypt_key:
            nonce = b64encode(os.urandom(6))[:8]
            encrypt_key = crypto.generateCryptoKeys(self.encrypt_key,
                                             self.validate_key + nonce, 1)
            data = util.pickle.dumps(session_data, 2)
            return nonce + b64encode(crypto.aesEncrypt(data, encrypt_key))
        else:
            data = util.pickle.dumps(session_data, 2)
            return b64encode(data)

    def _decrypt_data(self, session_data):
        """Bas64, decipher, then un-serialize the data for the session
        dict"""
        if self.encrypt_key:
            try:
                nonce = session_data[:8]
                encrypt_key = crypto.generateCryptoKeys(self.encrypt_key,
                                                 self.validate_key + nonce, 1)
                payload = b64decode(session_data[8:])
                data = crypto.aesDecrypt(payload, encrypt_key)
            except:
                # As much as I hate a bare except, we get some insane errors
                # here that get tossed when crypto fails, so we raise the
                # 'right' exception
                if self.invalidate_corrupt:
                    return None
                else:
                    raise
            try:
                return util.pickle.loads(data)
            except:
                if self.invalidate_corrupt:
                    return None
                else:
                    raise
        else:
            data = b64decode(session_data)
            return util.pickle.loads(data)

    def _delete_cookie(self):
        self.request['set_cookie'] = True
        expires = datetime.utcnow() - timedelta(365)
        self._set_cookie_values(expires)
        self._update_cookie_out()

    def delete(self):
        """Deletes the session from the persistent storage, and sends
        an expired cookie out"""
        if self.use_cookies:
            self._delete_cookie()
        self.clear()

    def invalidate(self):
        """Invalidates this session, creates a new session id, returns
        to the is_new state"""
        self.clear()
        self.was_invalidated = True
        self._create_id()
        self.load()

    def load(self):
        "Loads the data from this session from persistent storage"
        self.namespace = self.namespace_class(self.id,
            data_dir=self.data_dir,
            digest_filenames=False,
            **self.namespace_args)
        now = time.time()
        if self.use_cookies:
            self.request['set_cookie'] = True

        self.namespace.acquire_read_lock()
        timed_out = False
        try:
            self.clear()
            try:
                session_data = self.namespace['session']

                if (session_data is not None and self.encrypt_key):
                    session_data = self._decrypt_data(session_data)

                # Memcached always returns a key, its None when its not
                # present
                if session_data is None:
                    session_data = {
                        '_creation_time': now,
                        '_accessed_time': now
                    }
                    self.is_new = True
            except (KeyError, TypeError):
                session_data = {
                    '_creation_time': now,
                    '_accessed_time': now
                }
                self.is_new = True

            if session_data is None or len(session_data) == 0:
                session_data = {
                    '_creation_time': now,
                    '_accessed_time': now
                }
                self.is_new = True

            if self.timeout is not None and \
               now - session_data['_accessed_time'] > self.timeout:
                timed_out = True
            else:
                # Properly set the last_accessed time, which is different
                # than the *currently* _accessed_time
                if self.is_new or '_accessed_time' not in session_data:
                    self.last_accessed = None
                else:
                    self.last_accessed = session_data['_accessed_time']

                # Update the current _accessed_time
                session_data['_accessed_time'] = now

                # Set the path if applicable
                if '_path' in session_data:
                    self._path = session_data['_path']
                self.update(session_data)
                self.accessed_dict = session_data.copy()
        finally:
            self.namespace.release_read_lock()
        if timed_out:
            self.invalidate()

    def save(self, accessed_only=False):
        """Saves the data for this session to persistent storage

        If accessed_only is True, then only the original data loaded
        at the beginning of the request will be saved, with the updated
        last accessed time.

        """
        # Look to see if its a new session that was only accessed
        # Don't save it under that case
        if accessed_only and self.is_new:
            return None

        # this session might not have a namespace yet or the session id
        # might have been regenerated
        if not hasattr(self, 'namespace') or self.namespace.namespace != self.id:
            self.namespace = self.namespace_class(
                                    self.id,
                                    data_dir=self.data_dir,
                                    digest_filenames=False,
                                    **self.namespace_args)

        self.namespace.acquire_write_lock(replace=True)
        try:
            if accessed_only:
                data = dict(self.accessed_dict.items())
            else:
                data = dict(self.items())

            if self.encrypt_key:
                data = self._encrypt_data(data)

            # Save the data
            if not data and 'session' in self.namespace:
                del self.namespace['session']
            else:
                self.namespace['session'] = data
        finally:
            self.namespace.release_write_lock()
        if self.use_cookies and self.is_new:
            self.request['set_cookie'] = True

    def revert(self):
        """Revert the session to its original state from its first
        access in the request"""
        self.clear()
        self.update(self.accessed_dict)

    def regenerate_id(self):
        """
            creates a new session id, retains all session data

            Its a good security practice to regnerate the id after a client
            elevates priviliges.

        """
        self._create_id(set_new=False)

    # TODO: I think both these methods should be removed.  They're from
    # the original mod_python code i was ripping off but they really
    # have no use here.
    def lock(self):
        """Locks this session against other processes/threads.  This is
        automatic when load/save is called.

        ***use with caution*** and always with a corresponding 'unlock'
        inside a "finally:" block, as a stray lock typically cannot be
        unlocked without shutting down the whole application.

        """
        self.namespace.acquire_write_lock()

    def unlock(self):
        """Unlocks this session against other processes/threads.  This
        is automatic when load/save is called.

        ***use with caution*** and always within a "finally:" block, as
        a stray lock typically cannot be unlocked without shutting down
        the whole application.

        """
        self.namespace.release_write_lock()
    pass


class SessionObject(object):
    """Session proxy/lazy creator

    This object proxies access to the actual session object, so that in
    the case that the session hasn't been used before, it will be
    setup. This avoid creating and loading the session from persistent
    storage unless its actually used during the request.

    """
    def __init__(self, environ, **params):
        self._params = params
        self._envirion = environ
        self._sess = None
        self._headers = {}
        self._dirty = False

    @property
    def _session(self):
        """Lazy initial creation of session object"""
        if self._sess is None:
            params = self._params
            environ = self._environ
            self._headers = req = {'cookie_out': None}
            req['cookie'] = environ.get('HTTP_COOKIE')
            self._sess = Session(
                req, use_cookies=True, **params)
        return self._sess

    def __getattr__(self, attr):
        return getattr(self._session, attr)

    def __setattr__(self, attr, value):
        setattr(self._session, attr, value)

    def __delattr__(self, name):
        self._session.__delattr__(name)

    def __getitem__(self, key):
        return self._session[key]

    def __setitem__(self, key, value):
        self._session[key] = value

    def __delitem__(self, key):
        self._session.__delitem__(key)

    def __repr__(self):
        return self._session.__repr__()

    def __iter__(self):
        """Only works for proxying to a dict"""
        return iter(self._session.keys())

    def __contains__(self, key):
        return key in self._session

    def has_key(self, key):
        return key in self._session

    def get_by_id(self, session_id):
        """Loads a session given a session ID"""
        params = self._params
        session = Session(
            {}, use_cookies=False, session_id=session_id, **params)
        if session.is_new:
            return None
        return session

    def save(self):
        self._dirty = True

    def delete(self):
        self._dirty = True
        self._session.delete()

    def persist(self):
        """Persist the session to the storage

        If its set to autosave, then the entire session will be saved
        regardless of if save() has been called. Otherwise, just the
        accessed time will be updated if save() was not called, or
        the session will be saved if save() was called.

        """
        if self._params.get('auto'):
            self._session.save()
        else:
            if self._dirty:
                self._session.save()
            else:
                self._session.save(accessed_only=True)

    @property
    def dirty(self):
        return self._dirty

    @property
    def accessed(self):
        """Returns whether or not the session has been accessed"""
        return self._sess is not None


class SessionMiddleware(object):
    environ_key = 'avalon.session'

    def __init__(self, wrap_app):
        self.wrap_app = self.app = wrap_app

    def __call__(self, environ, start_response):
        session = SessionObject(environ, **self.options)
        environ[self.environ_key] = session
        environ['avalon.get_session'] = self._get_session

        def session_start_response(status, headers, exc_info=None):
            if session.accessed:
                session.persist()
                if session.__dict__['_headers']['set_cookie']:
                    cookie = session.__dict__['_headers']['cookie_out']
                    if cookie:
                        headers.append(('Set-cookie', cookie))
            return start_response(status, headers, exc_info)
        return self.wrap_app(environ, session_start_response)

    def _get_session(self):
        return Session({}, use_cookies=False, **self.options)
