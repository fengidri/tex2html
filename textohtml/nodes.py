# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-03-16 09:13:46
#    email     :   fengidri@yeah.net
#    version   :   1.0.1
from words import Word
import logging

class LostParamsEx(Exception):
    def __init__(self, word):
        print "%s:%s Lost Param" % (word.pos[0], word.pos[1])

class node_text(object):
    def __init__(self, ws):
        self.word = ws.getword()
        self.context = ws.getcontext(self.word)

        ws.update()

    def html(self):
        return self.context

class node_cpunc(object): # 形如: \%
    def __init__(self, ws):
        self.word = ws.getword()
        self.context = ws.getcontext(self.word)[1:2]

        ws.update()
    def html(self):
        return self.context

class node_comment(object):
    def __init__(self, ws):
        ws.update()

    def html(self):
        return ''

class node_typing(object):
    def __init__(self, ws):
        s = len('\starttyping')
        e = len('\stoptyping')
        self.word = ws.getword()
        ws.update()
        self.context = ws.getcontext(self.word)[s: -1 * e]

    def html( self ):
        tp = self.context

        tp = tp.replace('&', "&amp;" )
        tp = tp.replace(  '<', '&lt;' )
        tp = tp.replace(  '>', '&gt;' )
        return "<pre>%s</pre>\n" %  tp

class node_punc(object):
    def __init__(self, ws):
        self.word = ws.getword()
        word = self.word

        self.name =  self.word.name()

        if self.name == '%':
            ws.find('\n')
            self.h =  ''

        elif self.name == ' ':
            _ws, e = ws.find_same(' ')
            if e:# 忽略最后空格
                self.h = ''
            else:
                self.h =  ' '

        elif self.name == '\n':
            _ws, e = ws.find_same('\n')
            if e:# 忽略最后换行
                self.h = ''
            elif len(_ws) > 1:
                self.h = "</p>\n\n<p>"
            else:
                self.h = '\n'

        elif self.name == '$':
            #TODO
            ws.find('$')
            self.h = ''

        else:
            self.h = self.name
            ws.update()


    def html(self):
        return self.h

class node_control(object): 
    """
        1. 控制序列后面出现的{}, [], 一定会被处理掉
        2. 控制序列后面出现的\n, space 也会被处理掉
    """
    def __init__(self, ws):
        self.ws = ws
        self.Params = []
        self.Attrs  = []

        #list.__init__(self)
        self.word = ws.getword()
        self._getattrs(ws)
        self._getparams(ws)
        self.init(ws)

    def init(self, ws):
        ws.update()

    def html(self):
        return ''
    def _getparams(self, ws): # 得到参数, 参数可以有多个, {}
        self.__get_params_or_attrs(ws, '{', '}', self.Params)

    def _getattrs(self, ws): # 得到属性, 也可以有多个, []
        self.__get_params_or_attrs(ws, '[', ']', self.Attrs)

    def __get_params_or_attrs(self, ws, s, e, cb):
        cr_num = 0
        logging.debug("get params or attrs for %s",  ws.getword().show())
        while True:
            ws.update()
            word = ws.getword()
            if not word:
                break

            name = word.name()

            # 序列后的空格可以被吃掉,  同样参数后的空格也会被吃掉
            if name == ' ': continue

            #但是回车只能吃一个空格
            if name == '\n':
                if cr_num == 0:
                    cr_num += 1
                    continue
                else:
                    ws.back()
                    break

            if name == s:
                # TODO 这里的nesting 还要进行思考
                ps = ws.findnesting(e, nesting=s)
                p = node_tree(ps.slice(1, -1))
                ws.getword().show()
                cb.append(p)
                cr_num = 0# 一个参数后, 可以再吃一个空格
                ws.back()
                ws.getword().show()
            else:
                ws.back()
                break


class Section( node_control ):
    def init(self, ws):
        ws.update()
        self.name = self.word.name()

    def html( self ):
        name = self.name
        level = name.count('sub') + 3

        if not self.Params:
            raise LostParamsEx(self.word)

        c = self.Params[0].html()
        h = "\n<h%s>%s</h%s>\n" % (level, c, level)
        return h
        



