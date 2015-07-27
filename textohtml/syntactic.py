# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-07-24 16:03:35
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

# 完成对于 控制序列的 参数, 选项的提取
# 处理\def 的替换
# 完成 item, typing 的语法树的生成

import token



class Syntax(object):
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.length = len(tokens)
        self.defs = {}

    def get(self):
        if self.pos >= self.length:
            return None
        pos = self.pos
        self.pos += 1
        return self.tokens[pos]

    def syntax(self, stop_name = None):
        # 从当前的位置(self.pos)开始对于输入的token 流进行语法解析
        #
        # 有两种情况会退出解析
        #    1. token 流已经结束了
        #    2. 遇到的 stop_name
        # 返回值:
        #  list: 这中间的每一个元素都是 token

        syntax = []
        while True:
            tok = self.get()
            if tok == None:
                break

            if tok.Type == token.TYPE_COMMENT:
                continue

            if tok.Type == token.TYPE_TEXPUNC:
                if tok.name == '{':
                    tok.syntax = self.syntax('}')
                    tok.syntax.pop()


            # tex 只要对于 control , texpunc 进行语法解析
            elif tok.Type == token.TYPE_CONTROL:
                group = self.defs.get(tok.name) # def 定义的新的控制序列
                if group:
                    syntax.extend(group)
                    continue
                tok = self.paser(tok)

            if tok:
                syntax.append(tok)
                if stop_name and tok.name == stop_name:
                    break

        return syntax

    def paser(self, tok):
        #处理 tok paser, 目前只对于控制序列进行 paser
        # 理想的情况下, 要依赖于一些数据规则. 这里在比较简单的情况下进行处理
        # 返回:
        #     None 解析后的 token 不用加入到 syntax 里
        #     Token 解析之后的 token.

        if tok.name == '\def':
            ctrl = self.except_control()
            if not ctrl:
                raise Exception("Not Found Control after : %s" % tok.infostr())

            group = self.except_group()
            if not group:
                raise Exception("Not Found group after : %s" % tok.infostr())

            self.defs[ctrl.name] = group
            return


        args = []
        opt = self.except_opts()
        while True:
            arg = self.except_group()
            if arg:
                args.append(arg)
            else:
                break

        # 所在有 syn_list 中的控制序列都有这两个参数 token

        tok.args = args # syn_list
        tok.opts = opt

        if tok.name == '\starttyping':
            tok.plain_start = self.get()
            while True:

                t = self.get()
                if not t:
                    raise Exception("Not Found \stoptyping after : %s" % tok.infostr())
                if t.name == '\stoptyping':
                    tok.plain_stop = t
                    break

        elif tok.name == '\startitemize':
            sub = self.syntax('\stopitemize')
            if not sub:
                raise Exception("Not Found \stopitemize after : %s" % tok.infostr())
            sub.pop()
            tok.syntax = sub # syn_list

        elif tok.name == '\starttable':
            sub = self.syntax('\stoptable')
            if not sub:
                raise Exception("Not Found \stoptable after : %s" % tok.infostr())
            tok.syntax = sub # syn_list

        return tok





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
        cur_pos = self.pos
        while True:
            tok = self.get()
            if not tok:
                self.pos = cur_pos
                return None

            elif tok.name in [' ', '\n']:
                continue

            elif tok.name == '{':
                sy =  self.syntax('}')
                sy.pop()
                return sy

            else:
                self.pos = cur_pos
                return None

    def except_control(self):
        cur_pos = self.pos
        while True:
            tok = self.get()
            if not tok:
                self.pos = cur_pos
                return None

            elif tok.name in [' ', '\n']:
                continue

            elif tok.Type == token.TYPE_CONTROL:
                return tok

            else:
                self.pos = cur_pos
                return None

    def except_opts(self):
        cur_pos = self.pos
        while True:
            tok = self.get()
            if not tok:
                self.pos = cur_pos
                return None

            elif tok.name in [' ', '\n']:
                continue

            elif tok.name == '[':
                return self.find_plain(tok, '}')

            else:
                self.pos = cur_pos
                return None





def debug(syntax, level  = 0):
    for tok in syntax:
        print '%s%s' % ('  ' * level, tok.infostr())
        if tok.Type == token.TYPE_CONTROL:
            for arg in tok.args:
                debug(arg, level + 1)
                print ''

            if hasattr(tok , 'syntax'):
                debug(tok.syntax, level + 1)








if __name__ == "__main__":
    import codecs
    f = codecs.open('../index.mkiv', 'r','utf8')

    syn = Syntax(token.PaserToken(f.read()))
    debug(syn.syntax())



