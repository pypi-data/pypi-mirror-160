# -*- coding: utf-8 -*-

"""
requests.exceptions
~~~~~~~~~~~~~~~~~~~

This module contains the set of Requests' exceptions.
"""
from .libs.urllib3.exceptions import HTTPError as BaseHTTPError

from .compat import JSONDecodeError as CompatJSONDecodeError


class RequestException(IOError):
    """There was an ambiguous exception that occurred while handling your
    request.
    """

    def __init__(self, *args, **kwargs):
        """Initialize RequestException with `request` and `response` objects."""
        response = kwargs.pop('response', None)
        self.response = response
        self.request = kwargs.pop('request', None)
        if (response is not None and not self.request and
                hasattr(response, 'request')):
            self.request = self.response.request
        super(RequestException, self).__init__(*args, **kwargs)


class InvalidJSONError(RequestException):
    """A JSON error occurred."""


class JSONDecodeError(InvalidJSONError, CompatJSONDecodeError):
    """Couldn't decode the text into json"""


class HTTPError(RequestException):
    """An HTTP error occurred."""


class ConnectionError(RequestException):
    """A Connection error occurred."""


class ProxyError(ConnectionError):
    """A proxy error occurred."""


class SSLError(ConnectionError):
    """An SSL error occurred."""


class Timeout(RequestException):
    """The request timed out.

    Catching this error will catch both
    :exc:`~requests.exceptions.ConnectTimeout` and
    :exc:`~requests.exceptions.ReadTimeout` errors.
    """


class ConnectTimeout(ConnectionError, Timeout):
    """The request timed out while trying to connect to the remote server.

    Requests that produced this error are safe to retry.
    """


class ReadTimeout(Timeout):
    """
    服务器在分配的时间内没有发送任何数据。
    """


class URLRequired(RequestException):
    """
    发出请求需要一个有效的URL。
    """


class TooManyRedirects(RequestException):
    """
    太多的重定向。
    """


class MissingSchema(RequestException, ValueError):
    """
    太多的重定向。URL方案(例如http或https)缺失。
    """


class InvalidSchema(RequestException, ValueError):
    """The URL scheme provided is either invalid or unsupported."""


class InvalidURL(RequestException, ValueError):
    """
    提供的URL不知何故无效。
    """


class InvalidHeader(RequestException, ValueError):
    """
    提供的URL不知何故无效。提供的报头值在某种程度上是无效的。
    """


class InvalidProxyURL(InvalidURL):
    """
    提供的代理URL无效。
    """


class ChunkedEncodingError(RequestException):
    """
    服务器声明了块编码，但发送了一个无效的块。
    """


class ContentDecodingError(RequestException, BaseHTTPError):
    """Failed to decode response content."""


class StreamConsumedError(RequestException, TypeError):
    """
    此响应的内容已经被使用。
    """


class RetryError(RequestException):
    """
    自定义重试逻辑失败
    """


class UnrewindableBodyError(RequestException):
    """
    自定义重试逻辑失败请求在尝试倒带正文时遇到错误。
    """


class RequestsWarning(Warning):
    """
    请求的基本警告。
    """


class FileModeWarning(RequestsWarning, DeprecationWarning):
    """
    请求的基本警告。文件以文本模式打开，但请求确定其二进制长度。
    """


class RequestsDependencyWarning(RequestsWarning):
    """
    导入的依赖项与预期的版本范围不匹配。
    """
