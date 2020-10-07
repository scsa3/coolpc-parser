import re
from datetime import datetime
from pathlib import Path

from bs4.element import Tag
from jinja2 import Template

from utilits import get_index_soup, translator


class InternalHdd:
    def __init__(self):
        self.title = "傳統內接硬碟HDD"
        self.tag = self.get_tag()
        self.optgroups = self.get_optgroups()
        self.options = self.get_options()

    def get_tag(self):
        soup = get_index_soup()
        title_tag = soup.find(text=self.title)
        tag: Tag = title_tag.parent
        return tag

    def get_optgroups(self):
        optgroups = self.tag.find_all("optgroup")
        return optgroups

    def get_options(self):
        options = list()
        for group in self.optgroups:
            subtitle = group["label"]
            for option_tag in group.find_all("option"):
                if option_tag.has_attr("disabled"):
                    continue
                a_option = InternalHddOption(self.title, subtitle, option_tag.text)
                options.append(a_option)
        return options


class InternalHddOption:
    def __init__(self, title: str, subtitle: str, describe: str):
        self.title = title
        self.subtitle = subtitle
        self.describe = describe
        self.brand = self.get_brand()
        self.size = self.get_size()
        self.series = self.get_series()
        self.memory = self.get_memory()
        self.model = self.get_model()
        self.rpm = self.get_rpm()
        self.warranty = self.get_warranty()
        self.price = self.get_price()
        self.cp_value = self.get_cp_value()

    def get_brand(self):
        brand = self.describe.split()[0]
        return brand

    def get_size(self):
        match = re.search(r"(\d+)(TB|G)", self.describe)
        size = match.group(1)
        size = int(size)
        unit = match.group(2)
        if "G" == unit:
            size /= 1000
        return size

    def get_series(self):
        match = re.search(r"(?<=【)[\w ]+(?=】)", self.describe)
        if not match:
            return None
        series = match.group()
        return series

    def get_memory(self):
        match = re.search(r"(?<=\()?\d+(?=MB?)", self.describe)
        if not match:
            return None
        memory = match.group()
        return memory

    def get_model(self):
        match = re.search(r"(?<=\()(\w|^/)+(?=\))", self.describe)
        if not match:
            return None
        model = match.group()
        return model

    def get_rpm(self):
        match = re.search(r"(?<=/)\d+(?=轉/)", self.describe)
        if not match:
            return None
        rpm = match.group()
        return int(rpm)

    def get_warranty(self):
        match = re.search(r"(?<=/)\w(?=年)", self.describe)
        if not match:
            return None
        warranty = match.group()
        return translator[warranty]

    def get_price(self):
        match = re.search(r"(?<=\$)(\d+)", self.describe)
        price = match.group()
        return int(price)

    def get_cp_value(self):
        return self.size * 1_000_000 / self.price


def save_to_html(options: list):
    template_path = Path("../templates/internal-hdd.jinja2")
    content = template_path.read_text()
    template = Template(content)

    html = template.render(items=options, update_time=datetime.now())
    path = Path("../res/html/internal-hdd.html")
    path.write_text(html)


if __name__ == '__main__':
    x = InternalHdd()
    save_to_html(x.options)
