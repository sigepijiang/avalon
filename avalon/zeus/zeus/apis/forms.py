# -*- coding: utf-8 -*-

import voluptuous


client_id = {
    voluptuous.Required('client_id'): voluptuous.Coerce(int),
}

ukey = {
    voluptuous.Required('ukey'): voluptuous.Match(r'^[0-9a-zA-Z]{8}$'),
}

secret = {
    voluptuous.Required('secret'): voluptuous.Match(r'^[0-9a-zA-Z]{32}$'),
}
