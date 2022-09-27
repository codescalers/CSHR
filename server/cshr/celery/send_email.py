from array import array
from django.conf import settings
from celery import Celery
from server.components import config
from celery.schedules import crontab
import datetime
from django.core.mail import send_mail
from celery import shared_task
from django.core.exceptions import ImproperlyConfigured
from rest_framework.response import Response


if config("REDIS_HOST") is None:
    raise ImproperlyConfigured("REDIS_HOST is not defined")
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

    from server.cshr.models.users import User

    date_since_month_and_a_half = datetime.datetime.now() - datetime.timedelta(45)
    date_since_three_months = datetime.datetime.now() - datetime.timedelta(90)
    users_joined_month_and_a_half_ago = User.objects.filter(
        created_at__year=date_since_month_and_a_half.year,
        created_at__month=date_since_month_and_a_half.month,
        created_at__day=date_since_month_and_a_half.day,
    )
    users_joined_three_months_ago = User.objects.filter(
        created_at__year=date_since_three_months.year,
        created_at__month=date_since_three_months.month,
        created_at__day=date_since_three_months.day,
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
            mail_title,
            user_msg,
            settings.EMAIL_HOST_USER,
            [
                user_email,
            ],
        )
        send_mail(
            mail_title,
            msg,
            settings.EMAIL_HOST_USER,
            [
                user_email,
                supervisor_email,
            ],
        )
        send_mail(mail_title, msg, settings.EMAIL_HOST_USER, admins_emails)

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
            mail_title,
            user_msg,
            settings.EMAIL_HOST_USER,
            [
                user_email,
            ],
        )
        send_mail(
            mail_title,
            msg,
            settings.EMAIL_HOST_USER,
            [
                supervisor_email,
            ],
        )
        send_mail(mail_title, msg, settings.EMAIL_HOST_USER, admins_emails)


@shared_task()
def send_email_for_request(user_id, msg, mail_title) -> Response:
    from django.core.mail import send_mail
    from server.cshr.models.users import User
    from server.cshr.utils.send_email import get_email_recievers
    from server.cshr.services.users import get_user_by_id
    from server.cshr.utils.send_email import check_email_configuration

    check_email_configuration()
    user: User = get_user_by_id(user_id)
    if user is None:
        return False
    recievers: array[str] = get_email_recievers(user)
    send_mail(mail_title, msg, settings.EMAIL_HOST_USER, recievers, fail_silently=False)
    return True


@shared_task()
def send_email_for_reply(approving_user_id, data, msg, mail_title) -> Response:
    from django.core.mail import send_mail
    from server.cshr.models.users import User
    from server.cshr.utils.send_email import get_email_recievers
    from server.cshr.services.users import get_user_by_id
    from server.cshr.utils.send_email import check_email_configuration

    check_email_configuration()
    approving_user: User = get_user_by_id(approving_user_id)
    if approving_user is None:
        return False
    applying_user = data.applying_user
    if applying_user is None:
        return False
    recievers: array[str] = get_email_recievers(applying_user)
    send_mail(mail_title, msg, settings.EMAIL_HOST_USER, recievers, fail_silently=False)
    return True
