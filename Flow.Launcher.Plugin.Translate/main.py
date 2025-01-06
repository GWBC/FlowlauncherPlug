import sys
from pathlib import Path

curPath = Path(__file__).parent

sys.path.append(str(curPath))
sys.path.append(str(curPath.joinpath("lib")))

from flox import Flox
from libretranslatepy import LibreTranslateAPI


class Translate(Flox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger_level("info")
        self.url = self.settings.get("url")
        self.lt = LibreTranslateAPI(self.url)

    def query(self, query):
        if len(query) == 0:
            return []
        return self.add_item(
            title=self.lt.translate(query, "en", "zh"),
        )

    def context_menu(self, data):
        self.logger.debug("context_menu:{}".format(str(data)))

    def exception(self, exception):
        self.logger.debug("exception:{}".format(str(exception)))

    def open_setting_dialog(self):
        self.logger.debug(
            "open_setting_dialog:{}".format(str(self.settings.get("url")))
        )


if __name__ == "__main__":
    Translate()
