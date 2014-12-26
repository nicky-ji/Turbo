import os
serverfile = "./server.txt"
server_list = []
f=open(serverfile)
for li in f:
   server_list.append(li)

serverrun= "./run_server.txt"

os.system("ps aux | grep mini | grep -v grep | cut -c 10-14 | xargs kill -9")
   
for server in server_list:
    with open(serverrun,"a+") as f:
       f.write('\n'+server)
    pro = os.popen('ps aux| grep mini| grep -v grep').read()
    if pro:
        pid = pro.split()[1]
        while pid:
            # print pid
            pro = os.popen('ps aux| grep mini| grep -v grep').read()
            if pro:
                pid = pro.split()[1]
            else:
                break

    os.system("%s"%server)
