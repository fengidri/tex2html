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
        "\goto":          ("<a href=",  CVT_ARG2,  '>', CVT_ARG1, "</a>"),
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
        self.par_write_type = 0
        self.index_number = [0, 0, 0]

        self.handle_map = {
                token.TYPE_TEXT_PUNC: self.handle_token_text_punc,
                token.TYPE_TEXT_CN: self.handle_token_text_cn,
                token.TYPE_TEXT_EN: self.handle_token_text_en,
                token.TYPE_CONPUNC: self.handle_token_conpunc,
                token.TYPE_CONTROL: self.handle_token_control,
                token.TYPE_TEXPUNC: self.handle_token_texpunc,
                }

    def handle_token_text_en(self, tok):
        self.fd.write(' ')
        self.fd.write(tok.name)
        self.par_write_type = token.TYPE_TEXT_EN

    def handle_token_text_cn(self, tok):
        if self.par_write_type == TYPE_TEXT_EN:
            self.fd.write(' ')

        self.fd.write(token.name)
        self.par_write_type = token.TYPE_TEXT_CN

    def handle_token_text_punc(self, tok):
        self.fd.write(tok.name)

    def handle_token_conpunc(self, tok):
        self.fd.write(tok.name[1])

    def handle_token_texpunc(self, tok):
        pass

    def add_index_number(self, tok):
        if tok.name == '\section':
            level = 0
        elif tok.name == '\subsection':
            level = 1
        elif tok.name == '\subsubsection':
            level = 2
        else:
            return

        for i in range(level + 1, len(self.index_number)):
            self.index_number[i]  = 0

        self.index_number[level] += 1
        for i in self.index_number[0: level + 1]:
            self.fd.write(str(i))
            self.fd.write('.')

        self.fd.write(' ')


    def handle_token_control(self, tok):
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
                    self.add_index_number(tok)
                    self.handle_syntax(tok.args[0])

            elif CVT_ARG2 == s:
                if len(tok.args) <= 1:
                    raise Exception("%s: except 2 args" % tok.infostr())
                else:
                    self.handle_syntax(tok.args[1])

            elif CVT_SYNTAX == s:
                    self.handle_syntax(tok.syntax)

            elif CVT_TYPING == s:
                for c in tok.plain():
                    self.fd.write(c)

    def handle_syntax(self, syn_list):
        for tok in syn_list:
            self.handle_token(tok)

    def handle_token(self, tok):
        self.handle_map[tok.Type](tok)

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
                self.par_write_type = 0
                for i in range(start, length):
                    self.handle_token(par[i])
                self.par_write_type = 0


    def convert(self, pars):
        for p in pars:
            if isinstance(p, list): # is par
                self.handle_par(p)
            else:
                self.handle_token(p)



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

