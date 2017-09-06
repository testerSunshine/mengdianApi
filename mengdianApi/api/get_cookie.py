# -*- coding: utf8 -*-
import json

__author__ = 'MR.wen'

import cookielib
import sys
import urllib
import urllib2
import requests
from bs4 import BeautifulSoup
from requests import RequestException
reload(sys)
sys.setdefaultencoding('utf-8')


class Get_token():
    def get_ghs_token(self, account, pwd):
        data = self._set_ghs_token(account, pwd)
        return data

    def get_yy_token(self):
        data = self._set_yy_token()
        return data

    def get_crm_token(self, username, identityCode, password, loginType):
        data = self._set_crm_token(username, identityCode, password, loginType)
        return data

    def get_h5_token(self):
        data = self._set_h5_token()
        return data

    def _set_ghs_token(self, account, pwd):
        """
        将供货商后台必须的weimob id 赋值给__cookies_ghs
        """
        login_info = {'account': account, 'password': pwd}
        ghsLogin = "http://md.passport.weimobqa.com"  # 供货商和运营的登陆id一样，此处不用配置
        ghs = "http://md.passport.weimobqa.com/passport/login?callback=http%3A%2F%2Fmd.zs.weimobqa.com%2F&type="
        return self.get_token(ghsLogin, ghs, login_info)

    def _set_yy_token(self):
        """
        获取运营后台必须的weimob id, 赋值给__cookies_yy
        """
        YyLogin = "http://md.passport.weimobqa.com"  # 供货商和运营的登陆id一样，此处不用配置
        yy = "http://md.passport.weimobqa.com/passport/login?callback=http%3A%2F%2Fmd.manager.weimobqa.com%2F&type="
        login_info = {'account': 'operation', 'password': "111111"}
        return self.get_token(YyLogin, yy, login_info)

    def _set_crm_token(self, username, identityCode, password, loginType):
        """获取crm登陆token"""
        url = "http://172.21.248.149:8080/api/login"
        login_info = {"username": username, "identityCode": identityCode, "password": password, "validateCode": "111", "loginType": loginType}
        return self.req_post(url, login_info)

    def _set_h5_token(self):
        """
        获取H5登陆 session，固定手机号码15618715582
        """
        verify_url = "http://m-qa.weimobqa.com/api/user/verify"   # 发送H5登陆验证码
        verify_data = {"mobile": 15618715582, "mode": "h5FastLogin"}
        self.req_post(verify_url, verify_data, is_need_con=True)

        verify_code_url = "http://md.delivery.weimobqa.com/tools/getCode.php?env=qa&mobile=15618715582_0086&version=v2_h5FastLogin&dataType=json"  # 获取验证码
        verify_code_data = {"env": "qa",
                            "mobile": "15618715582_0086",
                            "version": "v2_h5FastLogin",
                            "dataType": "json"}
        results = json.loads(self.req_post(verify_code_url, verify_code_data, is_need_con=True))
        verifycode = eval(results).get("code", None)   # 将返回值转成字典格式
        if verifycode is not None and verifycode is not "false":
            url = "http://m-qa.weimobqa.com/api/user/login"  # 登陆很h5获得cookie
            login_info = {"verifycode": verifycode, "mobile": 15618715582, "mode": "h5FastLogin"}
            code = self.req_post(url, login_info)
            return code
        else:
            return {'cm.sid': 'null'}

    def up_post(self, url, data=None):
        """
        urllib2请求
        :param url: 请求网址
        :param data: 请求body
        :return: header
        """
        req = urllib2.Request(url)
        s_data = urllib.urlencode(data)
        cookies = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies))
        opener.open(req, s_data)
        c = dict()
        for ck in cookies:
            c[ck.name] = ck.value
            if c[ck.name] is not None:
                break
        return c

    def req_get(self, url, cookies=None):
        """
        requests get请求
        :param url:
        :param cookies:
        :return:
        """
        if cookies == None:
            result = requests.get(url=url)
        else:
            result = requests.get(url=url, cookies=cookies)
        try:
            if result.status_code == 200:
                return result.content
            else:
                return result.status_code
        except urllib2.HTTPError, e:
            return e.reason

    def req_post(self, url, data, cookies=None, is_need_con=False):
        """
         requests post请求
         :param url:
         :param cookies:
         :return:
         """
        if data is None:
            raise Exception('date不可缺少...')
            print(result.content)
        else:
            result = requests.post(url=url, cookies=cookies, data=data)
            if result.status_code == 200:
                c = dict()
                for cookie in result.cookies:
                    c[cookie.name] = cookie.value
                if is_need_con:
                    return json.dumps(result.content)
                else:
                    return c
            else:
                return "登陆失败"

    def bs(self, html_data):
        """
        解析网页代码
        :param html_data:
        :return: soup
        """
        soup = BeautifulSoup(html_data, "html.parser")
        return soup

    def get_token(self, base_url, login_url, dic):
        """
        获取后台必须的weimob id
        :return:  weimob id
        """
        try:
            result = self.req_get(login_url)
            soup = self.bs(result)
            action = soup.form['action']  # 加密请求的action文件
            d = soup.find_all('input')[2]['value']  # 加密请求的d文件
            playLoad = {'d': d}
            playLoad.update(dic)
            cookie = self.up_post(base_url + action, playLoad)
            return cookie
        except urllib2.URLError, e:
            print e.reason
        except RequestException, e:
            print e.response


g = Get_token()
print(g.get_h5_token())