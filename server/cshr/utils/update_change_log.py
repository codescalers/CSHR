"""This file has change_log_update function."""
from server.cshr.models.vacations import Vacation

from typing import List, Dict
import datetime


def update_vacation_change_log(
    vacation: Vacation,
    approved_date: str(datetime.datetime.today()),
    comment: List[Dict],
):
    change = vacation.change_log

    change["approved_user"] = vacation.approval_user.id
    change["approved_date"] = approved_date

    if vacation.change_log.__contains__("comments"):

        change["comments"].append(comment)
    else:
        change["comments"] = [comment]

    vacation.save()
    return change


def update_vacation_comment_log(vacation: Vacation, comment: List[Dict]):
    change = vacation.change_log
    if vacation.approval_user is not None:
        change["approved_user"] = vacation.approval_user.id

    print(vacation.approval_user)

    if vacation.change_log.__contains__("comments"):

        change["comments"].append(comment)
    else:
        change["comments"] = [comment]
    vacation.save()
    return change
