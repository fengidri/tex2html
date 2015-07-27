# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-07-26 16:05:52
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

import token
CVT_ARG1 = 1
CVT_ARG2 = 2
CVT_SYNTAX = 10
CVT_PAR = 20
CVT_TYPING = 30

html_convert = {
        "@par":           ("\n<p>",       CVT_PAR,     '\n</p>\n'),
        "\section":       ("\n<h3>",      CVT_ARG1,    '</h3>\n'),
        "\subsection":    ("\n<h4>",      CVT_ARG1,    '</h4>\n'),
        "\subsubsection": ("\n<h5>",      CVT_ARG1,    '</h5>\n'),
        "\startitemize":  ("\n<ul>\n",    CVT_SYNTAX,  '\n</ul>\n'),
        "\starttyping":   ("\n<pre>",     CVT_TYPING,  '</pre>\n'),
        "\item":          ("\n<li>"),
        "\goto":          ("<a href=",  CVT_ARG2,  '>', CVT_ARG2, "</a>"),
        "\img":           ("<img src=", CVT_ARG1,  ' ></img>'),
        "\starttable":    ("<table>\n", CVT_SYNTAX,    '\n</table>'),
        "\NC"   :         ('<tr><td>'),
        '\AR':            ('</td></tr>\n'),
        '\VL':            ('</td></td>'),
        '\\bold':         ("<b>", CVT_ARG1, "</b>")
        }


class Convert(object):
    def __init__(self, fd, cvt):
        self.fd = fd
        self.cvt = cvt # 转换表


    def handle_convert(self, tok):
        if tok.Type ==  token.TYPE_CONTROL:
            sq = self.cvt.get(tok.name)
            if not sq:
                raise Exception("%s: Dont Know" % tok.infostr())
            for s in sq:
                if isinstance(s, basestring):
                    self.fd.write(s)

                elif CVT_ARG1 == s:
                    if len(tok.args) <= 0:
                        raise Exception("%s: except 1 args" % tok.infostr())
                    else:
                        for _tok in tok.args[0]:
                            self.handle_convert(_tok)

                elif CVT_ARG2 == s:
                    if len(tok.args) <= 1:
                        raise Exception("%s: except 2 args" % tok.infostr())
                    else:
                        for _tok in tok.args[1]:
                            self.handle_convert(_tok)

                elif CVT_SYNTAX == s:
                        for _tok in tok.syntax:
                            self.handle_convert(_tok)
                elif CVT_TYPING == s:
                    tok.write(self.fd)
        else:
            tok.write(self.fd)

    def handle_par(self, par):
        length = len(par)
        start = 0
        while start < length:
            if not par[start].name in [' ', '\n', '\\ ']:
                break
            start += 1

        if start >= length: # 处理段落空的情况
            return

        for o in self.cvt.get('@par'):
            if isinstance(o, basestring):
                self.fd.write(o)

            if o == CVT_PAR:
                for i in range(start, length):
                    self.handle_convert(par[i])


    def convert(self, pars):
        for p in pars:
            if isinstance(p, list): # is par
                self.handle_par(p)

            else:
                self.handle_convert(p)



if __name__ == "__main__":
    import syntactic
    import codecs
    import token
    import paragraph

    f = codecs.open('../index.mkiv', 'r','utf8')
    tokens = token.PaserToken(f.read())
    syn_list = syntactic.Syntax(tokens).syntax()
    pars = paragraph.paragraph(syn_list)

    import sys
    ct  = Convert(sys.stdout, html_convert)
    ct.convert(pars)

    pass

