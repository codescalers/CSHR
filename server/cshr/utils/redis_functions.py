import datetime
from time import strptime
from typing import Dict
from django.utils.dateparse import parse_datetime
import redis
import json
from django.core.exceptions import ImproperlyConfigured
from server.components import config
from server.cshr.models.users import User
from server.cshr.serializers.users import TeamSerializer
from server.cshr.services.users import get_user_by_id


if config("REDIS_HOST_ONLY") is None:
    raise ImproperlyConfigured("REDIS_HOST_ONLY is not defined")

if config("REDIS_PORT") is None:
    raise ImproperlyConfigured("REDIS_PORT is not defined")

redis_instance = redis.StrictRedis(
    host=config("REDIS_HOST_ONLY"), port=config("REDIS_PORT"), db=0
)


def set_notification_request_redis(data: Dict) -> bool:
    """this function set requests notifications"""
    user = get_user_by_id(data["applying_user"])
    title = "applying for " + data["type"]
    created_at = parse_datetime(data["created_at"])

    sending_data: Dict = {
        "created_at": f'{created_at.date()} | {created_at.time().hour}:{created_at.time().minute}',
        "title": title,
        "type": data["type"],
        "event_id": str(data["id"]),
        "user": json.dumps(TeamSerializer(user).data)
    }
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
    created_at = parse_datetime(data.created_at)
    sending_data: Dict = {
        "created_at": f'{created_at.date()} | {created_at.time().hour}:{created_at.time().minute}',
        "title": title,
        "type": data.type,
        "event_id": event_id,
        "user": json.dumps(TeamSerializer(approving_user).data)
    }
    applying_user = data.applying_user
    hashname = "user" + str(applying_user.id) + ":" + data.type + str(data.id)
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
