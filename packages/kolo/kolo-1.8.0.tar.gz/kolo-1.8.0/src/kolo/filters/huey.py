import os
from typing import Any, Dict, List, Tuple, TYPE_CHECKING

import ulid

from kolo.serialize import serialize_function_args, serialize_function_kwargs


if TYPE_CHECKING:
    # Literal and TypedDict only exist on python 3.8+
    # We run mypy using a high enough version, so this is ok!
    from typing import Literal, TypedDict

    class HueyJob(TypedDict, total=False):
        frame_id: str
        name: str
        args: Tuple[Any, ...]
        kwargs: Dict[str, Any]
        type: Literal["background_job", "huey_job"]
        subtype: Literal["huey"]


class HueyFilter:
    use_frames_of_interest = False
    co_names = ["__init__"]

    def __init__(self, config) -> None:
        self.config = config

    def __call__(self, frame, event, arg):
        filepath = frame.f_code.co_filename
        co_name = frame.f_code.co_name
        if (
            event == "call"
            and co_name == "__init__"
            and os.path.normpath("/huey/api.py") in filepath
        ):
            from huey.api import Task

            return isinstance(frame.f_locals["self"], Task)
        return False

    def process(self, frame, event, arg, call_frame_ids):
        frame_locals = frame.f_locals
        task_object = frame_locals["self"]
        task_args = serialize_function_args(frame_locals["args"])
        task_kwargs = serialize_function_kwargs(frame_locals["kwargs"])

        return {
            "frame_id": f"frm_{ulid.new()}",
            "name": f"{task_object.__module__}.{task_object.name}",
            "args": task_args,
            "kwargs": task_kwargs,
            "type": "background_job",
            "subtype": "huey",
        }
