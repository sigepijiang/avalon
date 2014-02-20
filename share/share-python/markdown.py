# -*- coding: utf-8 -*-

import re

from markdown2 import Markdown, DEFAULT_TAB_WIDTH


class MyMarkDown(Markdown):
    _del_re = re.compile(r"(~~)(?=\S)(.+?[~]*)(?<=\S)\1", re.S)

    def _do_delete(self, text):
        text = self._del_re.sub(r"<del>\2</del>", text)
        return text

    def _run_span_gamut(self, text):
        text = super(MyMarkDown, self)._run_span_gamut(text)
        text = self._do_delete(text)
        return text


def markdown(text, html4tags=False, tab_width=DEFAULT_TAB_WIDTH,
             safe_mode=None, extras=None, link_patterns=None,
             use_file_vars=False):
    return MyMarkDown(html4tags=html4tags, tab_width=tab_width,
                    safe_mode=safe_mode, extras=extras,
                    link_patterns=link_patterns,
                    use_file_vars=use_file_vars).convert(text)
