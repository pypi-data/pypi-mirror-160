import re


class Parser:
    def __removeBracketed(self, title: str) -> str:
        return re.sub(r"[\s_.]*\[[^\]]*\][\s_.]*", " ", title)

    def __removeParends(self, title: str) -> str:
        return re.sub(r"[\s_.]*\([^)]*\)[\s_.]*", " ", title)

    def __removeFileExtension(self, title: str) -> str:
        extensions = [".mkv", ".mp4"]
        if any(ext in title for ext in extensions):
            return title[0 : title.rindex(".")]
        return title

    def __removeDelimiter(self, title: str) -> str:
        if r" " not in title:
            title = re.sub(r"\.", " ", title)
            return re.sub(r"\_", " ", title)
        return title

    def dir_parse(self, title: str) -> str:
        parsed_title = title.strip()

        if "&#39;" in parsed_title:
            parsed_title = parsed_title.replace("&#39;", "'")

        parsed_title = self.__removeFileExtension(parsed_title)
        parsed_title = self.__removeDelimiter(parsed_title)
        parsed_title = self.__removeBracketed(parsed_title)
        parsed_title = self.__removeParends(parsed_title)

        return parsed_title.strip()

    def parse(self, title: str) -> str:
        return self.dir_parse(title)
