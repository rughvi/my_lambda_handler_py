import json
import logging
import os

from botocore.exceptions import ClientError
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
ALLOWABLE_EVENT_AGE = timedelta(minutes=float(os.environ['ALLOWABLE_EVENT_AGE']))

def lambda_handler(event, context) -> bool:
    print("test_handler called")
    now = datetime.utcnow().replace(tzinfo=timezone.utc)
    if is_too_old(event, now):
        logger.warning(f"Discarding event as it is too old {json.dumps(event)}")
        return False

    return True

def is_too_old(event:dict, now: datetime) -> bool:
    event_time = event.get("time", "")
    if event_time:
        try:
            time = datetime.strptime(event_time, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
            return time < now - ALLOWABLE_EVENT_AGE
        except ValueError as err:
            logger.error(f"Unable to parse the time from event : {json.dumps(event)}")
            raise err

    return False

