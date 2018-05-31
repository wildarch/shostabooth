from __future__ import (absolute_import, division, print_function, unicode_literals)
from builtins import *
import flickr_api
from os import path

AUTH_FILE = 'auth_handler.key'

if not path.isfile(AUTH_FILE):
    print("No authentication handler file exists! Please run flickr_authorize.py first!")
    # Just continue now, we warned the user and flickr_api will raise the exception
flickr_api.set_auth_handler(AUTH_FILE)
