from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from datetime import timedelta

# establece la configuración de Django para la aplicación de Celery.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core', broker='redis://redis:6379/0')

# Utiliza la configuración de Django para la configuración de Celery.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Carga las tareas de todos los archivos registered_apps.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'check_users_every_24_hours': {
        'task': 'chat.tasks.check_users',
        'schedule': timedelta(hours=24),
    },
}