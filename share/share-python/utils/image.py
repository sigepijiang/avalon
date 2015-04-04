#-*- coding: utf-8 -*-


def image_for(hashkey, onerror=''):
    if onerror:
        hashkey = hashkey or onerror
    if not hashkey:
        return ''

    return 'http://wishstone.qiniudn.com/%s' % hashkey
