# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-07-24 16:03:35
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

# 完成对于 控制序列的 参数, 选项的提取
# 处理\def 的替换
# 完成 item, typing 的语法树的生成

import token

TYPE_TREE = 10

RES_CONTINUE = 1
RES_STOP     = 0
RES_REDO     = 2 # 对于传进入来的 char 要重新处理一次
"""
\def CONTROL { TEX }
\section { TEX }
\subsection { TEX }
\subsubsection { TEX }
\sub
"""


class Syntax(object):
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.length = len(tokens)

    def get(self):
        if self.pos >= self.length:
            return None
        pos = self.pos
        self.pos += 1
        return self.tokens[pos]

    def syntax(self, stop_name = None):
        # 从当前的位置(self.pos)开始对于输入的token 流进行语法解析
        # 有两种情况会退出解析
        #    1. token 流已经结束了
        #    2. 遇到的 stop_name
        syntax = []
        while True:
            tok = self.get()
            if tok == None:
                break

            if stop_name and tok.name == stop_name:
                syntax.append(tok)
                break

            # tex 只要对于 control , texpunc 进行语法解析
            if tok.Type == token.TYPE_CONTROL:
                self.paser(tok)
                #tok.args, tok.opts = self.get_args_opts()

            syntax.append(tok)

        return syntax

    def paser(self, tok):
        #处理 tok paser,
        # 理想的情况下, 要依赖于一些数据规则. 这里在比较简单的情况下进行处理

        if tok.name == '\def':
            ctrl = self.except_control()
            if not ctrl:
                raise Exception("Not Found Control after : %s" % tok.infostr())

            group = self.except_group()
            if not group:
                raise Exception("Not Found group after : %s" % tok.infostr())
            tok.ctrl = ctrl
            tok.group = group
            return tok

        else:
            args = []
            opt = self.except_opts()
            while True:
                arg = self.except_group()
                if arg:
                    args.append(arg)
                else:
                    break

            tok.args = args
            tok.opts = opt
            return tok

        if tok.name == '\starttyping':
            while True:
                t = self.get()
                if not t:
                    raise Exception("Not Found \stoptyping after : %s" % tok.infostr())
                if t.name == '\stoptyping':
                    break
            tok.stop = t
            return tok

        elif tok.name == '\startitemize':
            sub = self.syntax('\stopitemize')
            if not sub:
                raise Exception("Not Found \stopitemize after : %s" % tok.infostr())
            token.sub = sub
            return token

        elif tok.name == '\starttable':
            sub = self.syntax('\stoptable')
            if not sub:
                raise Exception("Not Found \stoptable after : %s" % tok.infostr())
            token.sub = sub
            return token






    def find_plain(self, start_tok, stop_name):
        # 根据 stop name 找到对应的 stop, 如果没有找到就报错.
        # start 在报错的时候有用
        # 返回是包含有 stop token 的 list, start_tok 并不在其中
        sub = []
        while True:
            tok = self.get()
            if not tok:
                return None

            sub.append(tok)
            if tok.name == stop_name:
                return sub

    def except_group(self):
        while True:
            tok = self.get()
            if not tok:
                return None

            elif tok.name in [' ', '\n']:
                continue

            elif tok.name == '{':
                return self.syntax('}')

            else:
                return None

    def except_control(self):
        while True:
            tok = self.get()
            if not tok:
                return None

            elif tok.name in [' ', '\n']:
                continue

            elif tok.Type == token.TYPE_CONTROL:
                return tok

            else:
                return None

    def except_opts(self):
        while True:
            tok = self.get()
            if not tok:
                return None

            elif tok.name in [' ', '\n']:
                continue

            elif tok.name == '[':
                return self.find_plain(tok, '}')

            else:
                return None


    def get_args_opts(self):
        opts = []
        args = []

        def _get():# 得到[ 或 {
            while True:
                tok = self.get()
                if not tok:
                    return None

                elif tok.name in [' ', '\n']:
                    continue

                elif tok.name  in ['[', '{']:
                    return tok

                else:
                    return None

        def _find():
            cur_pos = self.pos
            tok = _get()
            if not tok:
                self.pos = cur_pos
                return False

            if tok.name == '[':
                opt = self.find(tok, ']')
                opt.pop()
                opts.append(opt)
                return True

            if tok.name == '{':
                arg = self.find(tok, '}')
                arg.pop()
                args.append(arg)
                return True

        while _find():
            pass

        return (args, opts)










if __name__ == "__main__":
    import codecs
    f = codecs.open('../index.mkiv', 'r','utf8')

    syn = Syntax(token.PaserToken(f.read()))


    for tok in syn.syntax():
        print tok.infostr()
        if hasattr(tok, 'group'):
            for t in tok.group:
                print '    group', t.infostr()

        if hasattr(tok, 'args'):
            for t in tok.args:
                print '    args', t.infostr()
        #if tok.Type == token.TYPE_CONTROL:
        #    print tok.name
        #    for arg in tok.args:
        #        for a in arg:
        #            print '  @:', a.infostr()
        #        print ''

        #    for a in tok.opts:
        #        print '+:', a.infostr()

        #    print '--------------------'


