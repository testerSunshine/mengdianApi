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
        try:
            console = subprocess.check_output("sh /data/deploy/install_tomcat.sh {0} {1} {2} {3} {4}".format(self.utils["host"],
                                                                                                self.utils["tomcat_num"],
                                                                                                self.utils["tomcat1"],
                                                                                                self.utils["tomcat2"],
                                                                                                self.utils["tomcat3"],
                                                                                                ), shell=True)
            return console
        except subprocess.CalledProcessError as err:
            return "命令错误: {0}".format(err)



# s = ServerUtils(host=1)
# s.install_tomcat()