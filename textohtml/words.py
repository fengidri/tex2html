# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-03-16 09:13:29
#    email     :   fengidri@yeah.net
#    version   :   1.0.1
import logging
logging.basicConfig(level = logging.INFO, format = '%(message)s')


class Token(object):
    TYPE_CONTROL = 1  # 控制序列
    TYPE_TEXT    = 3  # 文字
    TYPE_TEXPUNC = 4  # 形如\# \$ \% \^ \& \_ \{ \} \~ \\
    TYPE_COMMENT = 5

    RES_CONTINUE = 1
    RES_STOP     = 0
    RES_REDO     = 2 # 对于传进入来的 char 要重新处理一次

    tokes = []
    Source       = None
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

class Token_Text(Token):
    Type = Token.TYPE_TEXT
    def log(self):
        logging.info("@%s: TEXT: %s", self.position(), self.content())


class Token_TexPunc(Token):
    Type = Token.TYPE_TEXPUNC
    def __init__(self, char):
        Token.__init__(self, char)
        self.punc = char[0]

    def log(self):
        s = self.content().replace(' ', '\<space>').replace('\n', '\<cr>')
        logging.info("@%s: TexPunc : %s", self.position(), s)

    def update(self, char):
        if self.punc == ' ':
            if char[0] == ' ':
                return Token.RES_CONTINUE
            else:
                self.e = char[3] - 1
                return Token.RES_REDO

        if self.punc == '\n':
            if char[0] == '\n':
                return Token.RES_CONTINUE
            else:
                self.e = char[3] - 1
                return Token.RES_REDO

        self.e = char[3] - 1
        return Token.RES_REDO



class Token_Comment(Token):
    Type = Token.TYPE_COMMENT
    def update(self, char):
        if char[0] == '\n':
            self.e = char[3]
            return Token.RES_STOP
        return Token.RES_CONTINUE

    def log(self):
        comment = self.content()
        comment = comment.replace('\n', '\\n')
        logging.info("@%s: Comment : %s", self.position(), comment)

class Token_Control(Token):
    Type = Token.TYPE_CONTROL
    except_space = False

    def log(self):
        comment = self.content()
        comment = comment.replace('\n', '\\n')
        logging.info("@%s: Control : %s", self.position(), comment)

    def update_end(self, char):
        self.stop(char[3])

    def update(self, char):
        c = char[0]
        if char[3] - self.s == 1:
            if c in ['#', '$', '%', '^', '&', '_', '{', '}', '~', '\\']:
                # 形如: \$ \#
                self.e = char[3]
                return Token.RES_STOP

            elif not (c.islower()  or c.isupper()):
                raise Exception("Control Token Error: @%d,%d" % (self.s[1], self.s[2]))

            else:
                return Token.RES_CONTINUE

        if self.except_space:
            if c == ' ' or c == '\r': # 形如 "\section    "
                return Token.RES_CONTINUE
            else:
                return Token.RES_REDO
        else:
            if c == ' ':
                self.e = char[3] - 1
                self.except_space = True
                return Token.RES_CONTINUE

            if c.islower() or c.isupper():
                return Token.RES_CONTINUE
            else:
                self.e = char[3] - 1
                return Token.RES_REDO



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
            if Token.RES_STOP == res:
                CurToken = None

            elif Token.RES_REDO == res:
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











class Words(object):# 对于进行词法分析的结果进行包装, 是语法分析中的依赖
    def __init__(self, source, start = 0, end = None, words = None):
        self.source = source # 记录source, 不是source 对象
        if not words:
            words = []
        self.words = words

        self.start = start
        if not end: end = len(self.words)
        self.end = end

        self.pos = start
    def show(self):
        return (self.start, self.end, self.pos)

    def getall(self, name):# 得到所有名为name 的word 在Words中的index
        sn_index = []
        for index, w in enumerate(self.words[self.pos: self.end]):
            if w.name() == name:
                sn_index.append(index + self.pos - self.start)
        return sn_index

    def getpos(self):
        return self.pos

    def initpos(self, pos):
        self.pos = pos


    def reinit(self):
        self.pos = self.start

    def append(self, w):
        self.words.append(w)
        self.end += 1

    def getcontext(self, word):
        # 依据word 的pos 与length 得到对应的source
        pos = word.pos[2]
        length = word.len
        return self.source[pos: pos + length]

    def get_context_between(self, w1, w2): # 得到两个word 中间的context, 开区间
        s = w1.pos[2] + w1.len
        e = w2.pos[2]
        return self.source[s: e]

    def findnesting(self, name, nesting, inside = True): # 可以嵌套
        # 如果开启了nesting, 那么对于
        logging.debug('find:ws:%s', self.show())
        if inside:
            level = 0
        else:
            level = 1
        for index, w in enumerate(self.words[self.pos: self.end]):
            if w.name() == nesting:
                level += 1
            if w.name() == name:
                if level > 1:
                    level -= 1
                    continue

                pos = self.pos + index
                ws = self.slice(self.pos - self.start, pos - self.start + 1)
                self.pos = pos + 1
                return ws
        else:
            w = self.words[self.pos]
            msg = "NOT FOUND:%s from %s, %s" % (name, w.pos[0], w.pos[1])
            raise Exception(msg)

    def find(self, name, nesting = False): # nesting是不是可以嵌套
        # 如果开启了nesting, 那么对于
        logging.debug('find:ws:%s', self.show())
        for index, w in enumerate(self.words[self.pos: self.end]):
            if w.name() == name:
                pos = self.pos + index
                ws = self.slice(self.pos - self.start, pos - self.start + 1)
                self.pos = pos + 1
                return ws
        else:
            w = self.words[self.pos]
            msg = "NOT FOUND:%s from %s, %s" % (name, w.pos[0], w.pos[1])
            raise Exception(msg)

    def find_same(self, name):
        end = False
        for index, w in enumerate(self.words[self.pos: self.end]):
            if w.name() != name:
                pos = self.pos + index
                break
        else:
            end = True
            pos = self.pos + index  + 1

        ws = self.slice(self.pos - self.start, pos - self.start)
        self.pos = pos
        return (ws, end)
    def sliceto(self, end):
        if end:
            if end < 0:
                end = self.end + end
            else:
                end = self.start + end
        else:
            end = self.end

        start = self.pos

        return Words(self.source, words = self.words, start= start, end = end)


    def slice(self, start, end=None):
        if end:
            if end < 0:
                end = self.end + end
            else:
                end = self.start + end
        else:
            end = self.end

        start = self.start + start

        return Words(self.source, words = self.words, start= start, end = end)

    def getword(self):
        if self.pos < self.start or self.pos >= self.end:
            return None
        return self.words[self.pos]

    def getword_byindex(self, index):
        if index < 0:
            index = self.end + index
        else:
            index = self.start + index

        if index >= self.end or index < self.start:
            return None
        #print self.pos, ' ', self.end, ' ', self.start, len(self.words)
        return self.words[index]

    def update(self):
        self.pos += 1

    def back(self): # 使用要注意
        self.pos -= 1

    def __len__(self):
        return self.end - self.start

if __name__ == "__main__":
    import codecs
    f = codecs.open('../index.mkiv', 'r','utf8')

    for t in PaserToken(f.read()):
        t.log()






















