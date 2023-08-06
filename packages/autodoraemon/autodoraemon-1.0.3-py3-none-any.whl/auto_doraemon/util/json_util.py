#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
json 处理工具

@author:zhaojiajun
@file:json_util.py
@time:2022/07/28
"""

from deepdiff import DeepDiff


def is_same_json(src, tar):
    """
    对比两个json对象
    :param src:
    :param tar:
    :return: 返回对比结果和对比明细
    """
    detail = DeepDiff(src, tar)
    result = False if detail else True
    return result, detail


if __name__ == '__main__':
    json_1 = {"key1": 123, "key2": "test"}
    json_2 = {"key1": 123, "key2": "test1"}
    print(is_same_json(json_1, json_2))
