# -*- coding: utf-8 -*-

import voluptuous


ukey = {
    voluptuous.Required('ukey'): voluptuous.Match(r'^[0-9a-zA-Z]{7}$'),
}

nickname = {
    voluptuous.Required('ukey'): voluptuous.Match(r'^[0-9a-zA-Z]{7}$'),
}

gender = {}
title = {}
summary = {}
