from django.conf import settings
from celery import Celery
from server.components import config
from celery.schedules import crontab
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")
app = Celery("tasks", broker=config("REDIS_HOST"))

app.autodiscover_tasks()

app.conf.beat_schedule = {
    "send_email": {
        "task": "send_email",
        "schedule": crontab(minute=0, hour=9),
    }
}
mail_title = "Probation period update"


@app.task(name="send_email")
def send_email():
    from server.cshr.models.users import USER_TYPE
    import datetime
    from django.core.mail import send_mail
    from server.cshr.models.users import User

    date_since_month_and_a_half = datetime.datetime.now() - datetime.timedelta(45)
    date_since_three_months = datetime.datetime.now() - datetime.timedelta(90)
    users_joined_month_and_a_half_ago = User.objects.filter(
        created_at__contains=date_since_month_and_a_half
    )
    users_joined_three_months_ago = User.objects.filter(
        created_at__contains=date_since_three_months
    )
    admins = User.objects.filter(user_type=USER_TYPE.ADMIN)
    admins_emails = []
    for admin in admins:
        admins_emails.append(admin.email)

    for user in users_joined_month_and_a_half_ago:
        user_email = user.email
        try:
            supervisor = User.objects.get(pk=user.reporting_to.id)
            supervisor_email = supervisor.email

        except User.DoesNotExist:
            supervisor_email = ""

        user_msg = "Well Done! You have passed half of the probation period"
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
                user_email,
                supervisor_email,
            ],
        )
        send_mail(msg, mail_title, settings.EMAIL_HOST_USER, admins_emails)

    for user in users_joined_three_months_ago:
        user_email = user.email
        try:
            supervisor = User.objects.get(pk=user.reporting_to.id)
            supervisor_email = supervisor.email

        except User.DoesNotExist:
            supervisor_email = ""
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
        send_mail(msg, mail_title, settings.EMAIL_HOST_USER, admins_emails)
