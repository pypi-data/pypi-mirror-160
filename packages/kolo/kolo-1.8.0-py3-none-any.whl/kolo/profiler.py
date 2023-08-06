import inspect
import json
import logging
import sys
import time
import types
from contextlib import contextmanager
from functools import wraps
from pathlib import Path
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    TypeVar,
    TYPE_CHECKING,
    cast,
)

import ulid

from .db import load_config, save_invocation_in_sqlite
from .filters.attrs import attrs_filter
from .filters.celery import CeleryFilter
from .filters.core import (
    build_frame_filter,
    exec_filter,
    frozen_filter,
    import_filter,
    library_filter,
)
from .filters.django import DjangoFilter
from .filters.exception import ExceptionFilter
from .filters.huey import HueyFilter
from .filters.kolo import kolo_filter
from .filters.logging import LoggingFilter
from .filters.requests import ApiRequestFilter
from .filters.sql import SQLQueryFilter
from .filters.unittest import UnitTestFilter
from .git import COMMIT_SHA
from .serialize import (
    frame_path,
    get_callsite_data,
    monkeypatch_queryset_repr,
    serialize_locals,
    serialize_potential_json,
)
from .version import __version__


logger = logging.getLogger("kolo")


if TYPE_CHECKING:
    from .filters.core import AdvancedFrameFilter, FrameFilter
    from .serialize import UserCodeCallSite


class KoloProfiler:
    """
    Collect runtime information about code to view in VSCode.

    include_frames can be passed to enable profiling of standard library
    or third party code.

    ignore_frames can also be passed to disable profiling of a user's
    own code.

    The list should contain fragments of the path to the relevant files.
    For example, to include profiling for the json module the include_frames
    could look like ["/json/"].

    The list may also contain frame filters. A frame filter is a function
    (or other callable) that takes the same arguments as the profilefunc
    passed to sys.setprofile and returns a boolean representing whether
    to allow or block the frame.

    include_frames takes precedence over ignore_frames. A frame that
    matches an entry in each list will be profiled.
    """

    def __init__(self, db_path: Path, config=None) -> None:
        self.db_path = db_path
        trace_id = ulid.new()
        self.trace_id = f"trc_{trace_id}"
        self.frames_of_interest: List[Dict[str, Any]] = []
        self.request: Optional[Dict[str, Any]] = None
        self.response: Optional[Dict[str, Any]] = None
        self.config = config if config is not None else {}
        filter_config = self.config.get("filters", {})
        include_frames = filter_config.get("include_frames", ())
        ignore_frames = filter_config.get("ignore_frames", ())
        self.include_frames = list(map(build_frame_filter, include_frames))
        self.ignore_frames = list(map(build_frame_filter, ignore_frames))
        self.default_include_frames: List[AdvancedFrameFilter] = [
            DjangoFilter(self.config),
            CeleryFilter(self.config),
            HueyFilter(self.config),
            ApiRequestFilter(self.config),
            ExceptionFilter(self.config),
            LoggingFilter(self.config),
            SQLQueryFilter(self.config),
            UnitTestFilter(self.config),
        ]

        self.co_names = set()
        for filter in self.default_include_frames:
            self.co_names.update(filter.co_names)

        self.default_ignore_frames: List[FrameFilter] = [
            library_filter,
            frozen_filter,
            import_filter,
            exec_filter,
            attrs_filter,
            kolo_filter,
        ]
        self.call_frame_ids: List[Dict[str, str]] = []
        self.timestamp = time.time()

    def __call__(self, frame: types.FrameType, event: str, arg: object) -> None:
        if event in ["c_call", "c_return"]:
            return

        for frame_filter in self.include_frames:
            try:
                if frame_filter(frame, event, arg):
                    self.process_frame(frame, event, arg)
                    return
            except Exception as e:
                logger.debug(
                    "Unexpected exception in include_frames: %s",
                    frame_filter,
                    exc_info=e,
                )
                continue

        for frame_filter in self.ignore_frames:
            try:
                if frame_filter(frame, event, arg):
                    return
            except Exception as e:
                logger.debug(
                    "Unexpected exception in ignore_frames: %s",
                    frame_filter,
                    exc_info=e,
                )
                continue

        co_name = frame.f_code.co_name
        if co_name in self.co_names:
            for frame_filter in self.default_include_frames:
                try:
                    if frame_filter(frame, event, arg):
                        if frame_filter.use_frames_of_interest:
                            self.process_frame(frame, event, arg)
                        with monkeypatch_queryset_repr():
                            frame_data = frame_filter.process(
                                frame, event, arg, self.call_frame_ids
                            )
                        if frame_data:
                            self.frames_of_interest.append(frame_data)
                        return
                except Exception as e:
                    logger.debug(
                        "Unexpected exception in default_include_frames: %s",
                        frame_filter,
                        exc_info=e,
                    )
                    continue

        for frame_filter in self.default_ignore_frames:
            try:
                if frame_filter(frame, event, arg):
                    return
            except Exception as e:
                logger.debug(
                    "Unexpected exception in default_ignore_frames: %s",
                    frame_filter,
                    exc_info=e,
                )
                continue

        try:
            self.process_frame(frame, event, arg)
        except Exception as e:
            logger.debug(
                "Unexpected exception in KoloProfiler.process_frame",
                exc_info=e,
            )

    def __enter__(self):
        sys.setprofile(self)

    def __exit__(self, *exc):
        sys.setprofile(None)

    def save_request_in_db(self) -> None:
        wal_mode = self.config.get("wal_mode", True)
        timestamp = self.timestamp
        json_data = {
            "command_line_args": sys.argv,
            "current_commit_sha": COMMIT_SHA,
            "frames_of_interest": self.frames_of_interest,
            "meta": {"version": __version__, "use_frame_boundaries": True},
            "timestamp": timestamp,
            "trace_id": self.trace_id,
        }
        save_invocation_in_sqlite(
            self.db_path, self.trace_id, json.dumps(json_data), wal_mode
        )

    def process_frame(self, frame: types.FrameType, event: str, arg: object) -> None:
        user_code_call_site: Optional[UserCodeCallSite]
        if event == "call" and self.call_frame_ids:
            user_code_call_site = get_callsite_data(frame, self.call_frame_ids[-1])
        else:
            # If we are a return frame, we don't bother duplicating
            # information for the call frame.
            # If we are the first call frame, we don't have a callsite.
            user_code_call_site = None

        frame_id = f"frm_{ulid.new()}"
        co_name = frame.f_code.co_name
        if event == "call":
            call_frame_data = {
                "frame_id": frame_id,
                "filepath": frame.f_code.co_filename,
                "co_name": co_name,
            }
            self.call_frame_ids.append(call_frame_data)
        elif event == "return":  # pragma: no branch
            self.call_frame_ids.pop()

        with monkeypatch_queryset_repr():
            frame_data = {
                "path": frame_path(frame),
                "co_name": co_name,
                "qualname": get_qualname(frame),
                "event": event,
                "frame_id": frame_id,
                "arg": serialize_potential_json(arg),
                "locals": serialize_locals(frame.f_locals),
                "timestamp": time.time(),
                "type": "frame",
                "user_code_call_site": user_code_call_site,
            }
            self.frames_of_interest.append(frame_data)


