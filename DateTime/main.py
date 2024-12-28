# -*- coding: utf-8 -*-

import sys
from datetime import datetime
from pathlib import Path

curPath = Path(__file__).parent
parentPath = curPath.parent
commPath = parentPath.joinpath("Asset")

sys.path.append(str(parentPath))
sys.path.append(str(commPath))
sys.path.append(str(commPath.joinpath("lib")))
sys.path.append(str(commPath.joinpath("plugin")))

import pyperclip
from flowlauncher import FlowLauncher

from Comm.util import Util


class DateTime(FlowLauncher):
    def __init__(self):
        self.util = Util("DateTime.png")
        super().__init__()

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
            return [self.util.makeRPC("输入信息错误")]

        t = int(dt.timestamp())
        st = dt.strftime("%Y-%m-%d %H:%M:%S")
        st2 = dt.strftime("%Y/%m/%d %H:%M:%S")

        return [
            self.util.makeRPC(
                title="{:<16}{}".format("时间戳:", t), method="copy2clipboard", args=[t]
            ),
            self.util.makeRPC(
                title="{:<13}{}".format("日期时间:", st),
                method="copy2clipboard",
                args=[st],
            ),
            self.util.makeRPC(
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
    DateTime()
