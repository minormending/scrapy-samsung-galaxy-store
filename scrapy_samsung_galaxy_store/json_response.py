import json
from typing import Any, Dict, List
from scrapy.http import Response


class JsonResponse(Response):
    def __init__(self, jobject: List[Any] | Dict[Any, Any], **kwargs):
        super().__init__(**kwargs)
        self.jobject: List[Any] | Dict[Any, Any] = jobject
        self.jtext: str = None

    @property
    def text(self):
        if self.jtext is None:
            self.jtext: str = json.dumps(self.jobject)
        return self.jtext

    def json(self):
        return self.jobject
