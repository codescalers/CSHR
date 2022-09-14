from django.conf import settings
from celery import Celery
from server.components import config
from celery.schedules import crontab
import datetime
from django.core.mail import send_mail
from celery import shared_task

# from django.core.exceptions import ImproperlyConfigured


# if (config("REDIS_HOST") is None):
#     raise ImproperlyConfigured("REDIS_HOST is not defined")
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
def send_email_for_vacation_request(user_id, data):
    from django.core.mail import send_mail
    from server.cshr.models.users import User
    from server.cshr.utils.send_email import get_email_recievers
    from server.cshr.utils.email_messages_templates import (
        get_vacation_request_email_template,
    )

    user: User = User.objects.get(pk=user_id)
    recievers = get_email_recievers(user)
    msg = get_vacation_request_email_template(user, data)
    mail_title = "vacation request"
    send_mail(mail_title, msg, settings.EMAIL_HOST_USER, recievers, fail_silently=False)


@shared_task()
def send_email_for_hr_letter_request(user_id, data):
    from django.core.mail import send_mail
    from server.cshr.models.users import User
    from server.cshr.utils.send_email import get_email_recievers
    from server.cshr.utils.email_messages_templates import (
        get_hr_letter_request_email_template,
    )

    user: User = User.objects.get(pk=user_id)
    recievers = get_email_recievers(user)
    msg = get_hr_letter_request_email_template(user, data)
    mail_title = "Hr Letter request"
    send_mail(mail_title, msg, settings.EMAIL_HOST_USER, recievers, fail_silently=False)


@shared_task()
def send_email_for_compensation_request(user_id, data):
    from django.core.mail import send_mail
    from server.cshr.models.users import User
    from server.cshr.utils.send_email import get_email_recievers
    from server.cshr.utils.email_messages_templates import (
        get_compensation_request_email_template,
    )

    user: User = User.objects.get(pk=user_id)
    recievers = get_email_recievers(user)
    msg = get_compensation_request_email_template(user, data)
    mail_title = "Compensation request"
    send_mail(mail_title, msg, settings.EMAIL_HOST_USER, recievers, fail_silently=False)


@shared_task()
def send_email_for_vacation_reply(approving_user_id, data):
    from django.core.mail import send_mail
    from server.cshr.models.users import User
    from server.cshr.utils.send_email import get_email_recievers
    from server.cshr.utils.email_messages_templates import (
        get_vacation_reply_email_template,
    )

    approving_user: User = User.objects.get(pk=approving_user_id)
    applying_user_id = data["applying_user"]
    applying_user = User.objects.get(pk=applying_user_id)
    recievers = get_email_recievers(applying_user)
    msg = get_vacation_reply_email_template(approving_user, data)
    mail_title = "Vacation reply"
    send_mail(mail_title, msg, settings.EMAIL_HOST_USER, recievers, fail_silently=False)


@shared_task()
def send_email_for_hr_letter_reply(approving_user_id, data):
    from django.core.mail import send_mail
    from server.cshr.models.users import User
    from server.cshr.utils.send_email import get_email_recievers
    from server.cshr.utils.email_messages_templates import (
        get_hr_letter_reply_email_template,
    )

    approving_user: User = User.objects.get(pk=approving_user_id)
    applying_user_id = data["applying_user"]
    applying_user = User.objects.get(pk=applying_user_id)
    recievers = get_email_recievers(applying_user)
    msg = get_hr_letter_reply_email_template(approving_user, data)
    mail_title = "Hr Letter reply"
    send_mail(mail_title, msg, settings.EMAIL_HOST_USER, recievers, fail_silently=False)


@shared_task()
def send_email_for_compensation_reply(approving_user_id, data):
    from django.core.mail import send_mail
    from server.cshr.models.users import User
    from server.cshr.utils.send_email import get_email_recievers
    from server.cshr.utils.email_messages_templates import (
        get_compensation_reply_email_template,
    )

    approving_user: User = User.objects.get(pk=approving_user_id)
    applying_user_id = data["applying_user"]
    applying_user = User.objects.get(pk=applying_user_id)
    recievers = get_email_recievers(applying_user)
    msg = get_compensation_reply_email_template(approving_user, data)
    mail_title = "Compensation reply"
    send_mail(mail_title, msg, settings.EMAIL_HOST_USER, recievers, fail_silently=False)
