# -*- coding: utf-8 -*-

import sys, json
from pathlib import Path
import urllib

curPath = Path(__file__).parent

sys.path.append(str(curPath))
sys.path.append(str(curPath.joinpath("lib")))

import pyperclip
from flox import Flox


class DataFormat(Flox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger_level("debug")
        self.icon = "Images/icon.png"

    def __err(self):
        self.add_item(title="url:格式化URL")
        self.add_item(title="json:格式化JSON")

    def query(self, query):
        s = str(query)
        ss = s.split(":", 1)
        if len(ss) != 2 or len(ss[1]) == 0:
            self.__err()
            return

        if ss[0] == "json":
            try:
                data = json.loads(ss[1])
                fmtData = json.dumps(data, indent=4)
                self.add_item(
                    title=fmtData, method="copy2clipboard", parameters=[fmtData]
                )
                return
            except Exception as e:
                self.add_item(title="美化失败：{}".format(str(e)))
                return
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

                self.add_item(
                    title=fmtUrl, method="copy2clipboard", parameters=[fmtUrl]
                )
                self.add_item(
                    title=result, method="copy2clipboard", parameters=[result]
                )
                return
            except Exception as e:
                self.add_item(title="美化失败：{}".format(str(e)))
                return
        return []

    def context_menu(self, data):
        return []

    def copy2clipboard(self, v):
        pyperclip.copy(v)


if __name__ == "__main__":
    DataFormat()
