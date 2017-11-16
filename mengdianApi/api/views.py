# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from collections import OrderedDict

from django.http import HttpResponse

from mengdianApi.api.ServerUtils import ServerUtils
from mengdianApi.api.get_cookie import Get_token


def index(request):
    return HttpResponse("Hello Django!")


def server_utils(request):
    """
    服务器操作
    :param request:
    :return:
    """
    global message
    body = json.loads(request.body)
    host = body.get("host", "")
    t = body.get("t", "")
    if host is "":
        return HttpResponse(json.dumps({"code": 999999, "message": "host必填参数不能空！"}))
    if t == "tm":
        tomcat_num = body.get("tomcat_num", "")
        tomcat1 = body.get("tomcat1", "")
        tomcat2 = body.get("tomcat2", "")
        tomcat3 = body.get("tomcat3", "")
        su = ServerUtils(host=host, tomcat_num=tomcat_num, tomcat1=tomcat1, tomcat2=tomcat2, tomcat3=tomcat3)
        message = su.install_tomcat()
        print message
        return HttpResponse(json.dumps({"code": 0, "message": message}))
    elif t == "jdk" or t == "wcc":
        jdk_version = body.get("jdk_version", "")
        su = ServerUtils(host=host, t=t, jdk_version=jdk_version)
        message = su.install_jdk()
        print message
        return HttpResponse(json.dumps({"code": 0, "message": message}))
    elif t == "r":
        host = body.get("host", "")
        path = body.get("path", "")
        utils = body.get("utils", "")
        su = ServerUtils(host=host, path=path, utils=utils)
        message = su.server_manage()
        print message
        return HttpResponse(json.dumps({"code": 0, "message": message}))


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
        username = body.get("username", None)
        identityCode = body.get("identityCode", None)
        password = body.get("password", None)
        loginType = body.get("loginType", None)
        if username is not None and identityCode is not None and password is not None and loginType is not None:
            cookie = token.get_crm_token(username, identityCode, password, loginType)
            r = OrderedDict()
            data = OrderedDict()
            data["cookie"] = cookie
            r["code"] = 0
            r["msg"] = "success"
            r["type"] = "crm"
            r["data"] = data
            return HttpResponse(json.dumps(r))
        else:
            return HttpResponse({"code": 999999, "message": "crm登陆必填参数不得为空，username，identityCode，password，loginType"})
    elif type == "h5":
        cookie = token.get_h5_token()
        if cookie.get("cm.sid") != "null":
            r = OrderedDict()
            data = OrderedDict()
            data["cookie"] = cookie["cm.sid"]
            r["code"] = 0
            r["msg"] = "success"
            r["type"] = "h5"
            r["data"] = data
            return HttpResponse(json.dumps(r))
        else:
            return HttpResponse({"code": 999999, "message": "h5登录失败，请自行查看接口"})
    else:
        return HttpResponse(json.dumps({"code": 999999, "message": "type类型不能为空!"}))
