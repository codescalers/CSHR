"""This file has change_log_update function."""
from server.cshr.models.vacations import Vacation
from typing import List, Dict


def update_vacation_change_log(vacation: Vacation, comment: List[Dict]) -> Vacation:
    print(vacation, vacation.change_log, comment)
    vacation.change_log.append(comment)
    vacation.save()
    return vacation
