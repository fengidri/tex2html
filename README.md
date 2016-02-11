# tex2html
paser the tex file. Can convert the file to html or markdown.


解析分成两个阶段: 分词与样式输出两个阶段.

分词的过程可以通过一些命令进行控制. 这些命令可能在一些宏里面, 所以这个时候
就要对宏进行展开. 但是宏的展开是就涉及到了宏的参数的问题.


宏的参数有两种如下, # 后面的数字表示参数的数量. 每一个 token 视为一个整个.
一个 group 在上一级中也是视为一个 token.

\defregex 定义的宏, 的参数列表通过 python 的 regex 提取.

\def\marco#2{....}
\defregex\marco##{}




# 样式输出
目前并不支持输出成 pdf 之类的格式, 主要是输出成 html 的格式. HTML 可以输出成优秀
的 PDF.

同时也支持输出成 markdown.


# slide
```
chapter{chapter name}
     section {section name}
     section {section name}
     section {section name}
     section {section name}
     section {section name}

chapter{chapter name}
     section {section name}
     section {section name}
     section {section name}
     section {section name}
     section {section name}
```

