#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/2/22 15:34
# @Author  : 张大鹏
# @Site    : 
# @File    : exceptions1.py
# @Software: PyCharm

class StatusCodeError(Exception):
    def __init__(self, *args):
        super(StatusCodeError, self).__init__(*args)


class ParamError(Exception):
    def __init__(self, *args):
        super(ParamError, self).__init__(*args)


class EmptyError(Exception):
    def __init__(self, *args):
        super(EmptyError, self).__init__(*args)
