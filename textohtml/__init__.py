# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-03-16 09:15:24
#    email     :   fengidri@yeah.net
#    version   :   1.0.1
import codecs

import logging

logging.basicConfig(level = logging.DEBUG)

from words import split
from nodes import node_tree

def open_source_to_words(f):
    f = codecs.open(f, 'r','utf8')
    return split(f.read())

def savehtml(o, words):
    f = codecs.open(o, 'w','utf8')
    f.write(node_tree(words).html())


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-i")
    parser.add_argument("-o")


    args = parser.parse_args()
    savehtml(args.o, open_source_to_words(args.i))


if __name__ == "__main__":
    main()
    pass

