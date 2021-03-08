import requests
from bs4 import BeautifulSoup


zh_numbers = '一二三四五六七八九十'
translator = {zh_numbers[i]: i+1 for i in range(len(zh_numbers))}


def get_index_soup(is_coolpc_having_fucking_garbage_html=False) -> BeautifulSoup:
    url = "http://www.coolpc.com.tw/evaluate.php"
    resp = requests.get(url)
    html = resp.text if not is_coolpc_having_fucking_garbage_html else resp.text.replace(
        "<OPTGROUP", "</OPTGROUP><OPTGROUP")
    return BeautifulSoup(html, "html.parser")
