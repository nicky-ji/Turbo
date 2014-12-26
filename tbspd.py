#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import urllib2
import time
import json

turbo_local_proxy = "http://10.96.0.194:9090"
default_target_url = "http://121.42.51.106/pic/flower.jpg"

Logs = []

serverfile = "./run_server.txt"
f =  open(serverfile).readlines()
server = f[-1]
servername = f[-1].split(".")[0][13:]
Logdir = './results/'+servername
LogTime =time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))
LogFile = Logdir+'/'+LogTime+'tbresult.txt'
#LogFile = './results/results/tbresult.txt'
LogInfo = Logdir+'/'+LogTime+'tbjson.txt'

FinalLog = "./log.txt"
#log = open(FinalLog,"a+")

if not os.path.isdir(Logdir):
    os.makedirs(Logdir)

UrlFile = './url.txt'
url_list = []

log_list = []

test_date = time.strftime('%Y%m%d-%H:%M:%S',time.localtime(time.time()))

def loadTestUrl():
    file_object = open(UrlFile)
    try:
        for line in file_object:
            if line.find('http://') == -1:
                print "invalid url or unnecesary blank lines in url.txt"
                sys.exit()
            url = line.split()
            url_list.append(url)
    finally:
        file_object.close()

def log(*args):
    Logs.append(' '.join([str(a) for a in args]))

def writeDate():
    with open(LogFile, 'w') as f:
        f.write(test_date + '\n')

def writeLog():
    with open(LogFile,'a+') as f:
        f.write('\n'.join(Logs))

def writeLogInfo():
    with open(LogInfo,'w') as f:
        f.write(test_date + '\n')
        f.write(json.dumps(log_list))

def printResult():
    print open(LogFile,'r').read()

def createLogData(profile_list):
    item = {}

    if len(profile_list) != 2:
        print 'error occurs when save data log'
        sys.exit()

    item['url'] = profile_list[0].url
    for p in profile_list:
        data = {}
        data['dx'] = int(p.dx*1000)
        data['avg'] = p.avg
        data['realavg'] = p.realavg
        data['size'] = p.sizes
        #datas = ",".join(format(int(x*1000), '5d') for x in p.datas)
        #data['datas'] = p.datas
        data['datas'] = map(lambda x: int(x*1000), p.datas)

        if p.name == 'direct':
            item['direct'] = data
        elif p.name == 'turbo':
            item['turbo'] = data
        else:
            print 'error occurs when save data log'
            sys.exit()
    print item
    log_list.append(item)

class Profiler:
    TimeoutUrls = {}

    def __init__(self, name, url):
        if name:
            self.name = name
        else:
            self.name = 'direct'
        if len(self.name) > 15:
            self.name = self.name[:15]
        self.url = url
        self.datas = []
        self.dx = 0.0
        self.avg = 0.0
        self.realavg = 0.0
        self.resources = []
        self.sizes = (0,0)

    def addSize(self, sizes):
        #self.sizes = map(lambda x,y: x+y, self.sizes, sizes)
        self.sizes = sizes

    def addData(self, d):
        self.datas.append(d)

    def caculate(self):
        if not self.datas:
            return
        l = self.datas
        ex = (sum(l) / len(l))

        self.dx = sum(map(lambda x: (x-ex)**2, l)) / len(l)
        s = 2 * (self.dx ** 0.5)
        #print 'before ', map(lambda x: int(x*1000), l)
        self.realavg = int((sum(l) / len(l)) * 1000)
        newl = filter(lambda x: abs(x-ex) < s, l)
        if not newl:
            newl = l
        #print 'after ', map(lambda x: int(x*1000), newl)
        self.avg = int((sum(newl) / len(newl)) * 1000)

    def logResult(self):
        if 0 in self.datas:
            print 'some thing wrong clear data'
            for i in xrange(len(self.datas)):
                self.datas[i] = 0

        if not self.avg:
            self.caculate()
        datas = ",".join(format(int(x*1000), '5d') for x in self.datas)
        log("%s %-20s dx=%-5d avg=%-5d realavg=%-5d size=%-5s times=%s" %
            (self.name, self.url, int(self.dx*1000), self.avg, self.realavg, self.sizes, datas))

    def addRescources(self, url, status ,cntype, time):
        self.resources.append((status, cntype, time, url))

    def logResources(self):
        for r in self.resources:
            log(*r)


