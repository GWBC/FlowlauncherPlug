# -*- coding: utf-8 -*-

import sys
import base64
from pathlib import Path

curPath = Path(__file__).parent

sys.path.append(str(curPath))
sys.path.append(str(curPath.joinpath("lib")))

import tkinter as tk
from tkinter import filedialog

import pyperclip
from flox import Flox


def fileHeader(path):
    exts = {
        ".jpg": "data:image/jpg",
        ".jpeg": "data:image/jpeg",
        ".png": "data:image/png",
        ".gif": "data:image/gif",
        ".bmp": "data:image/bmp",
        ".tiff": "data:image/tiff",
        ".webp": "data:image/webp",
    }

    ext = Path(path).suffix
    v = exts.get(ext.lower())
    if v is None:
        return ""
    return "{};base64,".format(v)


class Base64(Flox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger_level("debug")
        self.icon = "Images/icon.png"

    def __err(self):
        self.add_item(title="en:编码字符串")
        self.add_item(title="de:解码字符串")
        self.add_item(title="ef:编码文件")
        self.add_item(title="df:解码文件")

    def query(self, query):
        s = str(query)
        s = s.split(":")
        if len(s) != 2:
            self.__err()
            return

        if s[0] == "en":
            base64_encode = base64.b64encode(s[1].encode("utf8")).decode("utf8")
            self.add_item(
                title="{}{}".format("编码:", base64_encode),
                method="copy2clipboard",
                parameters=[base64_encode],
            )
            return

        if s[0] == "de":
            base64_decode = base64.b64decode(s[1]).decode("utf8")
            self.add_item(
                title="{}{}".format("解码:", base64_encode),
                method="copy2clipboard",
                parameters=[base64_decode],
            )
            return

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
                f.write(fileHeader(file_path).encode("utf8"))
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

        self.__err()

    def context_menu(self, data):
        return []

    def copy2clipboard(self, t):
        pyperclip.copy(str(t).strip())


if __name__ == "__main__":
    Base64()
