import os
from typing import Any, Dict

import ulid


class UnitTestFilter:
    use_frames_of_interest = False
    event_types = {
        "startTest": "start_test",
        "stopTest": "end_test",
    }
    co_names = list(event_types)

    def __init__(self, config) -> None:
        self.config = config

    def __call__(self, frame, event, arg):
        filepath = frame.f_code.co_filename
        co_name = frame.f_code.co_name
        return (
            event == "call"
            and os.path.normpath("unittest/result.py") in filepath
            and co_name in self.event_types
        )

    def process(self, frame, event, arg, call_frame_ids):  # pragma: no cover
        co_name = frame.f_code.co_name
        testcase = frame.f_locals["test"]
        return {
            "frame_id": f"frm_{ulid.new()}",
            "type": self.event_types[co_name],
            "test_name": testcase._testMethodName,
            "test_class": testcase.__class__.__qualname__,
        }
