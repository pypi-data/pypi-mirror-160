from datetime import datetime, timezone
from dateutil import parser


def avoid_infinite_retries(timestamp, event_id, max_age_ms=600000):
    """
    Take timestamp, event id and max age in ms.
    Drop the deployment, return None, if event age is greater than given max age in ms.
    """
    # get event age in ms
    event_time = parser.parse(timestamp)
    event_age = (datetime.now(timezone.utc) - event_time).total_seconds()
    event_age_ms = event_age * 1000

	# Ignore events that are too old
    if event_age_ms > max_age_ms:
        print(f'Dropped {event_id} (age {event_age_ms} ms)')
        return None
