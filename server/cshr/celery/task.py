from django.conf import settings

from celery import Celery
from celery.schedules import crontab
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")
app = Celery("tasks", broker="redis://localhost:6000")

app.autodiscover_tasks()

app.conf.beat_schedule = {
    "send_email": {
        "task": "send_email",
        "schedule": crontab(minute=0, hour=8),
    }
}
mail_title = "Probation period update"


@app.task(name="send_email")
def send_email():
    from server.cshr.models.users import USER_TYPE
    from datetime import datetime
    from django.core.mail import send_mail
    from server.cshr.models.users import User

    users = User.objects.all()
    admins = User.objects.filter(user_type = USER_TYPE.ADMIN)
    admins_emails =[]
    for admin in admins:
        admins_emails.append(admin.email)
        
    for user in users:
        joining_date = user.created_at
        # difference between user joining date and today in days
        delta_days = (
            datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            - joining_date.replace(
                hour=0, minute=0, second=0, microsecond=0, tzinfo=None
            )
        ).days
        user_email = user.email
        try:
            supervisor = User.objects.get(pk=user.reporting_to.id)        
            supervisor_email = supervisor.email
        except:
            supervisor_email = ""    
        if delta_days == 45:

            msg = "{fname} {lname} has passed half of the probation period".format(
                fname=user.first_name, lname=user.last_name
            )
            send_mail(
                msg,
                mail_title,
                settings.EMAIL_HOST_USER,
                [
                    user_email,
                    supervisor_email,
                    
                ],
            )
            send_mail(
                msg,
                mail_title,
                settings.EMAIL_HOST_USER,
                admins_emails
            )

        elif delta_days == 90:
            user_msg = "Congratulations on passing your probation period"
            msg = "{fname} {lname} has passed half of the probation period".format(
                fname=user.first_name, lname=user.last_name
            )
            send_mail(
                user_msg,
                mail_title,
                settings.EMAIL_HOST_USER,
                [
                    user_email,
                ],
            )
            send_mail(
                msg,
                mail_title,
                settings.EMAIL_HOST_USER,
                [
                    supervisor_email,
                ],
            )
            send_mail(
                msg,
                mail_title,
                settings.EMAIL_HOST_USER,
                admins_emails   
            )