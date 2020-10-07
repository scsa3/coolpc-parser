import requests
from bs4 import BeautifulSoup

translator = {
    "一": 1,
    "二": 2,
    "三": 3,
    "四": 4,
    "五": 5,
    "六": 6,
    "七": 7,
    "八": 8,
    "九": 9,
    "十": 10,
}


def get_index_soup() -> BeautifulSoup:
    url = "http://www.coolpc.com.tw/evaluate.php"
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    return soup
