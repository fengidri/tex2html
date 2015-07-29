# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-07-29 11:18:29
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

import token
import syntactic

import codecs
f = codecs.open('../index.mkiv', 'r','utf8')
src = f.read()

tp = token.TokenPaser(src)
syn = syntactic.SyntaxPaser()

tp.syn = syn
syn.tp = tp

tp.paser()



if __name__ == "__main__":
    pass

