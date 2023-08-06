import types
from typing import Any, Dict, List, Tuple, TYPE_CHECKING

import ulid

from kolo.serialize import serialize_function_args, serialize_function_kwargs


if TYPE_CHECKING:
    # Literal and TypedDict only exist on python 3.8+
    # We run mypy using a high enough version, so this is ok!
    from typing import Literal, TypedDict

    class CeleryJob(TypedDict, total=False):
        frame_id: str
        name: str
        args: Tuple[Any, ...]
        kwargs: Dict[str, Any]
        type: Literal["background_job", "celery_job"]
        subtype: Literal["celery"]


class CeleryFilter:
    co_names = ["apply_async"]

    def __init__(self, config) -> None:
        self.config = config
        self.use_frames_of_interest = True

    def __call__(self, frame: types.FrameType, event: str, arg: object) -> bool:
        filepath = frame.f_code.co_filename
        return (
            "celery" in filepath
            and "sentry_sdk" not in filepath
            and "apply_async" in frame.f_code.co_name
        )

    def process(
        self,
        frame: types.FrameType,
        event: str,
        arg: object,
        call_frame_ids: List[Dict[str, str]],
    ):
        if event == "return":
            return

        frame_locals = frame.f_locals
        task_name = frame_locals["self"].name
        task_args = serialize_function_args(frame_locals["args"])
        task_kwargs = serialize_function_kwargs(frame_locals["kwargs"])

        return {
            "frame_id": f"frm_{ulid.new()}",
            "name": task_name,
            "args": task_args,
            "kwargs": task_kwargs,
            "type": "background_job",
            "subtype": "celery",
        }
