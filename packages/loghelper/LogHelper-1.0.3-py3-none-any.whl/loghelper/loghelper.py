#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = "ITXiaoPang"
__mtime__ = "2021/07/10"
__project__ = "LogHelper"
__file__ = "loghelper.py"
__IDE__ = "PyCharm"

import logging
import os
import traceback

from logging.handlers import TimedRotatingFileHandler, WatchedFileHandler
try:
    from concurrent_log import ConcurrentTimedRotatingFileHandler
except ImportError:
    ConcurrentTimedRotatingFileHandler = TimedRotatingFileHandler

try:
    from flask import has_request_context, request
except ImportError:
    def has_request_context():
        return False


    class _MockFlaskRequest:
        url = 'mock_url'
        remote_addr = 'mock_remote_addr'


    request = _MockFlaskRequest()

try:
    from pythonjsonlogger.jsonlogger import JsonFormatter

    use_json_format = True
except ImportError:
    class JsonFormatter:
        def __init__(self, *args, **kwargs):
            pass


    use_json_format = False


class WatchedTimedRotatingFileHandler(TimedRotatingFileHandler, WatchedFileHandler):
    def __init__(self, filename, *args, **kwargs):
        TimedRotatingFileHandler.__init__(self, filename, *args, **kwargs)

        self.dev, self.ino = -1, -1
        self._statstream()

    def emit(self, record):
        try:
            if self.shouldRollover(record):
                self.doRollover()
            # notice that reopenIfNeeded calls os.stat
            # it may cause efficiency issues
            self.reopenIfNeeded()
            logging.FileHandler.emit(self, record)
        except Exception:
            self.handleError(record)


class LogHelper:
    def __init__(
            self, log_dir: str, log_path: str = '/var/log/',
            backup_count: int = 7, when: str = 'midnight',
            timed_rotating_file_handler=TimedRotatingFileHandler
    ):
        self.logging_directory = os.path.join(log_path, log_dir)
        self.backup_count = backup_count
        self.when = when
        self.timed_rotating_file_handler = timed_rotating_file_handler

        if os.path.exists(self.logging_directory):
            if not os.path.isdir(self.logging_directory):
                raise ValueError(f'{self.logging_directory}不是目录')
        else:
            try:
                os.makedirs(self.logging_directory, mode=0o755)
            except Exception as ex:
                raise OSError(f'自动创建日志目录失败:{ex}')

    class RequestFormatter(logging.Formatter):
        def format(self, record):
            if has_request_context():
                record.url = request.url
                record.remote_addr = request.remote_addr
            else:
                record.url = '-'
                record.remote_addr = '127.0.0.1'

            return super().format(record)

    logging_format = RequestFormatter(
        '<%(asctime)s> %(levelname)s '
        '(%(filename)s %(funcName)s %(lineno)d) '
        '{%(process)d %(thread)d %(threadName)s} '
        '[%(url)s %(remote_addr)s] '
        '%(message)s'
    )

    @staticmethod
    def _create_stream_handler(name, formatter):
        log_stream_handler = logging.StreamHandler()
        log_stream_handler.name = name
        log_stream_handler.setFormatter(formatter)
        return log_stream_handler

    def _create_timed_rotating_file_handler(self, name, filename, formatter):
        timed_rotating_file_handler = self.timed_rotating_file_handler(
            filename=os.path.join(self.logging_directory, f'{filename}.Runtime.log'),
            when=self.when, backupCount=self.backup_count,
            encoding='UTF-8'
        )
        timed_rotating_file_handler.name = name
        timed_rotating_file_handler.setFormatter(formatter)
        return timed_rotating_file_handler

    def create_logger(
            self, name=__name__, filename: str = __name__,
            add_stream_handler: bool = False,
            json_ensure_ascii: bool = False,
            reserved_attrs: list = None,
    ):
        _logger = logging.getLogger(name)
        _logger.setLevel(logging.INFO)
        # stream_handler
        if add_stream_handler:
            stream_handler = self._create_stream_handler(name=f'stream_{name}', formatter=self.logging_format)
            if stream_handler.name not in [_.name for _ in _logger.handlers]:
                _logger.addHandler(stream_handler)

        # raw_timed_rotating_file_handler
        raw_timed_rotating_file_handler = self._create_timed_rotating_file_handler(
            name=f'raw_{name}',
            filename=f'raw_{filename}',
            formatter=self.logging_format
        )
        if raw_timed_rotating_file_handler.name not in [_.name for _ in _logger.handlers]:
            _logger.addHandler(raw_timed_rotating_file_handler)

        # json_timed_rotating_file_handler
        if use_json_format:
            if not reserved_attrs:
                reserved_attrs = [
                    'msg',
                    'args',
                    'levelno',
                    'relativeCreated',
                ]
            logging_format_json = JsonFormatter(
                timestamp=True,
                json_indent=None,
                json_ensure_ascii=json_ensure_ascii,
                reserved_attrs=reserved_attrs
            )
            json_timed_rotating_file_handler = self._create_timed_rotating_file_handler(
                name=f'json_{name}',
                filename=f'json_{filename}',
                formatter=logging_format_json
            )
            if json_timed_rotating_file_handler.name not in [_.name for _ in _logger.handlers]:
                _logger.addHandler(json_timed_rotating_file_handler)

        return _logger

    @staticmethod
    def get_caller_frame(level: int = 3):
        ret_caller = None
        extract_stack = traceback.extract_stack()
        if len(extract_stack) > level:
            caller = extract_stack[-level]
            if isinstance(caller, traceback.FrameSummary):
                ret_caller = caller
        return ret_caller
