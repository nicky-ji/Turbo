import os
import threading

serverrun= "./run_server.txt"
fi = open(serverrun).readlines()
server = fi[-1]

def start(servername):
    os.system("cd /home/oupengtest")
    os.system("%s"%servername)

def kill():
    os.system("python tbspd.py")
    pro = os.popen('ps aux| grep mini| grep -v grep').read()
    if pro:
        pid = pro.split()[1]
        os.system("kill -9 %s"%pid)
    else:
        pass

def main():
    process1 = threading.Thread(target=start,args=(server,))
    process2 = threading.Thread(target=kill,args=())
    #s = Start("proxy=http://uf05-02.opera-mini.net ./mini_proxy")
    #k = Kill()
    process1.start()
    process2.start()

main()

