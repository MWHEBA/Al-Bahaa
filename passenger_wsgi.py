import os
import sys
import gc

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_PATH)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')

gc.set_threshold(700, 10, 10)

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
