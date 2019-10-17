import re
import os

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

    setStatus = SetSlackStatus(
        "Bearer %s" % AUTHORIZATION,
        str(title)
    )

    return setStatus.set_status()

set_my_slack_status()
