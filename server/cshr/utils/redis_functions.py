from typing import Dict
from django.utils.dateparse import parse_datetime
from django.core.exceptions import ImproperlyConfigured
from cshr.models.requests import TYPE_CHOICES
from cshr.models.users import USER_TYPE, User
from cshr.serializers.users import TeamSerializer
from cshr.services.users import get_user_by_id
from components import config
import redis
import json

from cshr.api.response import CustomResponse

try:
    _, R_HOST, R_PORT = config("REDIS_HOST").replace("//", "").split(":")
except Exception:
    raise ImproperlyConfigured("REDIS_HOST is not defined")

redis_instance = redis.StrictRedis(host=R_HOST, port=R_PORT, db=0)


def set_notification_request_redis(data: Dict) -> bool:
    """this function set requests notifications"""
    applying_user = None
    if type(data.get("applying_user")) is not int and data.get("applying_user").get(
        "id"
    ):
        applying_user = data["applying_user"]["id"]
    else:
        applying_user = data["applying_user"]
    user = get_user_by_id(applying_user)
    title = "applying for " + data["type"]
    created_at = parse_datetime(str(data["created_at"]))

    sending_data: Dict = {
        "created_at": f"{created_at.date()} | {created_at.time().hour}:{created_at.time().minute}",
        "title": title,
        "type": data["type"],
        "event_id": str(data["id"]),
        "user": json.dumps(TeamSerializer(user).data),
    }
    if (
        sending_data.get("type") == TYPE_CHOICES.COMPENSATION
        or sending_data.get("type") == TYPE_CHOICES.HR_LETTERS
        or sending_data.get("type") == TYPE_CHOICES.OFFICIAL_DOCUMENT
    ):
        admins: User = User.objects.filter(user_type=USER_TYPE.ADMIN)
        for admin in admins:
            hashname = "user" + str(admin.id) + ":" + data["type"] + str(data["id"])
            redis_instance.hmset(hashname, sending_data)
            redis_instance.expire(hashname, 30 * 3600 * 24)
    else:
        approving_users = user.reporting_to.all()
        for approving_user in approving_users:
            hashname = (
                "user" + str(approving_user.id) + ":" + data["type"] + str(data["id"])
            )
            redis_instance.hmset(hashname, sending_data)
            redis_instance.expire(hashname, 30 * 3600 * 24)
    return True


def set_notification_reply_redis(data: Dict, state: str, event_id: int):
    """this function set accept notifications"""
    approving_user = data.approval_user
    title = f"Your {data.type} request was {state} by {approving_user.full_name}"
    created_at = parse_datetime(str(data.created_at))
    sending_data: Dict = {
        "created_at": f"{created_at.date()} | {created_at.time().hour}:{created_at.time().minute}",
        "title": title,
        "type": data.type,
        "event_id": event_id,
        "user": json.dumps(TeamSerializer(approving_user).data),
    }
    applying_user = data.applying_user
    hashname = "user" + str(applying_user.id) + ":" + data.type + str(data.id)
    redis_instance.hmset(hashname, sending_data)
    return True


def notification_commented(data: Dict, user, state: str, event_id: int):
    """this function set accept notifications"""
    commented_user: User = None
    hashname: str = None

    if user == data.approval_user:
        commented_user = data.approval_user
        title = f"Your {data.type} request was {state} by {commented_user.full_name}"
        hashname = "user" + str(data.approval_user.id) + ":" + data.type + str(data.id)
    elif user == data.applying_user:
        commented_user = data.applying_user
        title = f"Your approving {data.type} request was {state} by {commented_user.full_name}"
        hashname = "user" + str(data.applying_user.id) + ":" + data.type + str(data.id)
    else:
        commented_user = user
        title = f"Your {data.type} request was {state} by  {commented_user.full_name}"
        hashname = "user" + str(data.applying_user.id) + ":" + data.type + str(data.id)

    created_at = data.created_at
    sending_data: Dict = {
        "created_at": f"{created_at.date()} | {created_at.time().hour}:{created_at.time().minute}",
        "title": title,
        "type": data.type,
        "event_id": event_id,
        "user": json.dumps(TeamSerializer(commented_user).data),
    }
    if hashname is None:
        return False
    redis_instance.hmset(hashname, sending_data)
    return True


# def get_notifications(user: User):
#     """
#     Retrieve all notifications for a specific user.

#     Args:
#         user (User): The user for whom notifications are to be retrieved.

#     Returns:
#         list: A list of dictionaries containing notification data.
#     """
#     notifications = []
#     keys = redis_instance.keys("user" + str(user.id) + "*")

#     for key in keys:
#         val = redis_instance.hgetall(key)
#         dval = dict((k.decode("utf8"), v.decode("utf8")) for k, v in val.items())

#         # Parse notification data
#         noti_user_id = json.loads(dval.get("user"))["id"]
#         noti_id = int(json.loads(dval.get("event_id")))

#         # Check if the user associated with the notification exists
#         try:
#             usernt = User.objects.get(id=noti_user_id)
#             dval["user"] = BaseUserSerializer(usernt).data
#         except User.DoesNotExist:
#             redis_instance.delete(key)

#         # Check if the request associated with the notification exists
#         try:
#             Requests.objects.get(id=noti_id)
#         except Requests.DoesNotExist:
#             redis_instance.delete(key)

#         notifications.append(dval)

#     return notifications


# def sort_notifications_by_created_at(notifications):
#     # Custom key function to extract timestamp from the notification
#     def get_timestamp(notification):
#         created_at_str = notification["created_at"]
#         # Parse the timestamp string and convert it to datetime object
#         return datetime.strptime(created_at_str, "%Y-%m-%d | %H:%M")

#     # Sort the notifications based on the created_at timestamp
#     sorted_notifications = sorted(notifications, key=get_timestamp, reverse=True)
#     return sorted_notifications


def ping_redis():
    try:
        redis_instance.ping()
    except Exception:
        raise redis.ConnectionError(
            "Redis is not running, please make sure that you run the redis server on the provided values."
        )


def get_redis_conf() -> Dict[str, str]:
    return {"host": R_HOST, "port": R_PORT}


def http_ensure_redis_error():
    return CustomResponse.bad_request(
        message="Connection Refused",
        error={
            "message": "Redis is not running, please make sure that you run the Redis server on the provided values",
            "values": {"host": R_HOST, "port": R_PORT},
        },
    )
