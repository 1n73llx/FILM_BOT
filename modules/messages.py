import json
from config import Config

class Messages:
    def __init__(
        self,
        lang_fetcher=None,
        default_lang=Config.BASE_LANGUAGE,
        base_path="./modules",
    ):
        self.lang_fetcher = lang_fetcher or (lambda _: default_lang)
        self.default_lang = default_lang
        self.base_path = base_path

    def __load_language_file(self, lang):
        file_path = f"{self.base_path}/{lang}.json"
        with open(file=file_path, mode="r", encoding="utf-8") as f:
            return json.load(fp=f)


    def get(self, file, key, user_id=None, extra_args=[]):
        lang = "en"
        messages = self.__load_language_file(lang)
        try:
            message = messages[file]
        except KeyError:
            message = self.__load_language_file(self.default_lang)[file][key.lower()]

        if not isinstance(extra_args, list):
            extra_args = [extra_args]

        return message.format(*extra_args)
