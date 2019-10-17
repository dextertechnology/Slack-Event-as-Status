import json
import http.client


class SetSlackStatus:
    def __init__(self, authorization, status_text, **kwargs):
        self.authorization = authorization
        self.status_text = status_text
        self.kwargs = kwargs
        self.responsee = ""

    def _initialize_header(self):
        return {
            'authorization': self.authorization,
            'content-type': self.kwargs.get('content-type', 'application/json; charset=utf-8'),
            'cache-control': self.kwargs.get('cache-control', 'no-cache'),
        }

    def set_status(self):
        payload = {
            "profile": {
                "status_text": self.status_text,
                "status_emoji": self.kwargs.get('status_emoji', ""),
                "status_expiration": self.kwargs.get('status_expiration', 0)
            }
        }

        conn = http.client.HTTPSConnection("slack.com")

        conn.request(
            "POST",
            "/api/users.profile.set",
            json.dumps(payload),
            self._initialize_header()
        )

        res = conn.getresponse()

        if res:
            self.responsee = res.read().decode("utf-8")
            return "Successfully updated"
