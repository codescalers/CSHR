from server.cshr.models.users import User
from server.cshr.models.users import USER_TYPE
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from server.cshr.services.users import get_user_by_id
from django.core.exceptions import ObjectDoesNotExist


def get_admins_emails():
    """this function return array of admins emails"""
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
        supervisor = get_user_by_id(super.id)
        if supervisor is None:
            raise ObjectDoesNotExist("Invalid supervisor ID")
        supervisor_emails.append(supervisor.email)
    return supervisor_emails


def get_email_recievers(user: User):
    admins_emails = get_admins_emails()
    supervisor_emails = get_supervisor_emails(user)
    recievers = admins_emails + supervisor_emails
    recievers.append(user.email)
    return recievers


def check_email_configuration():
    arr = [
        settings.EMAIL_HOST_PASSWORD,
        settings.EMAIL_HOST_USER,
        settings.EMAIL_PORT,
        settings.EMAIL_HOST,
    ]
    for item in arr:
        if item == "":
            raise ImproperlyConfigured("%s is not configured correctly" % (item))
