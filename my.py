import os
import threading
con=threading.Condition()

class Start(threading.Thread):
    def __init__(self,servername):
        threading.Thread.__init__(self)
        self.server = servername
    
    def run(self):
        global is_started
        con.acquire()
        if is_started is False:
            print self.server
            os.system("%s"%self.server)
	    is_started = True
            #con.notify()
        else:
	    pass
            #con.notify()
        con.release()
    
class Kill(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    
    def run(self):
        global is_started
        #con.acquire()
	print "status: "+is_started
        if is_started:
            os.system("python tbspd.py")
            pro = os.popen('ps aux| grep mini| grep -v grep').read()
            pid = pro.split()[1]
            os.system("kill -9 %s"%pid)
            is_started = False
        else:
	    pass
            #con.notify()
        #con.release()

if __name__ == '__main__':
    is_started = False
    s = Start("proxy=http://uf05-02.opera-mini.net ./mini_proxy")
    k = Kill()
    s.start()
    k.start()
    #s.join()
    #k.join()
