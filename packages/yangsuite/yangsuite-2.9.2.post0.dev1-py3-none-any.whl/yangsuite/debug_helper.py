import os
import django
import configparser
from yangsuite.application import read_prefs

def start_django():
    config = read_prefs()
    prefs = config[configparser.DEFAULTSECT]
    os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                          prefs.get('settings_module'))
    os.environ.setdefault('MEDIA_ROOT',
                          prefs.get('data_path'))
    # set_base_path(os.environ['MEDIA_ROOT'])
    django.setup()

