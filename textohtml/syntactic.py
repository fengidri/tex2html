# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-07-24 16:03:35
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

# 完成对于 控制序列的 参数, 选项的提取
# 完成 item, typing 的语法树的生成
# 处理\def 的替换

import token

RES_CONTINUE = 1
RES_STOP     = 0
RES_REDO     = 2 # 对于传进入来的 char 要重新处理一次

class Syntax_Control(object):
    def __init__(self, tok):
        self.tree = [tok]

    def update_end(self, tok):
        pass

    def update(self, tok):




def syntactic(tokens):
    syntax = []
    def handle(cur_syntax, tok):
        if cur_syntax:
            res = cur_syntax.update(tok)
            if RES_STOP == res:
                cur_syntax = None

            elif RES_REDO == res:
                syntax.append(cur_syntax)
                cur_syntax = None
                return handle(cur_syntax, tok)

        if tok.Type == token.TYPE_CONTROL:
            cur_syntax = Syntax_Control(tok)
        else:
            syntax.append(tok)

        return cur_syntax

    for tok in tokens:
        cur_syntax = handle(tok)

    if cur_syntax:
        cur_syntax.update_end(tok)


if __name__ == "__main__":
    pass

