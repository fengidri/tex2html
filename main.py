# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-06-23 14:13:15
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

from textohtml import open_source_to_words, savehtml
import codecs

import argparse
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i",    help='Input file. ft=mkiv')
    parser.add_argument("-o",    help='Output file. ft=html')
    parser.add_argument("--js",  help='JS file. ft=js')
    parser.add_argument("--css", help='CSS file. ft=css')

    parser.add_argument('-n', type=int)

    args = parser.parse_args()

    if args.i:
        ws =open_source_to_words(args.i)

    if args.n:
        logging.info( ws.getword_byindex(args.n).show() )

    if args.o:
        print '-------'
        f = codecs.open(args.o, 'w','utf8')
        if args.js:
            f.write('<script>\n')
            f.write(open(args.js).read())
            f.write('\n</script>\n')

        if args.css:
            f.write('<style>\n')
            f.write(open(args.css).read())
            f.write('\n</style>\n')

        savehtml(f, ws)
        f.close()

if __name__ == "__main__":
    main()

