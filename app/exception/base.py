#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from app.config.error_code import UnknownError, MESSAGE


class ApiError(Exception):
    """
    标准API异常
    """
    default_message = "服务端异常"
    default_code = UnknownError
    default_http_code = MESSAGE[default_code]["http_code"]

    def __init__(self, message=None, code=None, http_code=None, *args, **kwargs):
        """
        标准API异常构造函数

        :param code: 异常编码
        :param message: 异常信息
        :param http_code: HTTP状态码
        :param args:
        :param kwargs:
        """

        super(ApiError, self).__init__(message, *args)

        self.code = code or self.default_code
        self.message = message or self.default_message
        self.http_code = http_code or MESSAGE.get(self.code, {}).get("http_code") or self.default_http_code
        self.args = args
        self.kwargs = kwargs

    def __str__(self):
        return f"""{self.__class__.__name__}(code={self.code}, message={self.message}, http_code={self.http_code})"""

    @property
    def data(self):
        result = {
            "code": self.code,
            "message": self.message,
            "http_code": self.http_code
        }
        result.update(self.kwargs)
        return result
