# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-03-16 09:13:29
#    email     :   fengidri@yeah.net
#    version   :   1.0.1


# 注意完成token 解析后可以由于注释的问题, 连续的换行不能连接起来
import logging
logging.basicConfig(level = logging.INFO, format = '%(message)s')

TYPE_CONTROL   = 1  # 控制序列
TYPE_TEXT_CN   = 3  # 文字
TYPE_TEXT_EN   = 7  # 文字
TYPE_TEXT_PUNC = 8  # , . ! "
TYPE_TEXPUNC   = 4  # # $ %
TYPE_CONPUNC   = 6  # 形如\# \$ \% \^ \& \_ \{ \} \~ \\
TYPE_COMMENT   = 5

RES_CONTINUE = 1
RES_STOP     = 0
RES_REDO     = 2 # 对于传进入来的 char 要重新处理一次

TEX_PUNC = ['#', '$', '%', '^', '&', '_', '{', '}', '~', '\\']


class Token(object):
    WRITE_TEXT_TYPE = 0

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


    def update(self, char):
        """
            0: over
            1. contiune
        """
        pass

    def infostr(self):
        s = self.name.replace(' ', '\<space>').replace('\n', '\<cr>')
        return "@%s:%s" % (self.position(), s)

    @property
    def len(self):
        return len(self.content())

class Token_TEXT_CN(Token):
    Type = TYPE_TEXT_CN
    def __init__(self, char):
        Token.__init__(self, char)
        self.name = char[0]

    def update(self, char):
        if char[0] == ' ':
            return RES_CONTINUE
        return RES_REDO


class Token_TEXT_EN(Token):
    Type = TYPE_TEXT_EN
    stop  = False

    @staticmethod
    def is_en(c):
        if c in [' ', '\n']:
            return False

        if c in TEX_PUNC:
            return False
        return True

    def update(self, char):
        c = char[0]

        if self.stop: # 吃掉英语 word 后面的空格
            if c == ' ':
                return RES_CONTINUE
            return RES_REDO
        else:
            #if c.islower() or c.isupper() or c.isdigit():
            if Token_TEXT_EN.is_en(c):
                return RES_CONTINUE
            else:
                self.e = char[3] - 1
                self.name = self.content()
                self.stop = True
                if c == ' ':
                    return RES_CONTINUE
                return RES_REDO

class Token_TEXT_PUNC(Token): # 一般行文中使用的标点符号
    Type = TYPE_TEXT_PUNC
    def __init__(self, char):
        Token.__init__(self, char)
        self.name = char[0]

    def update(self, char):
        if char[0] == ' ':
            return RES_CONTINUE
        return RES_REDO



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

class Token_Control(Token):
    Type = TYPE_CONTROL
    except_space = False

    @property
    def name(self):
        return self.content()

    def plain(self):
            i = self.plain_start.s
            while i < self.plain_stop.s:
                yield Token.Source[i]
                i += 1



    def update(self, char):
        c = char[0]
        if char[3] - self.s == 1:
            if c in TEX_PUNC:
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
        self.pos = 0
        self.length = len(source)

    def getchar(self): # 得到当前的char
        for i, c in enumerate(self.source):
            self.col += 1
            yield (c, self.line, self.col, i)
            if '\n' == c:
                self.line += 1
                self.col = 0

    def lines(self):
        def char():
            while True:
                if self.pos < self.length:
                    c = self.source[self.pos]
                else:
                    c = '\n'

                if c == '\n':
                    break

                self.pos += 1
                self.col += 1

                yield (c, self.line, self.col, self.pos)

        while self.pos < self.length:
            yield char()
            self.line += 1

class TokenPaser(object):
    def __init__(self, source):
        self.src = Source(source)

        for line in self.src.lines():
            self.handle_line(line)

    def handle_line(self, line):
        """
            N: NewLine
            S: Skip Space

        """
        status = 'N'
        length = 0

        for char in line:
            length += 1
            if status == 'S' and char[0] == ' ':
                continue

            self.handle_char(char)

            if status == 'R':
                status = self.handle_char(char)
                assert status != 'R'

        if length == 0:#\par
            pass


    def handle_char(self, char):
        c = char[0]
        if CurToken:
            res = CurToken.update(char)
            if RES_STOP == res:
                CurToken = None

            elif RES_REDO == res:
                CurToken = None
                return handle(CurToken, char)
            return CurToken

        if c == '%':
            CurToken = Token_Comment(char)

        elif c == '\\':
            CurToken = Token_Control(char)

        elif c in ['#','$','&','{','}', '^', '_', '~', '[', ']', ' ']:
            CurToken = Token_TexPunc(char)

        elif Token_TEXT_EN.is_en(c):
            CurToken = Token_TEXT_EN(char)

        elif ord(c) > 255: # not english
            CurToken = Token_TEXT_CN(char)

        else:
            CurToken = Token_TEXT_PUNC(char)
        return CurToken





if __name__ == "__main__":
    import codecs
    f = codecs.open('../index.mkiv', 'r','utf8')

    for t in PaserToken(f.read()):
       print  t.infostr()






















