from celery import Celery
from configs import settings

app = Celery(settings.PROJECT_NAME)
app.config_from_object(settings.CELERY_CONFIG)
