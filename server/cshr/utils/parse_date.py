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

class CSHRDate:
    def __init__(self, date: Dict) -> None:
        self.date = date
        self.required_fields: List = ["year", "month", "day", "hour", "minute"]

    def no_provided_date(self):
        return CustomResponse.bad_request(
            error=[{"required_fields": {"date": {"required": True, "type": "dict"}}}],
            message="You must provide date field and must follow this pattern {}".format(
                self.required_fields
            ),
        )

    def wrong_provided_date(self):
        return CustomResponse.bad_request(
            error=[{"required_fields": {"date": {"required": True, "type": "dict"}}}],
            message="You must provide date field as dict type and must follow this pattern {}".format(
                self.required_fields
            ),
        )

    def error(self):
        provided_fields: List = []
        for field in self.required_fields:
            if field not in self.date.keys():
                provided_fields.append(field)
        return CustomResponse.bad_request(
            error=[
                {
                    "required_fields": {
                        "date": {
                            "required": True,
                            "type": "dict",
                            "must_provided_fields": provided_fields,
                        }
                    }
                }
            ],
            message="Please make sure that your date field containes {}".format(
                self.required_fields
            ),
        )

    def parse(self) -> datetime:
        """This function takes a dict and returns a datetime inctance."""
        if self.date is None:
            return self.no_provided_date()
        elif type(self.date) != dict:
            return self.wrong_provided_date()
        else:
            if (
                self.date.get("year")
                and self.date.get("month")
                and self.date.get("day")
                and self.date.get("hour")
                and self.date.get("minute")
            ):
                parsing: datetime = datetime(
                    year=self.date.get("year"),
                    month=self.date.get("month"),
                    day=self.date.get("day"),
                    hour=self.date.get("hour"),
                    minute=self.date.get("minute"),
                )
                return parsing
            return self.error()
