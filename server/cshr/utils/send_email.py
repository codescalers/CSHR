from server.cshr.models.users import User
from server.cshr.models.users import USER_TYPE
from typing import Dict
from django.core.mail import send_mail


def get_admins_emails():
    """ "this function return array of admins emails"""
    admins = User.objects.filter(user_type=USER_TYPE.ADMIN)
    admins_emails = []
    for admin in admins:
        admins_emails.append(admin.email)
    return admins_emails


def get_supervisor_emails(user: User):
    """ "this function return array of supervisor emails"""
    supervisors = user.reporting_to.all()
    supervisor_emails = []
    for super in supervisors:
        supervisor = User.objects.get(pk=super.id)
        supervisor_emails.append(supervisor.email)
    return supervisor_emails


def send_email(mail_title, msg, host_user, recievers):
    for reciever in recievers:
        send_mail(mail_title, msg, host_user, reciever, fail_silently=False)


def get_supervisor_dict(user: User) -> Dict:
    """this function return dictionary with supervisor fname , lname and email"""
    try:
        supervisor = User.objects.get(pk=user.reporting_to.id)
        supervisor_email = supervisor.email
        supervisor_fn = supervisor.fname
        supervisor_ln = supervisor.lname
    except Exception:
        supervisor_email = ""
        supervisor_fn = "Not"
        supervisor_ln = "Defined"

    supervisor_dict: Dict = {}
    supervisor_dict["email"] = supervisor_email
    supervisor_dict["fname"] = supervisor_fn
    supervisor_dict["lname"] = supervisor_ln
    return supervisor_dict
