"""This file has change_log_update function."""
import json
from server.cshr.models.users import User
from server.cshr.models.vacations import Vacation

from typing import List, Dict
import datetime 



def update_vacation_change_log(
        vacation: Vacation,
        approved_date: str(datetime.datetime.today()),
        comment: List[Dict]
    ):
    change =vacation.change_log
    # change: Dict = {}
    change['approved_user'] = vacation.approval_user.id
    change['approved_date'] = approved_date
    if vacation.change_log.__contains__('comments'):

      change['comments'].append(comment)
    else:
        change['comments']= [comment]

    # print(comment)
    # change['comments'].append(comment)
    print(change['comments'])
    print(change)
    # tmp.append(change)
    # print(type(tmp))
    # print(tmp)
    # vacation.change_log=json.loads(json.dumps(tmp))
    print(vacation.change_log)
    vacation.save()
    return change
