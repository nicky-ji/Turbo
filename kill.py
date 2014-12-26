import os
import time
serverfile = "./server.txt"
#runserver = "./run_server.txt"
server_list=[]
f = open(serverfile)
for li in f:
    server_list.append(li)

#fi = open(runserver).readlines()
#servername = fi[-1].split(".")[0][13:]
 
print len(server_list)
i=0

while i<len(server_list):
    pro = os.popen('ps aux| grep mini| grep -v grep').read()
    while pro:
        i+=1
        os.system("python tbspd.py")
        #os.chdir("./results")
	#servername = fi[-1].split(".")[0][13:]
        #print "servername: "+servername
        #os.renames("./results","./"+servername)
        #os.chdir("/home/oupengtest")
        pid = pro.split()[1]
        os.system("kill -9 %s"%pid)
        time.sleep(30)
        pro = os.popen('ps aux| grep mini| grep -v grep').read()
