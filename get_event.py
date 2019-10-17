import http.client
import datetime
import re


class GetPageContent:
    def __init__(self, domain, url, tag, **kwargs):
        self.domain = domain
        self.url = url
        self.tag = tag
        self.kwargs = kwargs
    
    def _get_response(self):
        conn = http.client.HTTPSConnection(self.domain)
        conn.request("GET", self.url)

        res = conn.getresponse()
        if not res.status == 200:
            return None

        return res.read().decode(self.kwargs.get('encoding', "utf-8"))
    
    def get_tag_content(self):
        if not self._get_response():
            raise Exception("Data not found")
        
        tag_data = re.search(
            re.escape("<%s>" % self.tag) + r"(.*?)" + re.escape("</%s>" % self.tag),
            self._get_response()
        )

        if not tag_data:
            raise Exception("Could not found event")

        return tag_data.group(1)
