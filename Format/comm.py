from pathlib import Path


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


def makeRPC(title: str, subTitle: str = "", method: str = "", args: list = []) -> str:
    rpc = {
        "Title": title,
        "SubTitle": subTitle,
        "IcoPath": "Images/app.png",
        "JsonRPCAction": {},
    }

    if len(method) != 0:
        rpc["JsonRPCAction"] = {
            "method": method,
            "parameters": args,
        }
    return rpc
