#-*- coding: utf-8 -*-
import os
import sys

from share.config import load_yaml


def get_app_info():
    yaml_path = sys.argv[1]
    config = load_yaml(yaml_path)

    app_name = config['APP_NAME']
    app_path = os.path.dirname(yaml_path)
    app_type = config['APP_TYPE']

    print app_name, app_path, app_type


if __name__ == '__main__':
    get_app_info()