def get_qualname(frame: types.FrameType) -> Optional[str]:
    try:
        qualname = frame.f_code.co_qualname  # type: ignore
    except AttributeError:
        pass
    else:
        module = frame.f_globals["__name__"]
        return f"{module}.{qualname}"

    co_name = frame.f_code.co_name
    if co_name == "<module>":  # pragma: no cover
        module = frame.f_globals["__name__"]
        return f"{module}.<module>"

    try:
        outer_frame = frame.f_back
        assert outer_frame
        try:
            function = outer_frame.f_locals[co_name]
        except KeyError:
            try:
                self = frame.f_locals["self"]
            except KeyError:
                cls = frame.f_locals.get("cls")
                if isinstance(cls, type):
                    function = inspect.getattr_static(cls, co_name)
                else:
                    try:
                        qualname = frame.f_locals["__qualname__"]
                    except KeyError:
                        function = frame.f_globals[co_name]
                    else:  # pragma: no cover
                        module = frame.f_globals["__name__"]
                        return f"{module}.{qualname}"
            else:
                function = inspect.getattr_static(self, co_name)
                if isinstance(function, property):
                    function = function.fget

        return f"{function.__module__}.{function.__qualname__}"
    except Exception:
        return None


@contextmanager
def enabled(config=None):
    if sys.getprofile():
        yield
        return
    db_path, config = load_config(config)
    profiler = KoloProfiler(db_path, config=config)
    with profiler:
        yield
    profiler.save_request_in_db()


F = TypeVar("F", bound=Callable[..., Any])


def enable(func: F, config=None) -> F:
    @wraps(func)
    def decorated(*args, **kwargs):
        with enabled(config):
            return func(*args, **kwargs)

    return cast(F, decorated)
