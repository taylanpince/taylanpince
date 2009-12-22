import os
import sys

sys.path.append("/home/taylan/sites/taylanpince/app")
sys.path.append("/home/taylan/sites/taylanpince/app/libs")
sys.path.append("/home/taylan/sites/taylanpince/app/taylanpince")

os.environ["DJANGO_SETTINGS_MODULE"] = "taylanpince.settings"

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