class Itemize( node_control ):
    def init(self, ws):
        _ws = ws.findnesting("\stopitemize", nesting='\startitemize', inside = False)
        self.tree = node_tree(_ws.slice(0, -1))

    def html(self ):
        return "\n    <ul>\n%s\n    </ul>" % self.tree.html()


class Item( node_control ):
    def init(self, ws):
        pass

    def html( self ):
        #if self.param:
        #    return '\n<li><b>%s</b>&nbsp;&nbsp;&nbsp;&nbsp;' % self.param[0].html()
        #TODO
        return '\n        <li>'


class Goto( node_control ):

    def html( self ):
        return "&nbsp;<a href=%s >%s</a>&nbsp;" % (self.Params[1].html(), 
                self.Params[0].html())
        return ''

class Img( node_control ):
    def html( self ):
        #TODO 
        return "<img src=%s >" % (self.Param[0].html())

class Par( node_control ):
    def html( self ):
        return "<br />"


class starttable(node_control):
    def html( self ):
        return "<table>\n"

class stoptable(node_control):
    def html( self ):
        return "</table>\n"

class NC(node_control):
    def html( self ):
        return  "<tr><td>"

class AR(node_control):
    def html( self ):
        return  "</td></tr>\n"

class VL(node_control):
    def html( self ):
        return "</td><td>"

class VL(node_control):
    def html( self ):
        return "</td><td>"

class Bold(node_control):
    def html(self):
        if len(self.Params) > 0:
            return "<b>%s</b>" % self.Params[0].html()
        return ""

class Newline(node_control):
    def html(self):
        return "</p>\n\n<p>"

class DefHandle(node_control):
    MAPS = {}
    def init(self, ws):
        ws.update()
        name = self.word.name()
        self.de = self.MAPS.get(name)
        if not self.de:
            raise Exception("Dont kwow: %s(%s)" % (name, self.word.pos))
    def html(self):
        return self.de.Params[0].html()

class Def(node_control):
    def init(self, ws):
        while True:
            ws.update()
            word = ws.getword()
            name = word.name()
            if name in ['\n', ' ']:
                continue
            if word.type == Word.TYPE_CONTROL:
                self._getattrs(ws)
                self._getparams(ws)
                DefHandle.MAPS[name] = self
                break
        ws.update()

    def html(self):
        return ''

class backslash(node_control):

    def html(self):
        return '\\'


NODE_MAP={ 
        '\section'       : Section,
        '\subsection'    : Section,
        '\subsubsection' : Section,
        '\startitemize'  : Itemize,
        '\item'          : Item,
        '\goto'          : Goto,
        '\img'           : Img,
        '\par'           : Newline,
        '\starttable'    : starttable,
        '\stoptable'     : stoptable,
        '\NC'            : NC,
        '\VL'            : VL,
        '\AR'            : AR,
        '\\bold'         : Bold,
        '\\def'          : Def,
        '\\backslash'            : backslash,
                }

class node_tree(list):
    handlemap = {
            Word.TYPE_PUNC:    node_punc,
            Word.TYPE_TEXT:    node_text,
            Word.TYPE_CPUNC:   node_cpunc,
            Word.TYPE_COMMENT: node_comment,
            Word.TYPE_TYPING:  node_typing,
            }
    def __init__(self, ws):
        # 跳过开头的空白
        logging.debug("node tree: from %s to %s" , ws.start, ws.end)
        while True:
            w = ws.getword()
            if not w:
                break
            if not w.name() in ['\n', ' ']:
                break
            ws.update()

        while True:
            w = ws.getword()
            if not w:
                break
            logging.debug("node tree: scan word: %s, pos: %s, end: %s, wpos: %s", 
                    w.showname(), ws.pos, ws.end, w.pos)

            cb = self.handlemap.get(w.type)
            if cb: self.append(cb(ws))

            elif w.type == Word.TYPE_CONTROL:
                callback = NODE_MAP.get(w.name())
                if not callback:
                    callback = DefHandle
                self.append(callback(ws))

        logging.debug("node tree exit: from %s to %s @ %s" , ws.start, ws.end, 
                ws.pos)

    def html(self):
        h = [n.html() for n in self]
        return ''.join(h)



if __name__ == "__main__":
    pass

