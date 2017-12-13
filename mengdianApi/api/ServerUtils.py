# -*- coding: utf8 -*-
__author__ = 'MR.wen'

import json
import subprocess
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
#
# a = subprocess.check_call("ls -a", shell=True)
#
# child = subprocess.Popen("cat views.py", shell=True, stdin=subprocess.PIPE)
# print child.communicate("views.py")

# a = {"b": 1, "c": "2"}
# print a.get("d", "")


class ServerUtils:
    def __init__(self, **kwargs):
        self.utils = kwargs

    def install_tomcat(self):
        """
        安装Tomcat
        :return:
        """
        print "sh /data/deploy/install_tomcat{0}.sh {1} {2} {3} {4} {5}".format(self.utils["tomcat_version"],
                                                                                self.utils["host"],
                                                                                self.utils["tomcat_num"],
                                                                                self.utils["tomcat1"],
                                                                                self.utils["tomcat2"],
                                                                                self.utils["tomcat3"],)
        try:
            console = subprocess.check_output("sh /data/deploy/install_tomcat{0}.sh {1} {2} {3} {4} {5}"
                                                                .format(self.utils["tomcat_version"],
                                                                        self.utils["host"],
                                                                        self.utils["tomcat_num"],
                                                                        self.utils["tomcat1"],
                                                                        self.utils["tomcat2"],
                                                                        self.utils["tomcat3"],
                                                                        ), shell=True)
            return console
        except subprocess.CalledProcessError as err:
            return "命令错误: {0}".format(err)

    def install_jdk(self):
        """
        安装jdk&wcc
        :return:
        """
        print "安装项目： {0}".format(self.utils["t"],)
        try:
            console = subprocess.check_output("sh /data/deploy/install_{0}.sh {1} {2}".format(self.utils["t"],
                                                                                         self.utils["host"],
                                                                                         self.utils["jdk_version"],
                                                                                         ), shell=True)
            return console
        except subprocess.CalledProcessError as err:
            return "命令错误: {0}".format(err)

    def server_manage(self):
        print "{0} server".format(self.utils["utils"])
        try:
            console = subprocess.check_output("sh /data/deploy/restart_tomcat.sh {0} {1} {2}".format(self.utils["host"],
                                                                                                self.utils["path"],
                                                                                                self.utils["utils"],
                                                                                                ), shell=True)
            return console
        except subprocess.CalledProcessError as err:
            return "命令错误: {0}".format(err)


# s = ServerUtils(host=1)
# s.install_tomcat()