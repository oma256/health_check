from huey import crontab
from huey.contrib.djhuey import db_periodic_task

from apps.notifications.models import Notification


@db_periodic_task(crontab(minute='0', hour='10', day_of_week='1,4'))
def send_notification_to_fill_indicator_2_day_in_week():
    Notification.create_indicator_type()
