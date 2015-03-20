# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-03-16 09:15:24
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

#TODO  最后的一个text会没有输出
import codecs

import logging


#logging.basicConfig(level = logging.DEBUG, format = '%(message)s')
logging.basicConfig(level = logging.INFO, format = '%(message)s')

from words import split
from nodes import node_tree
from pre import prehandler
from paragraph import SplitParagraph

def open_source_to_words(f):
    f = codecs.open(f, 'r','utf8')
    return prehandler(split(f.read()))

def savehtml(o, words):
    f = codecs.open(o, 'w','utf8')
    f.write(SplitParagraph(words, 0).html())

def texstohtml(src, o):
    import traceback
    try:
        words = prehandler(split(src))
        html = SplitParagraph(words, 0).html()
    except:
        html = '<pre>%s</pre>' % traceback.format_exc()


    f = codecs.open(o, 'w','utf8')
    f.write(html)


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-i")
    parser.add_argument("-o")
    parser.add_argument('-w', type=int)
    args = parser.parse_args()

    if args.i:
        ws =open_source_to_words(args.i)

    if args.w:
        logging.info( ws.getword_byindex(args.w).show() )

    if args.o:
        savehtml(args.o, ws)



if __name__ == "__main__":
    main()
    pass

