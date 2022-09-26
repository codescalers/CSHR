import redis
from django.core.exceptions import ImproperlyConfigured
from server.components import config
from server.cshr.models.users import User
from server.cshr.services.users import get_user_by_id


if config("REDIS_HOST_ONLY") is None:
    raise ImproperlyConfigured("REDIS_HOST_ONLY is not defined")

if config("REDIS_PORT") is None:
    raise ImproperlyConfigured("REDIS_PORT is not defined")

redis_instance = redis.StrictRedis(
    host=config("REDIS_HOST_ONLY"), port=config("REDIS_PORT"), db=0
)


def set_notification_request_redis(data, url):
    """this function set requests notifications"""
    user = get_user_by_id(data["applying_user"])
    if user is None:
        print("user is not founddd!!!!!!")
    title = user.first_name + " " + user.last_name + " is applying for " + data["type"]
    dict = {"title": title, "url": url}
    approving_users = user.reporting_to.all()
    for approving_user in approving_users:
        hashname = (
            "user" + str(approving_user.id) + ":" + data["type"] + str(data["id"])
        )
        redis_instance.hmset(hashname, dict)


def set_notification_reply_redis(data, state, url):
    """this function set accept notifications"""
    approving_user = data.approval_user
    title = (
        approving_user.first_name
        + " "
        + approving_user.last_name
        + " "
        + state
        + "your "
        + data.type
        + " request"
    )
    dict = {"title": title, "url": url}
    applying_user = data.applying_user
    hashname = "user" + str(applying_user.id) + ":" + data.type + str(data.id)
    redis_instance.hmset(hashname, dict)


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
