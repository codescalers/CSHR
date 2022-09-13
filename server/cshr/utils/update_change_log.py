"""This file has change_log_update function."""
from server.cshr.models.users import User
from server.cshr.models.vacations import Vacation

from typing import List, Dict
import datetime 



def update_vacation_change_log(
        vacation: Vacation,
        approved_date: datetime.datetime,
        comment: List[Dict]
    ):
    tmp =vacation.change_log
    change: Dict = {}
    change['approved_user'] = vacation.approval_user
    change['approved_date'] = approved_date
    change['comments'] = []
    print(comment)
    change['comments'].append(comment)
    print(change)
    list(tmp).append(change)
    vacation.change_log=tmp
    print(vacation.change_log)
    vacation.save()
    return change
