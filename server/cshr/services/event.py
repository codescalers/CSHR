from server.cshr.models.event import Event


def get_event_by_id(id: str) -> Event:
    """Return event who have the same id"""
    try:
        return Event.objects.get(id=int(id))
    except Event.DoesNotExist:
        return None


def get_all_events() -> Event:
    """Return all events"""
    return Event.objects.all()
