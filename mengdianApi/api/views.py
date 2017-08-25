# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from collections import OrderedDict

from django.http import HttpResponse
from mengdianApi.api.get_cookie import Get_token


def index(request):
    return HttpResponse("Hello Django!")


def get_session(request):
    token = Get_token()
    print(token)
    if token is not None:
        body = json.loads(request.body)
        type = body["type"]
    else:
        return HttpResponse(json.dumps({"code": 999999, "message": "无效的格式!"}))
    if type == "ghs":
        try:
            account = body["account"]
            pwd = body["pwd"]
            cookie = token.get_ghs_token(account, pwd)
            r = OrderedDict()
            data = OrderedDict()
            data["cookie"] = cookie
            r["code"] = 0
            r["msg"] = "success"
            r["type"] = "ghs"
            r["data"] = data
            return HttpResponse(json.dumps(r))
        except KeyError:
            return HttpResponse(json.dumps({"code": 999998, "message": "账户名或密码不能为空"}))
    elif type == "yy":
        cookie = token.get_yy_token()
        r = OrderedDict()
        data = OrderedDict()
        data["cookie"] = cookie
        r["code"] = 0
        r["msg"] = "success"
        r["type"] = "yy"
        r["data"] = data
        return HttpResponse(json.dumps(r))
    elif type == "crm":
        username = body["username"]
        identityCode = body["identityCode"]
        password = body["password"]
        cookie = token.get_crm_token(username, identityCode, password)
        r = OrderedDict()
        data = OrderedDict()
        data["cookie"] = cookie
        r["code"] = 0
        r["msg"] = "success"
        r["type"] = "crm"
        r["data"] = data
        return HttpResponse(json.dumps(r))
    else:
        return HttpResponse(json.dumps({"code": 999999, "message": "type类型不能为空!"}))

