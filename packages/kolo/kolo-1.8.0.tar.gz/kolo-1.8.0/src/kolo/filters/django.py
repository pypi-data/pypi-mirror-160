import os
import time
import types
from typing import Dict, List

import ulid

from ..serialize import get_content, get_request_body


class DjangoFilter:
    use_frames_of_interest = False
    co_names = ["get_response"]

    def __init__(self, config) -> None:
        self.config = config
        self.timestamp: float

    def __call__(self, frame: types.FrameType, event: str, arg: object) -> bool:
        co_name = frame.f_code.co_name
        filename = frame.f_code.co_filename
        return (
            co_name == "get_response"
            and os.path.normpath("/kolo/middleware.py") in filename
        )

    def process(
        self,
        frame: types.FrameType,
        event: str,
        arg: object,
        call_frame_ids: List[Dict[str, str]],
    ):
        if event == "call":
            self.timestamp = time.time()
            request = frame.f_locals["request"]
            self.request_data = {
                "frame_id": f"frm_{ulid.new()}",
                "scheme": request.scheme,
                "method": request.method,
                "path_info": request.path_info,
                "body": get_request_body(request),
                "headers": dict(request.headers),
                "url_pattern": None,
                "type": "django_request",
            }
            return self.request_data
        elif event == "return":  # pragma: no branch
            duration = time.time() - self.timestamp
            ms_duration = round(duration * 1000, 2)

            request = frame.f_locals["request"]
            match = request.resolver_match
            if match:  # match is None if this is a 404
                self.request_data["url_pattern"] = {
                    "namespace": match.namespace,
                    "route": match.route,
                    "url_name": match.url_name,
                    "view_qualname": match._func_path,
                }

            response = frame.f_locals["response"]
            return {
                "frame_id": f"frm_{ulid.new()}",
                "ms_duration": ms_duration,
                "status_code": response.status_code,
                "content": get_content(response),
                "headers": dict(response.items()),
                "type": "django_response",
            }
