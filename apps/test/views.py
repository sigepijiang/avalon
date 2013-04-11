#-*- coding: utf-8 -*-

import xml
from lxml import etree
from StringIO import StringIO
from time import time

from bottle import route, get, post, redirect
from bottle import request


@post('/test/')
def blog():
    print request.__dict__

    message_dict = etree.parse(StringIO(request.data))

    to_user_name = message_dict['ToUserName']
    from_user_name = message_dict['FromUserName']
    content = message_dict.get('Content', '').strip()
    message_type = message_dict['MsgType']

    result = '''
<xml>
    <ToUserName><![CDATA[{from_user_name}]]></ToUserName>
    <FromUserName><![CDATA[to_user_name]]></FromUserName>
    <CreateTime>{create_time}</CreateTime>
    <MsgType><![CDATA[text]]></MsgType>
    <Content><![CDATA[指南]]></Content>
    <FuncFlag>0</FuncFlag>
</xml>
    '''.format(from_user_name=to_user_name,
            create_time=int(time()),
            to_user_name=from_user_name)
    return result
