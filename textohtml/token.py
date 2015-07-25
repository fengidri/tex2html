# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-03-16 09:13:29
#    email     :   fengidri@yeah.net
#    version   :   1.0.1
import logging
logging.basicConfig(level = logging.INFO, format = '%(message)s')

TYPE_CONTROL = 1  # 控制序列
TYPE_TEXT    = 3  # 文字
TYPE_TEXPUNC = 4
TYPE_COMMENT = 5
TYPE_CONPUNC = 6# 形如\# \$ \% \^ \& \_ \{ \} \~ \\

RES_CONTINUE = 1
RES_STOP     = 0
RES_REDO     = 2 # 对于传进入来的 char 要重新处理一次

class Token(object):

    tokes = []
    Source       = None
    name = ''
    def __init__(self, char):
        self.l = char[1]
        self.c = char[2]
        self.s = char[3]
        self.e = None
        self.tokes.append(self)

    def position(self):
        return (self.l, self.c)

    def content(self):#
        if self.e:
            return Token.Source[self.s: self.e + 1]
        else:
            return Token.Source[self.s]

    def update_end(self, char):# 这里最后一个char
        self.e = char[3]

    def update(self, char):
        """
            0: over
            1. contiune
        """
        pass

    def infostr(self):
        s = self.name.replace(' ', '\<space>').replace('\n', '\<cr>')
        return "%s@%s" % (self.position(), s)

class Token_Text(Token):
    Type = TYPE_TEXT
    name = 'Text'


class Token_TexPunc(Token):
    Type = TYPE_TEXPUNC
    def __init__(self, char):
        Token.__init__(self, char)
        self.name = char[0]

    def update(self, char):
        if self.name == ' ':
            if char[0] == ' ':
                return RES_CONTINUE
            else:
                self.e = char[3] - 1
                return RES_REDO

        if self.name == '\n':
            if char[0] == '\n':
                return RES_CONTINUE
            else:
                self.e = char[3] - 1
                return RES_REDO

        self.e = char[3] - 1
        return RES_REDO




class Token_Comment(Token):
    Type = TYPE_COMMENT
    name = 'comment'
    def update(self, char):
        if char[0] == '\n':
            self.e = char[3]
            return RES_STOP
        return RES_CONTINUE

    def name(self):
        return 'comment'

class Token_Control(Token):
    Type = TYPE_CONTROL
    except_space = False

    @property
    def name(self):
        return self.content()

    def update_end(self, char):
        self.stop(char[3])

    def update(self, char):
        c = char[0]
        if char[3] - self.s == 1:
            if c in ['#', '$', '%', '^', '&', '_', '{', '}', '~', '\\']:
                # 形如: \$ \#
                self.e = char[3]
                self.Type = TYPE_CONPUNC
                return RES_STOP

            elif not (c.islower()  or c.isupper()):
                raise Exception("Control Token Error: @%d,%d" % (self.s[1], self.s[2]))

            else:
                return RES_CONTINUE

        if self.except_space:
            if c == ' ' or c == '\r': # 形如 "\section    "
                return RES_CONTINUE
            else:
                return RES_REDO
        else:
            if c == ' ':
                self.e = char[3] - 1
                self.except_space = True
                return RES_CONTINUE

            if c.islower() or c.isupper():
                return RES_CONTINUE
            else:
                self.e = char[3] - 1
                return RES_REDO



class Source(object): # 对于souce 进行包装
    def __init__(self, source):
        self.pos = 0
        self.line  = 1
        self.col = 0
        self.source = source

    def getchar(self): # 得到当前的char
        for i, c in enumerate(self.source):
            self.col += 1
            yield (c, self.line, self.col, i)
            if '\n' == c:
                self.line += 1
                self.col = 0




def PaserToken(source):
    def handle(CurToken, char):
        c = char[0]
        if CurToken:
            res = CurToken.update(char)
            if RES_STOP == res:
                CurToken = None

            elif RES_REDO == res:
                CurToken = None
                return handle(CurToken, char)

        elif c in ['%','#','$','&','{','}', '^', '_', '~', '[', ']', ' ', '\n']:
            CurToken = Token_TexPunc(char)

        elif c == '%':
            CurToken = Token_Comment(char)

        elif c == '\\':
            CurToken = Token_Control(char)

        else:
            Token_Text(char)
        return CurToken

    Token.Source = source
    CurToken = None


    for char in Source(source).getchar():
        CurToken = handle(CurToken, char)

    if CurToken:
        CurToken.update_end(char)

    return Token.tokes


if __name__ == "__main__":
    import codecs
    f = codecs.open('../index.mkiv', 'r','utf8')

    for t in PaserToken(f.read()):
        t.log()






















