from utilits import get_index_soup, translator
from jinja2 import Template
from bs4.element import Tag
import re
from datetime import datetime
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


class InternalHdd:
    def __init__(self):
        self.title = "傳統內接硬碟HDD"
        self.tag = self.get_tag()
        self.optgroups = self.tag.find_all("optgroup")
        self.options = []
        self.get_options()

    def get_tag(self):
        soup = get_index_soup(is_coolpc_having_fucking_garbage_html=True)
        title_tag = soup.find(text=self.title)
        tag: Tag = title_tag.parent
        return tag

    def get_options(self):
        for group in self.optgroups:
            subtitle = group["label"]
            for option_tag in group.find_all("option"):
                if option_tag.has_attr("disabled"):
                    continue
                self.options += [InternalHddOption(
                    self.title, subtitle, option_tag.text)]


class InternalHddOption:
    def __init__(self, title: str, subtitle: str, describe: str):
        self.title = title
        self.subtitle = subtitle
        self.describe = describe
        self.regex = {'size': r"(\d+)(TB|G)",
                      'series': r"(?<=【)[\w ]+(?=】)",
                      'memory': r"(?<=\()?\d+(?=MB?)",
                      'model': r"(?<=\()(\w|^/)+(?=\))",
                      'rpm': r"(?<=/)\d+(?=轉/)",
                      'warranty': r"(?<=/)\w(?=年)",
                      'price': r"(?<=\$)(\d+)"
                      }
        self.__get_data()

    def __search(self, regex_key: str):
        if regex_key not in self.regex:
            raise KeyError
        return re.search(self.regex[regex_key], self.describe)

    def __get_data(self):
        self.brand = self.describe.split()[0]

        match = self.__search('size')
        size, unit = int(match.group(1)), match.group(2)
        self.size = size//1000 if unit == 'G' else size

        match = self.__search('price')
        self.price = int(match.group())

        match = self.__search('rpm')
        self.rpm = int(match.group()) if match else None

        match = self.__search('warranty')
        self.warranty = translator[match.group()] if match else None

        match = self.__search('series')
        self.series = match.group() if match else None

        match = self.__search('memory')
        self.memory = match.group() if match else None

        match = self.__search('model')
        self.model = match.group() if match else None

        self.cp_value = self.size * 1_000_000 / self.price


def save_to_html(options: list):
    template_filename = BASE_DIR/"templates/internal-hdd.jinja2"
    html_output_filename = BASE_DIR/"res/html/internal-hdd.html"
    with open(template_filename, encoding='utf8') as t, open(html_output_filename, mode='w', encoding='utf8') as w:
        w.write(
            Template(t.read()).render(items=options,
                                      update_time=datetime.now()))


if __name__ == '__main__':
    save_to_html(InternalHdd().options)