def loadUrl(url, profiler, enable_proxy = False):
    loadtime = 0
    try:
        begin = time.time()
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'tbtest_tools')
        req.add_header('Accept-Encoding', 'gzip,deflate,sdch')
        req.add_header('Accept', '*/*')
        req.add_header('Cache-Control', 'no-cache')
        if enable_proxy:
            print 'use turbo!!!'
            proxy_handler = urllib2.ProxyHandler({'http': turbo_local_proxy})
            opener =  urllib2.build_opener(proxy_handler)
        else:
            opener =  urllib2.build_opener()
        resp = opener.open(req, timeout = 20)
        cntype = resp.headers.getheader('content-type')
        print 'content-type', cntype
        print 'status code', resp.getcode()
        #print 'headers', resp.headers
        size = len(resp.read())
        loadtime = time.time() - begin
        print 'page size', size
        #loadtime = int((time.time() - begin) * 1000)
        print 'loadtime is ', loadtime
        profiler.addSize(size)
        profiler.addRescources(url, resp.getcode() ,cntype, int(loadtime * 1000))
        return loadtime
    except urllib2.HTTPError, e:
        print 'fail to get page : httpcode=', e.code, e.read()
        return 0
    finally:
        opener.close()

def proceedSingleTest(url, loadtimes):
    print "start load url=", url, 'times=', loadtimes
    ltime = 0
    profiler_list = []
    profiler_list.append(Profiler('direct', url))
    profiler_list.append(Profiler('turbo', url))
    print '*' * 80
    for i in xrange(loadtimes):
        ltime = loadUrl(url, profiler_list[0], False)
        profiler_list[0].addData(ltime)
        print '*' * 80
    for i in xrange(loadtimes):
        ltime = loadUrl(url, profiler_list[1], True)
        profiler_list[1].addData(ltime)
        print '*' * 80
    for p in profiler_list:
        p.logResult()
    createLogData(profiler_list)

def showHelp():
    print """
    python tbspd.py url times
    example :
        python tbspd.py http://www.baidu.com 5
        python tbspd.py http://www.baidu.com
    """

def proceedAll():
    writeDate()
    for item in url_list:
        proceedSingleTest(item[0], int(item[1]))

def main(argv):
    loadTestUrl()
    if len(url_list) > 0:
        proceedAll()
    else:
        print 'no url file'
        url = default_target_url
        if len(argv) > 1:
            url = argv[1]
        if not url or url.find('http://') == -1:
            print url, "is not a valid url"
            showHelp()
            return

        loadtimes = 5
        if len(argv) > 2:
            try:
                loadtimes = int(argv[2])
            except Exception, e:
                print "second argument should be a nummber."
                showHelp()
                return
        proceedSingleTest(url, loadtimes)
    printResult()
    writeLog()
    writeLogInfo()

def ResultCheck():
    flog = open(FinalLog,"a+")
    if os.path.exists(LogFile) and os.path.exists(LogInfo):
        json = open(LogFile).readlines()
        result = open(LogInfo).readlines()
        if len(json)<=1 or len(result)<=1:
            flog.write(server + " run fail!\n")
        else:
            flog.write(server + " run pass!\n")
    else:
        flog.write(server + " run fail!\n" )

if __name__ == '__main__':
    try:
	main(sys.argv)
    except Exception,e:
        print "execute error:",e
        #pass
    finally:
    	ResultCheck()
