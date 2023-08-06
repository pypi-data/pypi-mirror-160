__title__ = 'xamino'
__author__ = 'forevercynical'
__license__ = 'MIT'
__copyright__ = 'Copyright 2022 Cynical'
__version__ = '0.1.0'

from base64 import b64decode, b64encode
from functools import reduce
from hashlib import sha1
from hmac import new as hmac
from re import sub
from colored import stylize, fg, bg, attr
from httpx import Client as httpx, Response as httpxResponse, ReadTimeout as httpxReadTimeout
from time import localtime, time, timezone, sleep
from os import path, urandom,  _exit as exit
from ujson import dumps, loads
from random import randint, choice
from string import ascii_letters, digits
from binascii import hexlify
from uuid import UUID