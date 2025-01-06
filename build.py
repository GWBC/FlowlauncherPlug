import os, json
import shutil
from pathlib import Path
from datetime import datetime

curPath = Path(__file__).parent
zipOutput = curPath.joinpath("output")
os.makedirs(zipOutput, exist_ok=True)


def getDirs() -> list[str]:
    ret: list[str] = []
    for root, dirs, files in os.walk(curPath):
        for dir in dirs:
            if dir.startswith("Flow"):
                ret.append(str(Path(root).joinpath(dir)))
    return ret


def getPlugins(dirs: list[str]) -> list[str]:
    ret: list[str] = []
    for dir in dirs:
        fpath = Path(dir).joinpath("plugin.json")
        if fpath.exists():
            ret.append(str(fpath))
    return ret


def procPlug(cfgPath: str) -> dict:
    parent = Path(cfgPath).parent
    output = zipOutput.joinpath(parent.name)

    shutil.make_archive(output, "zip", parent)

    with open(cfgPath, "r", encoding="utf8") as f:
        data = f.read()
        dataObj = json.loads(data)
        del dataObj["ActionKeyword"]
        del dataObj["ExecuteFileName"]
        dataObj["IcoPath"] = (
            "https://cdn.jsdelivr.net/gh/GWBC/FlowlauncherPlug@main/{}/Images/icon.png".format(
                parent.name
            )
        )
        dataObj["UrlSourceCode"] = dataObj["Website"]
        dataObj["UrlDownload"] = ""
        dataObj["Tested"] = True
        dataObj["DateAdded"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        dataObj["LatestReleaseDate"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        return dataObj


def procPlugins(plugs: list[str]) -> list[dict]:
    ret: list[dict] = []
    for ps in plugs:
        ret.append(procPlug(ps))
    return ret


def build():
    dirs = getDirs()
    plugs = getPlugins(dirs)
    for ps in plugs:
        print("获取插件：{}".format(ps))

    plugConfigs = procPlugins(plugs)
    print(json.dumps(plugConfigs))

    for root, dirs, files in os.walk(zipOutput):
        for file in files:
            print("输出插件：{}".format(str(Path(root).joinpath(file))))


if __name__ == "__main__":
    build()
