from cpwebapi import session, oauth_utils
from apscheduler.schedulers.background import BackgroundScheduler
import requests
import datetime
import json
import logging

"""  
1.api.ibkr.com & 2.api.ibkr.com = New Jersey
3.api.ibkr.com & 4.api.ibkr.com = Chicago
5.api.ibkr.com & 6.api.ibkr.com = Hong Kong
7.api.ibkr.com & 8.api.ibkr.com = Zug
"""

with open("config.json", "r") as config_file:
    oauth_config = json.load(config_file, object_hook=oauth_utils.oauth_config_hook)
oauth_session = session.OAuthSession(oauth_config, host="api.ibkr.com")
while True:
    # Check if the session is authenticated before starting the scheduler
    auth_status: requests.Response = oauth_session.auth_status()
    if auth_status.status_code == 200:
        break
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s; %(levelname)s; %(message)s",
    filename=f"./logs/cpwebapi_{datetime.datetime.now().strftime('%Y%m%d')}.log",
    filemode="a",
)
apscheduler_log = logging.getLogger("apscheduler")
apscheduler_log.setLevel(logging.WARNING)


def job_wrapper(job_func, *args, **kwargs):
    def wrapper():
        start_time = datetime.datetime.utcnow()
        response: requests.Response = job_func(*args, **kwargs)
        logging.info(
            "endpoint: %s; status_code: %s; response_time: %sms; request_time: %s",
            response.url,
            response.status_code,
            response.elapsed.total_seconds() * 1000,
            start_time,
        )

    return wrapper


@job_wrapper
def call_tickle() -> requests.Response:
    return oauth_session.tickle()


@job_wrapper
def call_auth_status() -> requests.Response:
    return oauth_session.auth_status()


scheduler = BackgroundScheduler()
scheduler.add_job(call_tickle, "interval", seconds=30)
scheduler.add_job(call_auth_status, "interval", seconds=30)
scheduler.start()

try:
    while True:
        pass
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()
    pass
