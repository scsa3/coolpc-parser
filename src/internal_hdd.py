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
        self.brand = self.describe.split()[0]
        self.size = self.get_size()
        self.series = self.get_series()
        self.memory = self.get_memory()
        self.model = self.get_model()
        self.rpm = self.get_rpm()
        self.warranty = self.get_warranty()
        self.price = self.get_price()
        self.cp_value = self.size * 1_000_000 / self.price

    def get_size(self):
        match = re.search(r"(\d+)(TB|G)", self.describe)
        size, unit = int(match.group(1)), match.group(2)
        return size//1000 if unit == 'G' else size

    def get_series(self):
        match = re.search(r"(?<=【)[\w ]+(?=】)", self.describe)
        if match:
            return match.group()

    def get_memory(self):
        match = re.search(r"(?<=\()?\d+(?=MB?)", self.describe)
        if match:
            return match.group()

    def get_model(self):
        match = re.search(r"(?<=\()(\w|^/)+(?=\))", self.describe)
        if match:
            return match.group()

    def get_rpm(self):
        match = re.search(r"(?<=/)\d+(?=轉/)", self.describe)
        if match:
            return int(match.group())

    def get_warranty(self):
        match = re.search(r"(?<=/)\w(?=年)", self.describe)
        if match:
            return translator[match.group()]

    def get_price(self):
        match = re.search(r"(?<=\$)(\d+)", self.describe)
        return int(match.group())


def save_to_html(options: list):
    template_filename = BASE_DIR/"templates/internal-hdd.jinja2"
    with open(template_filename, encoding='utf8') as f:
        template = Template(f.read())

    html_output_filename = BASE_DIR/"res/html/internal-hdd.html"
    with open(html_output_filename, mode='w', encoding='utf8') as f:
        f.write(template.render(items=options, update_time=datetime.now()))


if __name__ == '__main__':
    save_to_html(InternalHdd().options)
