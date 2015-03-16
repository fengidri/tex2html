# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-03-16 16:19:37
#    email     :   fengidri@yeah.net
#    version   :   1.0.1
from nodes import Section, node_tree

SPLITER = ['\section', '\subsection', '\subsubsection']
SPLITERCALL = [Section, Section, Section]
MAXLEVEL = 2

class ParSection(object):

    def __init__(self, ws, Level, hide = False):
        self.section = None
        self.Paragraph = None
        self.subParagraph = None
        if not hide:
            self.section = SPLITERCALL[Level](ws)

        if Level >= MAXLEVEL:
            self.subParagraph = node_tree(ws)
        else:
            self.Paragraph = SplitParagraph(ws, Level + 1)

    def html(self):
        if self.section:
            h = self.section.html()
        else:
            h = ''
        if self.Paragraph:
            return h + self.Paragraph.html()
        else:
            return "%s<p>%s</p>\n" % (h ,self.subParagraph.html())






class SplitParagraph(list):
    def __init__(self, ws, level): # sn: section name
                                     # scn: section name callba

        print '---------'
        sn = SPLITER[level]
        snc = SPLITERCALL[level]
        sn_index = []

        index = 0
        while True:
            word = ws.getword()
            if not word:
                break
            if word.name() == sn:
                sn_index.append(index)
            ws.update()
            index += 1

        if not sn_index:
            _ws = ws.slice(0)
            self.append(ParSection(_ws, level, hide = True))
            return


        if sn_index[0] != 0:
            _ws = ws.slice(0, sn_index[0])
            self.append(ParSection(_ws, level, hide = True))

        index = 0
        while True:
            if index >= len(index) -1:
                break

            s = sn_index[index]
            e = sn_index[index + 1]
            _ws = ws.slice(s, e)
            print type(_ws)
            self.append(ParSection(_ws, level))

        _ws = ws.slice(sn_index[-1])
        self.append(ParSection(_ws, level))

    def html(self):
        h = [n.html() for n in self]
        return ''.join(h)



if __name__ == "__main__":
    pass

