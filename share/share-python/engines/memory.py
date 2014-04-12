#-*- coding: utf-8 -*-
from memcache import Client


class Client(Client):
    def check_key(self, key, key_extra_len=0):
        if isinstance(key, tuple):
            key = key[1]
        if not key:
            raise Client.MemcachedKeyNoneError("Key is None")
        if not isinstance(key, (str, unicode)):
            raise Client.MemcachedKeyTypeError(
                'Keys must be str or unicode'
            )
        # XXX: 这个规则好烦，unicode会引发crc32的问题。
        # if isinstance(key, unicode):
        #     raise Client.MemcachedStringEncodingError(
        #         "Keys must be str()'s, not unicode.  "
        #         "Convert your unicode "
        #         "strings using mystring.encode(charset)!")
        # if not isinstance(key, str):
        #     raise Client.MemcachedKeyTypeError("Key must be str()'s")

        # if isinstance(key, basestring):
        #     if self.server_max_key_length != 0 and \
        #         len(key) + key_extra_len > self.server_max_key_length:
        #         raise Client.MemcachedKeyLengthError(
        #             "Key length is > %s" % self.server_max_key_length)
        #     if not valid_key_chars_re.match(key):
        #         raise Client.MemcachedKeyCharacterError(
        #                 "Control characters not allowed")
