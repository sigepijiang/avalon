# -*- coding:utf-8 -*-
import sys

_self = sys.modules[__name__]


class AvalonException(Exception):
    pass


class RouteBuildError(AvalonException):
    pass


class AvalonEnvironError(AvalonException):
    pass


class AvalonConfigError(AvalonException):
    '''
    服务器配置错误，阻止启动
    '''
    pass
