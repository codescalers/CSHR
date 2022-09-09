from server.cshr.models.users import User
from server.cshr.models.users import USER_TYPE
from typing import Dict


def get_admins_emails():
    """ "this function return array of admins"""
    admins = User.objects.filter(user_type=USER_TYPE.ADMIN)
    admins_emails = []
    for admin in admins:
        admins_emails.append(admin.email)
    return admins_emails


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
