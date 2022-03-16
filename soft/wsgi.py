import os
import sys
import site
import threading

sys.path.append('/opt/soft/wsgi')
#sys.path.insert(0, '/opt/python/current/app')
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "soft.settings")
#os.environ['HTTPS'] = "on"
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

#calling create bucket folders after wsgi worked
#from firmware.views import bucketfolders
#bucketfolders(get_wsgi_application())

from firmware.views import create_tables

create_tables(get_wsgi_application())

