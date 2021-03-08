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


def get_index_soup(is_coolpc_having_fucking_garbage_html=False) -> BeautifulSoup:
    url = "http://www.coolpc.com.tw/evaluate.php"
    resp = requests.get(url)
    if is_coolpc_having_fucking_garbage_html:
        html = resp.text.replace("<OPTGROUP", "</OPTGROUP><OPTGROUP")
    else:
        html = resp.text
    soup = BeautifulSoup(html, "html.parser")
    return soup
