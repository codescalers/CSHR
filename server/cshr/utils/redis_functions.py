from typing import Dict
from django.utils.dateparse import parse_datetime
from django.core.exceptions import ImproperlyConfigured
from server.cshr.models.requests import TYPE_CHOICES
from server.cshr.models.users import USER_TYPE, User
from server.cshr.serializers.users import TeamSerializer
from server.cshr.services.users import get_user_by_id
from server.components import config
import redis
import json
import os


if os.environ.get("REDIS_HOST") is None:
    try:
        _, R_HOST, R_PORT = config("REDIS_HOST").replace("//", "").split(":")
    except Exception:
        raise ImproperlyConfigured("REDIS_HOST is not defined")
else:
    print(os.environ.get("DJANGO_DEBUG"))
    print(os.environ.get("REDIS_HOST"))
    print(os.environ.get("REDIS_HOST").replace("//", "").split(":"))
    _, R_HOST, R_PORT = os.environ.get("REDIS_HOST").replace("//", "").split(":")

redis_instance = redis.StrictRedis(host=R_HOST, port=R_PORT, db=0)


def set_notification_request_redis(data: Dict) -> bool:
    """this function set requests notifications"""
    applying_user = None
    if type(data["applying_user"]) != int and data.get("applying_user").get("id"):
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
        hashname = "user" + str(data.applying_user.id) + ":" + data.type + str(data.id)
    elif user == data.applying_user:
        commented_user = data.applying_user
        title = f"Your approving {data.type} request was {state} by {commented_user.full_name}"
        hashname = "user" + str(data.approval_user.id) + ":" + data.type + str(data.id)

    created_at = parse_datetime(data.created_at)
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


def get_notifications(user: User):
    """this function returns all notifications for certain user"""
    keys = redis_instance.keys("user" + str(user.id) + "*")
    notifications = []
    val = ""
    for key in keys:
        val = redis_instance.hgetall(key)
        dval = dict((k.decode("utf8"), v.decode("utf8")) for k, v in val.items())
        notifications.append(dval)
    return notifications
