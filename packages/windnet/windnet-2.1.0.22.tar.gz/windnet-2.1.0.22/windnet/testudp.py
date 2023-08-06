


import json
import socket
from sys import argv
from windbase import CommEngine


class udpserver(object):
    def __init__(self) -> None:
        pass
ce = CommEngine()

def post_test_receive(data,srcaddr,sock):
    try:
        msg = json.loads(data.decode())
    except:
        ce.close(sock)
    if msg and msg.get("port",0):
        port = msg["port"]
        print("current port: {} from {}\n".format(port,srcaddr))
        ce.close(sock)
        

def post_sever_receive(data,srcaddr,sock):
    msg = json.loads(data.decode())
    print( "\nreceive {} ".format(msg))
    if msg and msg.get("start",0):
        start_port = msg["start"]
        end_port = msg["end"]
        port = start_port 
        while port < end_port:
            try:
                bind_addr = ("0.0.0.0",port)
                test_sock = ce.initsock(bind_addr)
                test_msg = {"port":port}
                ce.send_now(sock,json.dumps(test_msg).encode(),srcaddr)
                ce.wait_receive(test_sock,post_test_receive)
            except:
                pass
            port += 1
    pass

def post_client_receive(data,srcaddr,sock:socket):
    msg = json.loads(data.decode())
    if msg and msg.get("port",0):
        port = msg["port"]
        print("try port: {} from {}".format(port,sock.getsockname()))
        dst_addr = (srcaddr[0],port)
        ce.send_now(sock,data,dst_addr)
    pass

def server(listen_port:int):
    # ce = CommEngine()
    bind_addr = ("0.0.0.0",listen_port)
    server_sock = ce.initsock(bind_addr)
    ce.wait_receive(server_sock,post_sever_receive)
    input("press return to quit! ")

    pass

def client(serverport:int,start:int,end:int):
    ce = CommEngine()
    bind_addr = ("0.0.0.0",50000)
    client_sock = ce.initsock(bind_addr)
    server_addr = ("43.134.27.7",serverport)
    msg = {"start":start,"end":end}
    ce.send_now(client_sock,json.dumps(msg).encode(),server_addr)
    ce.wait_receive(client_sock,post_client_receive)
    input("press return to quit! ")
    

    pass

if __name__ == "__main__":
    if len(argv)<3:
        print("help:\n testudp.py -s listenport \n testudp.py -c serverport start end")
    if len(argv)==3 and argv[1] == "-s":
        server(int(argv[2]))
    if len(argv)==5 and argv[1] == "-c":
        client(int(argv[2]),int(argv[3]),int(argv[4]))

        
