import hashlib
import uuid
from typing import List


def md5(s: str) -> str:
    """

    @param s: a string
    @return: string`s md5
    """
    m = hashlib.md5()
    m.update(s.encode("utf-8"))
    return m.hexdigest()


def gen_uuid() -> str:
    """

    @return: uuid4
    """
    return str(uuid.uuid4())


def get_padding_line(text: str, max_len: int = None, padding: str = None) -> str:
    """
    add padding to log text
    "some logs"  ==> "-------- some logs --------"

    :param text: log text
    :param max_len: padding len
    :param padding: padding character, default: -
    :return:
    """
    max_len = max_len or 60
    padding = padding or "-"

    text_len = len(text)
    if (text_len % 2) == 0:
        _size = (max_len - text_len) // 2
        side_str = padding * _size
        return f"{side_str} {text} {side_str}"
    else:
        _size = (max_len - text_len) // 2
        side_str = padding * _size
        return f"{side_str}{padding} {text} {side_str}"


def printl(data: str):
    print(get_padding_line(data))


def convert_dict_key(data_dict: dict, rule: dict) -> dict:
    """
    convert dict`s old key to new key with rule

    @param data_dict: origin dict data
    @param rule: some rules like {"old_key": "new_key"}
    @return:
    """
    if data_dict and rule:
        for k, v in rule.items():
            if k in data_dict:
                data_dict[v] = data_dict.pop(k)
    return data_dict


def convert_list_dict_key(data_list: List[dict], rule: dict) -> list:
    """
    convert dict-item`s old key to new key which is included in a list with rule

    @param data_list: List[dict]
    @param rule: some rules like {"old_key": "new_key"}
    @return:
    """
    if data_list and rule:
        for data_item in data_list:
            for k, v in rule.items():
                if k in data_item:
                    data_item[v] = data_item.pop(k)
    return data_list


def sqlescape(s: str):
    """
    simple sql escape
    @param s: sql
    @return:
    """
    return s.translate(
        s.maketrans(
            {
                "\0": "\\0",
                "\r": "\\r",
                "\x08": "\\b",
                "\x09": "\\t",
                "\x1a": "\\z",
                "\n": "\\n",
                '"': "",
                "'": "",
                "\\": "\\\\",
                "%": "\\%",
            }
        )
    )
