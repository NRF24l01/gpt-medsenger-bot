from celery import Celery
from config import REDIS_HOST

celery = Celery(
    __name__,
    broker='redis://'+REDIS_HOST+':6379/0',
    backend='redis://'+REDIS_HOST+':6379/0'
)

celery.conf.task_default_queue = 'gpt_queue'