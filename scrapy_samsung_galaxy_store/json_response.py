import json
from typing import Any, Dict, List
from scrapy import signals, Spider
from scrapy.http import Request, Response

class JsonResponse(Response):
    def __init__(
        self,
        url: str,
        jobject: List[Any] | Dict[Any, Any],
        status: int=200,
        headers: Dict[str, Any]=None,
        body=b"",
        flags=None,
        request=None,
        certificate=None,
        ip_address=None,
        protocol=None,
    ):
        super().__init__(
            url,
            status,
            headers,
            body,
            flags,
            request,
            certificate,
            ip_address,
            protocol,
        )
        self.jobject = jobject
        self.jtext = None

    @property
    def text(self):
        if self.jtext is None:
            self.jtext: str = json.dumps(self.jobject)
        return self.jtext

    def json(self):
        return self.jobject