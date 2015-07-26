# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-03-16 16:19:37
#    email     :   fengidri@yeah.net
#    version   :   1.0.1


# 把 语法做生成 段落
import logging

def paragraph(syn_list):
    paragraphs = []
    parag = []
    for tok in syn_list:
        if tok.name in ['\section', '\subsection', '\subsubsection']:
            if parag:
                paragraphs.append(parag)
            paragraphs.append(tok)
            parag = []
            continue

        if tok.name == '\par' or (tok.name == '\n' and tok.len > 1):
            paragraphs.append(parag)
            parag = []
            continue

        parag.append(tok)
    if parag:
        paragraphs.append(parag)
    return paragraphs


if __name__ == "__main__":
    import syntactic
    import codecs
    import token

    f = codecs.open('../index.mkiv', 'r','utf8')
    tokens = token.PaserToken(f.read())
    syn_list = syntactic.Syntax(tokens).syntax()
    pars = paragraph(syn_list)
    for p in pars:
        print "*******************************"
        if isinstance(p, list):
            syntactic.debug(p, 2)
        else:
            print ">>>>>>>>>", p.infostr()

