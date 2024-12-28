from pathlib import Path


class Util:
    def __init__(self, icon: str):
        self.__icon = icon

    def fileHeader(self, path):
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

    def makeRPC(
        self,
        title: str,
        subTitle: str = "",
        method: str = "",
        args: list = [],
        icon: str | None = None,
    ) -> str:
        if icon == None:
            icon = self.__icon

        rpc = {
            "Title": title,
            "SubTitle": subTitle,
            "IcoPath": "../Asset/Images/{}".format(icon),
            "JsonRPCAction": {},
        }

        if len(method) != 0:
            rpc["JsonRPCAction"] = {
                "method": method,
                "parameters": args,
            }
        return rpc
