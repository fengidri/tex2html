# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-06-23 14:13:15
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

from textohtml import open_source_to_words, savehtml
import codecs


import argparse

import os
import pyinotify
Config = None

class OnWriteHandler(pyinotify.ProcessEvent):
    def process_IN_MODIFY(self, event):
        path = os.path.join(event.path,event.name)
        if path != Config.i:
            return
        try:
            print "build: %s" % Config.i
            handle()
        except:
            pass

def inotify():
    path = os.path.dirname(Config.i)

    wm = pyinotify.WatchManager()
    mask = pyinotify.IN_MODIFY #监测类型，如果多种用|分开，pyinotify.IN_CREATE | pyinotify.IN_DELETE
    wm.add_watch(path, mask, rec=True, auto_add=True)

    notifier = pyinotify.Notifier(wm, OnWriteHandler())
    print 'Start monitoring :%s (type c^c to exit)' % path
    while True:
        try:
            notifier.process_events()
            if notifier.check_events():
                notifier.read_events()
        except KeyboardInterrupt:
            notifier.stop()
            break

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i",    help='Input file. ft=mkiv')
    parser.add_argument("-o",    help='Output file. ft=html')
    parser.add_argument("--js",  help='JS file. ft=js')
    parser.add_argument("--css", help='CSS file. ft=css')

    parser.add_argument('-n', type=int)
    parser.add_argument('--inotify', type=bool, default=False)
    global Config
    Config = parser.parse_args()

    if Config.i:
        Config.i = os.path.realpath(Config.i)
    if not Config.inotify:
        handle()
    else:
        inotify()

def handle():
    if Config.i:
        ws =open_source_to_words(Config.i)

    if Config.n:
        logging.info( ws.getword_byindex(Config.n).show() )

    if Config.o:
        print '-------'
        f = codecs.open(Config.o, 'w','utf8')
        if Config.js:
            f.write('<script>\n')
            f.write(open(Config.js).read())
            f.write('\n</script>\n')

        if Config.css:
            f.write('<style>\n')
            f.write(open(Config.css).read())
            f.write('\n</style>\n')

        savehtml(f, ws)
        f.close()

if __name__ == "__main__":
    main()

