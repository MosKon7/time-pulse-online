# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, '/var/www/u2446498/data/www/time-pulse.online/monitoring')
sys.path.insert(1, '/var/www/u2446498/data/djangoenv/lib/python3.7/site-packages/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'monitoring.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()