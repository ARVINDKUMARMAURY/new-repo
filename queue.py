import random
from config import QUEUE_LIMIT

# chat_id -> list of song dicts
# song dict = {"title": str, "vidid": str, "duration": str, "requested_by": str, "video": bool}
_QUEUES = {}


def get_queue(chat_id: int):
    return _QUEUES.get(chat_id, [])


def queue_full(chat_id: int) -> bool:
    return len(get_queue(chat_id)) >= QUEUE_LIMIT


def add_to_queue(chat_id: int, song: dict) -> bool:
    """Returns False if queue limit reached, else adds and returns True."""
    if queue_full(chat_id):
        return False
    _QUEUES.setdefault(chat_id, []).append(song)
    return True


def pop_next(chat_id: int):
    """Removes and returns the next song, or None if queue is empty."""
    q = _QUEUES.get(chat_id)
    if not q:
        return None
    song = q.pop(0)
    if not q:
        _QUEUES.pop(chat_id, None)
    return song


def clear_queue(chat_id: int):
    _QUEUES.pop(chat_id, None)


def shuffle_queue(chat_id: int) -> bool:
    q = _QUEUES.get(chat_id)
    if not q or len(q) < 2:
        return False
    random.shuffle(q)
    return True


def is_active(chat_id: int) -> bool:
    return chat_id in _QUEUES and len(_QUEUES[chat_id]) > 0
