import os
try:
    import requests , user_agent , names , uuid , urllib , hashlib , instaloader , mechanize
except ModuleNotFoundError:
    os.system('pip install requests')
    os.system('pip install user_agent')
    os.system('pip install names')
    os.system('pip install urllib')
    os.system('pip install hashlib')
    os.system('pip install uuid')
    os.system('pip install instaloader')
    os.system('pip install mechanize')

from .gdo_drow import gdo_drow
from .check_email import check_email
from .gdo_order import gdo_order
from .IG import info_IG , session_IG , login_IG , create_IG
from .info_face import info_face
from .info_tiktok import info_tik
from .login import login
from .fake import *