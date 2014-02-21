#-*- coding: utf-8 -*-
import os
import hashlib
import re

import bs4
import markdown2

from share.restful import RESTfulAPI
from share.engines import db

from heracles import app
from heracles.models import BlogModel, TextModel


class UpdateOpenAPI(RESTfulAPI):
    path = '/blog/update'

    def _get_title(self, bs):
        return bs.h1.text

    def _get_summary(self, bs):
        tmp = bs4.BeautifulSoup()

        h_num = 0
        for i in bs.contents:
            if re.match(ur'h\d', i.name):
                h_num += 1

            if h_num >= 2:
                break

            tmp.append(i)
        return tmp.prettify()


    def _update_blogs(self, arg, directory, file_list):
        for file_name in file_list:
            blog = BlogModel.query.filter(
                BlogModel.file_name == file_name).first()
            md = open(os.path.join(directory, file_name), 'r').read()
            html = markdown2.markdown(md)
            bs = bs4.BeautifulSoup(html)

            hashkey = hashlib.md5(md).hexdigest()

            if not blog:
                text = TextModel(
                    content=html, hashkey=hashkey, parent_hashkey=None)

                blog = BlogModel(
                    file_name=file_name,
                    title=self._get_title(bs),
                )
                db.session.add(text)
                db.session.add(blog)
            else:
                print blog
                print hashkey
                print blog.text.hashkey
                text = blog.text
                if text.hashkey == hashkey:
                    continue

                text = TextModel(content=html, hashkey=hashkey)
                text.parent = blog.text

            blog.text = text
            blog.summary = self._get_summary(bs)
            db.session.commit()

    def create(self):
        path = os.path.join(app.config['app_path'], 'templates/md')
        os.path.walk(path, self._update_blogs, None)
        return {}
