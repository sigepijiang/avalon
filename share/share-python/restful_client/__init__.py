#-*- coding: utf-8 -*-

from .base import Client


# TODO: PEP302 APIImporter

apis = Client([], subdomain='apis')
backends = Client([], subdomain='backends')
services = Client([], subdomain='services')
