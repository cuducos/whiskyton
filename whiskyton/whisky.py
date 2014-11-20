# coding: utf-8

import re


def slugfy(string):
    regex = re.compile('[^a-zA-Z]+')
    string = regex.sub('', string)
    return string.lower()
