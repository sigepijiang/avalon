from .base import RESTfulAPI, RESTfulOpenAPI, RESTfulBackendAPI
from .client import Client
from .validator import resful_validator


# TODO: PEP302 APIImporter

apis = Client([], subdomain='apis')
backends = Client([], subdomain='backends')
services = Client([], subdomain='services')
