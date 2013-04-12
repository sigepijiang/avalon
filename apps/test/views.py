#-*- coding: utf-8 -*-

import xml
from lxml import etree
from StringIO import StringIO
from time import time

from bottle import route, get, post, redirect
from bottle import request


@get('/test/')
def test_get():
    print request.GET

    echostr = request.GET.get('echostr')
    return echostr


@post('/test/')
def test_post():
    print request.__dict__
    print dir(request)

    for i in dir(request):
        print i, getattr(request, i)
    print request.POST.keys()
    print request.GET.items()

    message_xml = etree.parse(StringIO(request.POST.keys()[0]))
    message_dict = {}


    for node in message_xml.iter():
        message_dict[node.tag] = node.text

    to_user_name = message_dict['ToUserName']
    from_user_name = message_dict['FromUserName']
    content = message_dict.get('Content', '').strip()
    message_type = message_dict['MsgType']

    result = '''
<xml>
    <ToUserName><![CDATA[{to_user_name}]]></ToUserName>
    <FromUserName><![CDATA[from_user_name]]></FromUserName>
    <CreateTime>{create_time}</CreateTime>
    <MsgType><![CDATA[text]]></MsgType>
    <Content><![CDATA[指南]]></Content>
    <FuncFlag>0</FuncFlag>
</xml>
    '''.format(from_user_name=to_user_name,
            create_time=int(time()),
            to_user_name=from_user_name)

    if content == u'for_test':
        return result
