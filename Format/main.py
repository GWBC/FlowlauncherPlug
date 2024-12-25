# -*- coding: utf-8 -*-

import sys, os, json
import urllib.parse

parent_folder_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(parent_folder_path)
sys.path.append(os.path.join(parent_folder_path, "lib"))
sys.path.append(os.path.join(parent_folder_path, "plugin"))

import pyperclip
from flowlauncher import FlowLauncher

from comm import makeRPC


class DataFormat(FlowLauncher):
    def __init__(self):
        self.err = [
            makeRPC("url:格式化URL"),
            makeRPC("json:格式化JSON"),
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
                return [makeRPC(fmtData)]
            except Exception as e:
                return [makeRPC("美化失败：{}".format(str(e)))]
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
                    makeRPC(fmtUrl, method="copy2clipboard", args=[fmtUrl]),
                    makeRPC(result, method="copy2clipboard", args=[result]),
                ]
            except Exception as e:
                return [makeRPC("美化失败：{}".format(str(e)))]
        return []

    def context_menu(self, data):
        return []

    def copy2clipboard(self, v):
        pyperclip.copy(v)


if __name__ == "__main__":
    DataFormat()
