import re
import os
import datetime

from nepali_date import NepaliDate

from get_event import GetPageContent
from set_event import SetSlackStatus


TODAY = NepaliDate.today().isoformat()

DOMAIN = 'www.hamropatro.com'
PATH = "/date/{0}".format(
            re.sub(r"\b0", "", TODAY)
        )
TAG = 'title'


AUTHORIZATION = os.getenv('BEARER_AUTH_KEY', None)


def get_left_time():
    today_date = datetime.datetime.combine(
        datetime.date.today(), datetime.datetime.max.time()
    )

    epoch = datetime.datetime.utcfromtimestamp(0)
    total_utc = (today_date - epoch).total_seconds()

    return total_utc + datetime.timedelta(hours=-5, minutes=-45).total_seconds()

def set_my_slack_status():
    page_content = GetPageContent(
        DOMAIN,
        PATH,
        TAG
    )
    title = re.sub(
        r" \| Hamro Patro",
        '',
        page_content.get_tag_content()
    )
    if not AUTHORIZATION:
        raise Exception("Authorization key not found")

    print(get_left_time())

    setStatus = SetSlackStatus(
        "Bearer %s" % AUTHORIZATION,
        str(title),
        status_expiration = get_left_time()
    )

    return setStatus.set_status()

set_my_slack_status()
