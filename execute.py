import os

serverfile = "./server.txt"
serverrun = "./run_server.txt"

server_list=[]
f = open(serverfile)
for server in f:
    server_list.append(server)

#ff = open(serverrun,"a+") 
#ff.write("begin")

def run():
    if os.path.exists("./log.txt"):
    	os.system("rm log.txt")
    if os.path.exists("./run_server.txt"):
    	os.system("rm run_server.txt")
    for server in server_list:
        with open(serverrun,"a+") as ff:
            ff.write('\n'+server)
        os.system("python my1.py")
       
run()
