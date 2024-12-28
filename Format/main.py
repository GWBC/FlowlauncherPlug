# -*- coding: utf-8 -*-

import sys, json
from pathlib import Path
import urllib.parse

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


class DataFormat(FlowLauncher):
    def __init__(self):
        self.util = Util("DataFormat.png")
        self.err = [
            self.util.makeRPC("url:格式化URL"),
            self.util.makeRPC("json:格式化JSON"),
        ]
        super().__init__()

    def query(self, query):
        s = str(query)
        ss = s.split(":", 1)
        if len(ss) != 2 or len(ss[1]) == 0:
            return self.err

        if ss[0] == "json":
            try:
                data = json.loads(ss[1])
                fmtData = json.dumps(data, indent=4)
                self.copy2clipboard(fmtData)
                return [self.util.makeRPC(fmtData)]
            except Exception as e:
                return [self.util.makeRPC("美化失败：{}".format(str(e)))]
        if ss[0] == "url":
            try:
                fmtUrl = urllib.parse.unquote(ss[1])
                parsed_url = urllib.parse.urlparse(ss[1])
                result = (
                    f"host: {parsed_url.netloc}\n"
                    f"path: {parsed_url.path}\n"
                    f"--------------------------------------------------------\n"
                )
                query_params = urllib.parse.parse_qs(parsed_url.query)
                result += "\n".join(
                    [f"{key}: {value}" for key, value in query_params.items()]
                )

                return [
                    self.util.makeRPC(fmtUrl, method="copy2clipboard", args=[fmtUrl]),
                    self.util.makeRPC(result, method="copy2clipboard", args=[result]),
                ]
            except Exception as e:
                return [self.util.makeRPC("美化失败：{}".format(str(e)))]
        return []

    def context_menu(self, data):
        return []

    def copy2clipboard(self, v):
        pyperclip.copy(v)


if __name__ == "__main__":
    DataFormat()
