# -*- coding: utf-8 -*-

import sys, os
from datetime import datetime, timezone

parent_folder_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(parent_folder_path)
sys.path.append(os.path.join(parent_folder_path, "lib"))
sys.path.append(os.path.join(parent_folder_path, "plugin"))

import pyperclip
from flowlauncher import FlowLauncher
from comm import makeRPC


class TimeStamp(FlowLauncher):
    def query(self, query):
        dt = datetime.now()
        if len(query) != 0:
            try:
                dt = datetime.strptime(query, "%Y-%m-%d %H:%M:%S")
            except:
                try:
                    dt = datetime.strptime(query, "%Y/%m/%d %H:%M:%S")
                except:
                    try:
                        dt = datetime.fromtimestamp(float(query))
                    except:
                        dt = None

        if dt != None and dt.year <= 1970:
            dt = None

        if not isinstance(dt, datetime):
            return [makeRPC("输入信息错误")]

        t = int(dt.timestamp())
        st = dt.strftime("%Y-%m-%d %H:%M:%S")
        st2 = dt.strftime("%Y/%m/%d %H:%M:%S")

        return [
            makeRPC(
                title="{:<16}{}".format("时间戳:", t), method="copy2clipboard", args=[t]
            ),
            makeRPC(
                title="{:<13}{}".format("日期时间:", st),
                method="copy2clipboard",
                args=[st],
            ),
            makeRPC(
                title="{:<13}{}".format("日期时间:", st2),
                method="copy2clipboard",
                args=[st2],
            ),
        ]

    def context_menu(self, data):
        return []

    def copy2clipboard(self, t):
        pyperclip.copy(str(t).strip())


if __name__ == "__main__":
    TimeStamp()
