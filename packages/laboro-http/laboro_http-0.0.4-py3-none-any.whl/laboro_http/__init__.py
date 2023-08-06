import os
import requests
from laboro.error import LaboroError
from laboro.module import Module


class Http(Module):
  """This class is derived from the ``laboro.module.Module`` base class.

  Its purpose is to provide a general purpose simplified HTTP client able to make all type of request over HTTP such as REST API call.

  Arguments:

    args: None. This module does not have initialization arguments.
  """

  def __init__(self, context, args=None):
    super().__init__(filepath=__file__, context=context, args=args)
    self.session = requests.Session()

  def __enter__(self):
    super().__enter__()
    return self

  @Module.laboro_method
  def request(self, url, method="GET", params=None, data=None, headers=None,
              cookies=None, files=None, auth=None, timeout=None,
              proxy=None, json=None, verify=True, exit_on_error=True):
    """
    Send any type of HTTP request and return the response sent back by server.
    Most arguments of this method are optional.
    When not specified otherwise, any optional argument defaults to *None*.

    Arguments:
      ``method``: String. Optional. The HTTP method to be used. This should be one of the `HTTP verbs`. See https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods for further details. Default to ``GET``.

      Actually only the following verbs are implemented:
      - GET, POST, PUT, DELETE, PATCH, HEAD.

      ``url``: String. Mandatory. The full URL to request including the `scheme` (i.e: http, https). The URL **must NOT** include any `GET` parameters.
      ``params``: Dictionary, list or tuple. Optional. Any suitable representation of the `GET` parameters to send in the request.
      ``data``: Dictionary. Optional. A dictionary representation of the body data of the request. This parameters is mainly used to send form data in a dictionary.
      ``json``: JSON. Optional. Any representation of valid JSON data (list or dictionary) to send in the body of the request.
      ``headers``: Dictionary. Optional. A dictionary representation of HTTP headers to send with the request.
      ``cookies``: Dictionary. Optional. A dictionary of cookies to send with request.
      ``files``: List. Optional. A list of filenames (full path) to send.
      ``auth``: Dictionary. Optional. A dictionary of two items: `username` and `password` to be used as Basic/Digest/Custom HTTP Authentication.
      ``timeout``: Integer. Optional. Request timeout in seconds.
      ``proxy``: String. A proxy URL with scheme, domain or IP address and port (i.e: https://proxy.my_company.com:3128).
      ``verify``: If set to false, the server SSL cert will not be verified. Default to ``True``.
      ``exit_on_error``: If set to ``False``, only log a warning whenever a error is encountered. Default to True, which will raise an error and immediately exit the workflow.

      Note:
      - When ``json`` is defined, the ``Content-Type`` header is automatically set to ``application/json; charset=UTF-8``.
      - When ``data`` or ``files`` is defined, the ``Content-Type`` header is automatically set to ``multipart/form-data``.
      - ``json`` can not be used alongside ``data`` or ``files``.
      - When ``exit_on_error`` is set to ``True`` (default), no response is returned whatever the error is a HTTP error or a system/network error.
      - When ``exit_on_error`` is set to ``False``, a response is returned if the encountered error is an HTTPError. Any other error will return ``None``.
      - In any case, the encountered error will be logged.

    Returns:
      A dictionary representation of the response returned by the requested server.

      The response dictionary will have all the following attributes:
      - ``cookies``: A dictionary of cookies sent by the requested server. Default to empty dictionary.
      - ``headers``: A dictionary representation of all response headers. Default to empty dictionary.
      - ``json``: Any valid representation of a JSON object. Mostly List or Dict. Default to empty dictionary if no JSON was sent back.
      - ``text``: Textual content of the response. Default to None.
      - ``status``: A dictionary with the following format: {"code": <status code>, "reason": <reason>}. ``code`` is one of the HTTP response status code while ``reason`` is the corresponding textual message of the status code. i.e: ``{"code": 404, "reason": "Not found"}``.
    """
    self.context.log.info(f"Sending request to: {method} {url}")
    req_args = {"params": params,
                "data": data,
                "headers": headers,
                "cookies": cookies,
                "files": files,
                "auth": auth,
                "timeout": timeout,
                "proxy": proxy,
                "json": json,
                "verify": verify}
    request_args = self._process_args(method, req_args)
    methods = {"GET": {"method": self._get,
                       "kwargs": request_args},
               "POST": {"method": self._post,
                        "kwargs": request_args},
               "PUT": {"method": self._put,
                       "kwargs": request_args},
               "DELETE": {"method": self._delete,
                          "kwargs": request_args},
               "PATCH": {"method": self._patch,
                         "kwargs": request_args}}
    try:
      resp = methods[method]["method"](url, **methods[method]["kwargs"])
      content_type = resp.headers.get('Content-Type')
      resp_json = resp.json() if "application/json" in content_type else None
      response = {"cookies": {cookie[0]: cookie[1]
                              for cookie in resp.cookies.items()},
                  "headers": resp.headers,
                  "json": resp_json,
                  "text": resp.text,
                  "status": {"code": resp.status_code,
                             "reason": resp.reason}}
      resp.raise_for_status()
      return response
    except requests.HTTPError as err:
      err_msg = f"[HttpRequestError] {resp.status_code}: {resp.reason}"
      if exit_on_error:
        raise LaboroError(err_msg) from err
      return response
    except Exception as err:
      err_msg = f"[HttpRequestError] {err.__class__.__name__}: {err}"
      if exit_on_error:
        raise LaboroError(err_msg) from err
      else:
        self.context.log.warning(err_msg)
        return None

  def _process_args(self, method, req_args):
    """Manage all request params to satisfy the format expected by python requests module.
    """
    get_args = {"params": None, "timeout": None,
                "headers": None, "cookies": None,
                "proxies": None, "auth": None, "verify": None}
    post_args = {"data": None, "json": None, "files": None}
    for arg, value in req_args.items():
      if arg in get_args and value is not None:
        get_args[arg] = self._process_arg(arg, value)
      if arg in post_args and value is not None:
        post_args[arg] = self._process_arg(arg, value)
      elif arg == "proxy" and value is not None:
        get_args["proxies"] = self._process_arg(arg, value)
    if method == "GET":
      return get_args
    return self._set_content_type({**get_args, **post_args})

  def _process_arg(self, arg, value):
    """Manage specific argument.
    """
    if arg == "auth":
      return (value.get("username"), value.get("password"))
    if arg == "files":
      files = {}
      for filename in value:
        fname = os.path.basename(filename)
        files[fname] = open(filename, mode="rb")
      return files
    elif arg == "proxy":
      return {"http": value,
              "https": value}
    else:
      return value

  def _set_content_type(self, args):
    """Set Content-Type header according to args.
    """
    headers = args.get("headers") or dict()
    if args.get("json") is not None:
      headers["Content-Type"] = "application/json; charset=UTF-8"
    if args.get("data") is not None or args.get("files") is not None:
      headers["Content-Type"] = "multipart/form-data"
    args["headers"] = headers
    return args

  def _get(self, url, **kwargs):
    return self.session.get(url, **kwargs)

  def _post(self, url, **kwargs):
    return self.session.post(url, **kwargs)

  def _head(self, url, **kwargs):
    return self.session.head(url, **kwargs)

  def _put(self, url, **kwargs):
    return self.session.put(url, **kwargs)

  def _delete(self, url, **kwargs):
    return self.session.delete(url, **kwargs)

  def _patch(self, url, **kwargs):
    return self.session.patch(url, **kwargs)
