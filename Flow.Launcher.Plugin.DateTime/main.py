# -*- coding: utf-8 -*-

import sys
from datetime import datetime
from pathlib import Path

curPath = Path(__file__).parent

sys.path.append(str(curPath))
sys.path.append(str(curPath.joinpath("lib")))

import pyperclip
from flox import Flox


class DateTime(Flox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger_level("debug")
        self.icon = "Images/icon.png"

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
            self.add_item(title="输入信息错误")
            return

        t = int(dt.timestamp())
        st = dt.strftime("%Y-%m-%d %H:%M:%S")
        st2 = dt.strftime("%Y/%m/%d %H:%M:%S")

        self.add_item(
            title="{:<16}{}".format("时间戳:", t),
            method="copy2clipboard",
            parameters=[t],
        )
        self.add_item(
            title="{:<13}{}".format("日期时间:", st),
            method="copy2clipboard",
            parameters=[st],
        )
        self.add_item(
            title="{:<13}{}".format("日期时间:", st2),
            method="copy2clipboard",
            parameters=[st2],
        )

    def context_menu(self, data):
        return []

    def copy2clipboard(self, t):
        pyperclip.copy(str(t).strip())


if __name__ == "__main__":
    DateTime()
