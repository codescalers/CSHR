from server.cshr.models.notifications import Notifications


def get_notification_by_id(id: str) -> Notifications:
    """Return notification who have the same id"""
    try:
        return Notifications.objects.get(id=int(id))
    except Notifications.DoesNotExist:
        return None


def get_all_notiifications() -> Notifications:
    """Return all notiifications"""
    return Notifications.objects.all()


def last_20_notifications(user_id: int) -> Notifications:
    """Return last 20 notifications"""
    return (
        Notifications.objects.get(creator_user=user_id)
        .order_by("-timestamp")
        .all()[:20]
    )
