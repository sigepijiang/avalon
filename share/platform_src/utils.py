#-*- coding: utf-8 -*-
import os

def importer(import_name):
    return __import__(import_name, fromlist=[''])


def base36_encode(number):
    assert number >= 0, 'positive integer required'
    if number == 0:
        return '0'
    base36 = []
    while number != 0:
        number, i = divmod(number, 36)
        base36.append('0123456789abcdefghijklmnopqrstuvwxyz'[i])
    return ''.join(reversed(base36))


def base36_decode(text):
    return int(text, 36)


def id2ukey(source):
    return base36_encode(int(source))


def ukey2id(source):
    return base36_decode(source)

def is_file_exists(path):
    return os.path.exists(path)
