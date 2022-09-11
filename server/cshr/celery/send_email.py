from typing import Dict
from django.conf import settings
from celery import Celery
from server.components import config
from celery.schedules import crontab
import datetime
from django.core.mail import send_mail
from celery import shared_task
from server.cshr.models.users import User
from server.cshr.utils.send_email import get_admins_emails
from server.cshr.utils.send_email import get_supervisor_dict

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
def send_email_for_vacation_request(user, data):
    from django.core.mail import send_mail

    admins_emails = get_admins_emails()
    supervisor_dict: Dict = get_supervisor_dict(user)
    user_email = user.email
    msg = "Request information: \n Applying user: {user_fname} {user_lname} \n \
            Approving user: {supervisor_fname} {supervisor_lname} \n \
            Reason: {reason} \n Start date : {start_date} \n End Date : {end_date} \n \
            Status :{status} \n Request Url: {request_url}".format(
        user_fname=user.first_name,
        user_lname=user.last_name,
        supervisor_fname=supervisor_dict["fname"],
        supervisor_lname=supervisor_dict["lname"],
        reason=data["reason"],
        start_date=data["from_date"],
        end_date=data["end_date"],
        status=data["status"],
        request_url="dummyurl.com",
    )
    mail_title = "vacation request"
    send_mail(
        mail_title, msg, settings.EMAIL_HOST_USER, admins_emails, fail_silently=False
    )
    send_mail(
        mail_title,
        msg,
        settings.EMAIL_HOST_USER,
        [user_email, supervisor_dict["email"]],
        fail_silently=False,
    )


@shared_task
def send_email_for_hr_letter_request(user: User, data):
    from django.core.mail import send_mail

    admins_emails = get_admins_emails()
    supervisor_dict: Dict = get_supervisor_dict(user)
    user_email = user.email
    msg = "Request information: \n Applying user: {user_fname} {user_lname} \n \
        Approving user: {supervisor_fname} {supervisor_lname} \n \
        Addresses : {addresses} \n  \
        Status :{status} \n Request Url: {request_url}".format(
        user_fname=user.first_name,
        user_lname=user.last_name,
        supervisor_fname=supervisor_dict["fname"],
        supervisor_lname=supervisor_dict["lname"],
        addresses=data["addresses"],
        status=data["status"],
        request_url="dummyurl.com",
    )
    mail_title = "Hr Letter request"

    send_mail(
        mail_title, msg, settings.EMAIL_HOST_USER, admins_emails, fail_silently=False
    )
    send_mail(
        mail_title,
        msg,
        settings.EMAIL_HOST_USER,
        [user_email, supervisor_dict["email"]],
        fail_silently=False,
    )


@shared_task()
def send_email_for_compensation_request(user, data):
    from django.core.mail import send_mail

    admins_emails = get_admins_emails()
    supervisor_dict: Dict = get_supervisor_dict(user)
    user_email = user.email
    msg = " Request information: \n Applying user: {user_fname} {user_lname} \n \
            Approving user: {supervisor_fname} {supervisor_lname} \n \
            Reason: {reason} \n Start date : {start_date} \n End Date : {end_date} \n \
            Status :{status} \n Request Url: {request_url}".format(
        user_fname=user.first_name,
        user_lname=user.last_name,
        supervisor_fname=supervisor_dict["fname"],
        supervisor_lname=supervisor_dict["lname"],
        reason=data["reason"],
        start_date=data["from_date"],
        end_date=data["end_date"],
        status=data["status"],
        request_url="dummyurl.com",
    )
    mail_title = "Compensation request"

    send_mail(
        mail_title, msg, settings.EMAIL_HOST_USER, admins_emails, fail_silently=False
    )
    send_mail(
        mail_title,
        msg,
        settings.EMAIL_HOST_USER,
        [user_email, supervisor_dict["email"]],
        fail_silently=False,
    )


@shared_task()
def send_email_for_vacation_reply(user, data):
    from django.core.mail import send_mail

    admins_emails = get_admins_emails()
    supervisor_dict: Dict = get_supervisor_dict(user)
    user_email = user.email
    msg = "Request information: \n Applying user: {user_fname} {user_lname} \n \
            Approving user: {supervisor_fname} {supervisor_lname}\n \
            Reason: {reason} \n Start date : {start_date} \n End Date : {end_date} \n \
            Status :{status} \n Request Url: {request_url}".format(
        user_fname=user.first_name,
        user_lname=user.last_name,
        supervisor_fname=supervisor_dict["fname"],
        supervisor_lname=supervisor_dict["lname"],
        reason=data["reason"],
        start_date=data["from_date"],
        end_date=data["end_date"],
        status=data["status"],
        request_url="dummyurl.com",
    )
    mail_title = "Vacation reply"

    send_mail(
        mail_title, msg, settings.EMAIL_HOST_USER, admins_emails, fail_silently=False
    )
    send_mail(
        mail_title,
        msg,
        settings.EMAIL_HOST_USER,
        [user_email, supervisor_dict["email"]],
        fail_silently=False,
    )


@shared_task()
def send_email_for_hr_letter_reply(user, data):
    from django.core.mail import send_mail

    admins_emails = get_admins_emails()
    supervisor_dict: Dict = get_supervisor_dict(user)
    user_email = user.email
    msg = " Reply information: \n Applying user: {user_fname} {user_lname} \n \
            Approving user: {supervisor_fname} {supervisor_lname} \n \
            Addresses : {addresses} \n \
            Status :{status} \n Request Url: {request_url}".format(
        user_fname=user.first_name,
        user_lname=user.last_name,
        supervisor_fname=supervisor_dict["fname"],
        supervisor_lname=supervisor_dict["lname"],
        addresses=data["addresses"],
        status=data["status"],
        request_url="dummyurl.com",
    )
    mail_title = "Hr Letter reply"

    send_mail(
        mail_title, msg, settings.EMAIL_HOST_USER, admins_emails, fail_silently=False
    )
    send_mail(
        mail_title,
        msg,
        settings.EMAIL_HOST_USER,
        [user_email, supervisor_dict["email"]],
        fail_silently=False,
    )


@shared_task()
def send_email_for_compensation_reply(user, data):
    from django.core.mail import send_mail

    admins_emails = get_admins_emails()
    supervisor_dict: Dict = get_supervisor_dict(user)
    user_email = user.email
    msg = "Reply information: \n Applying user: {user_fname} {user_lname} \n \
            Approving user: {supervisor_fname} {supervisor_lname} \n \
            Reason: {reason} \n Start date : {start_date} \n End Date : {end_date} \n \
            Status :{status} \n Request Url: {request_url}".format(
        user_fname=user.first_name,
        user_lname=user.last_name,
        supervisor_fname=supervisor_dict["fname"],
        supervisor_lname=supervisor_dict["lname"],
        reason=data["reason"],
        start_date=data["from_date"],
        end_date=data["end_date"],
        status=data["status"],
        request_url="dummyurl.com",
    )
    mail_title = "Compensation reply"

    send_mail(
        mail_title, msg, settings.EMAIL_HOST_USER, admins_emails, fail_silently=False
    )
    send_mail(
        mail_title,
        msg,
        settings.EMAIL_HOST_USER,
        [user_email, supervisor_dict["email"]],
        fail_silently=False,
    )