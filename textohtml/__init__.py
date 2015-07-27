# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-03-16 09:15:24
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

#TODO  最后的一个text会没有输出

import logging

import codecs

#logging.basicConfig(level = logging.DEBUG, format = '%(message)s')
logging.basicConfig(level = logging.ERROR, format = '%(message)s')

import token
import syntactic
import paragraph
import convert

def handle(out, cvt, buf):


    tokens = token.PaserToken(buf)
    syn_list = syntactic.Syntax(tokens).syntax()
    pars = paragraph.paragraph(syn_list)
    ct = convert.Convert(out, cvt)
    ct.convert(pars)


def markdown(path=None, buf=None):
    ws = handle(path, buf)
    if not ws:
        return ''

    return ws.md()

def html(out,  path):
    buf = codecs.open(path, 'r','utf8').read()
    ws = handle(out, convert.html_convert, buf)

def texstohtml(src, o):
    import traceback
    try:
        words = prehandler(split(src))
        html = SplitParagraph(words, 0).html()
    except:
        html = '<pre>%s</pre>' % traceback.format_exc()


    f = codecs.open(o, 'w','utf8')
    f.write(html)

if __name__ == "__main__":
    pass

