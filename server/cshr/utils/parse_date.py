"""This file containes parse date function that takes an obj and returns a datetime inctance."""
from typing import Dict, List
from datetime import datetime, timedelta

from server.cshr.api.response import CustomResponse


def get_dates_between_two_dates(start_date, end_date):
    dates_list = []
    current_date = start_date

    # Loop through the dates from start_date to end_date
    while current_date <= end_date:
        dates_list.append(current_date)
        current_date += timedelta(days=1)

    return dates_list
