import datetime
import json
import orjson
import logging
import traceback

from py_fastapi_logging.formatters.base import BaseFormatter
from py_fastapi_logging.schemas.base import BaseJsonLogSchema
from py_fastapi_logging.utils.extra import get_env_extra


class JSONLogFormatter(BaseFormatter):
    def __init__(self, fmt=None, datefmt=None, style='%', validate=True, multi_line=None):
        self.multi_line = multi_line
        super().__init__(fmt=fmt, datefmt=datefmt, style=style, validate=validate)
        self._skip_extra = {"name", "msg", "args", "levelname", "levelno", "pathname", "filename", "module",
                            "exc_info", "exc_text", "stack_info",
                            "lineno", "funcName", "created", "msecs", "relativeCreated",
                            "thread", "threadName", "processName", "process", "request_id", "progname"}

    def get_extra(self, record):
        extra = {name: value for name, value in record.__dict__.items() if name not in self._skip_extra}
        return extra

    @staticmethod
    def _default_to_str(value):
        return str(value)

    def _format_log(self, record: logging.LogRecord) -> dict:
        payload = {
            "message": record.getMessage()
        }
        now = datetime.datetime.fromtimestamp(record.created).astimezone().replace(microsecond=0).isoformat()

        json_log_fields = BaseJsonLogSchema(
            thread=record.process,
            timestamp=now,
            level=record.levelname,
        )

        for key in get_env_extra().keys():
            if hasattr(record, key):
                json_log_fields[key] = getattr(record, key)
            elif key == "progname":
                json_log_fields[key] = record.module

        aux = {
            'module': record.module,
            "lineno": record.lineno,
            "func_name": record.funcName,
            "process": record.process,
            "thread_name": record.threadName,
            "logger_name": record.name
        }
        payload["aux"] = aux

        if record.exc_info is not None:
            payload["backtrace"] = self.formatException(record.exc_info)

        payload['args'] = record.args
        payload["extra"] = self.get_extra(record)

        if record.exc_info:
            json_log_fields["exceptions"] = traceback.format_exception(*record.exc_info)

        elif record.exc_text:
            json_log_fields["exceptions"] = record.exc_text
        json_log_fields["payload"] = payload
        # if hasattr(record, "payload"):
        #     json_log_fields["payload"] = record.payload
        # elif hasattr(record, "message"):
        #     msg = record.message % record.args
        #     json_log_fields["payload"] = {"message": msg}
        # elif hasattr(record, "msg"):
        #     msg = record.msg % record.args
        #     json_log_fields["payload"] = {"message": msg}
        # try:
        #     return json.dumps(json_log_fields, ensure_ascii=False)
        # except Exception as e:
        #     m = {str(k): str(v) for k, v in json_log_fields.items()}
        #     m["failed_dump"] = str(e)
        #     return json.dumps(json_log_fields, ensure_ascii=False)

        option = orjson.OPT_UTC_Z
        if self.multi_line:
            option |= orjson.OPT_INDENT_2

        try:
            packed = orjson.dumps(json_log_fields, default=self._default_to_str, option=option)
        except Exception as e:
            m = {str(k): str(v) for k, v in json_log_fields.items()}
            m["failed_dump"] = str(e)
            packed = orjson.dumps(m, default=self._default_to_str, option=option)
        return packed.decode("utf-8")

