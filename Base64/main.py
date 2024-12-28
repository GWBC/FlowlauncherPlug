# -*- coding: utf-8 -*-

import sys
import base64
import tkinter as tk

from tkinter import filedialog
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


class Base64(FlowLauncher):
    def __init__(self):
        self.util = Util("Base64.png")
        self.err = [
            self.util.makeRPC("en:编码字符串"),
            self.util.makeRPC("de:解码字符串"),
            self.util.makeRPC("ef:编码文件"),
            self.util.makeRPC("df:解码文件"),
        ]
        super().__init__()

    def query(self, query):
        s = str(query)
        s = s.split(":")
        if len(s) != 2:
            return self.err

        if s[0] == "en":
            base64_encode = base64.b64encode(s[1].encode("utf8")).decode("utf8")
            return [
                self.util.makeRPC(
                    "{}{}".format("编码:", base64_encode),
                    method="copy2clipboard",
                    args=[base64_encode],
                )
            ]

        if s[0] == "de":
            base64_decode = base64.b64decode(s[1]).decode("utf8")
            return [
                self.util.makeRPC(
                    "{}{}".format("解码:", base64_decode),
                    method="copy2clipboard",
                    args=[base64_decode],
                )
            ]

        if s[0] == "ef":
            data = None

            root = tk.Tk()
            root.withdraw()
            file_path = filedialog.askopenfilename(
                title="打开文件",
                filetypes=[
                    ("图片", "*.jpg *.jpeg *.png *.gif *.bmp *.tiff *.webp"),
                    ("所有", "*.*"),
                ],
            )
            if len(file_path) == 0:
                return
            with open(file_path, "rb") as f:
                data = base64.b64encode(f.read())

            save_path = filedialog.asksaveasfilename(
                title="保存编码文件",
                initialfile="base64.txt",
                defaultextension=".txt",
                filetypes=[("txt", "*.txt"), ("所有", "*.*")],
            )
            if data == None or len(save_path) == 0:
                return
            with open(save_path, "wb") as f:
                f.write(self.util.fileHeader(file_path).encode("utf8"))
                f.write(data)

            return []

        if s[0] == "df":
            data = None

            root = tk.Tk()
            root.withdraw()
            file_path = filedialog.askopenfilename(
                title="打开编码文件",
                initialfile="base64.txt",
                defaultextension=".txt",
                filetypes=[("txt", "*.txt"), ("所有", "*.*")],
            )
            if len(file_path) == 0:
                return
            with open(file_path, "rb") as f:
                fdata = f.read()
                fdatas = fdata.split(",".encode("utf8"))
                if len(fdatas) >= 2:
                    data = base64.b64decode(fdatas[1])
                else:
                    data = base64.b64decode(fdatas[0])

            save_path = filedialog.asksaveasfilename(
                title="保存文件", filetypes=[("所有", "*.*")]
            )
            if data == None or len(save_path) == 0:
                return
            with open(save_path, "wb") as f:
                f.write(data)

            return []

        return self.err

    def context_menu(self, data):
        return []

    def copy2clipboard(self, t):
        pyperclip.copy(str(t).strip())


if __name__ == "__main__":
    Base64()
