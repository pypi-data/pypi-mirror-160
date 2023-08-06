#!/usr/local/bin/python38

import dns.resolver
# from dns import resolvere
import httplib2

iplist = []
appdomain = "www.google.com"

def get_iplist(domain=""):
    try:
        A = dns.resolver.resolve(domain,"A")
    except Exception as e:
        print("dns resolver error:" + str(e))
        return
    for i in A.response.answer:
        for j in i.items:
            if j.rdtype == 1:
                iplist.append(j.address)
    return True

def checkip(ip):
    checkurl = 'http://' + ip + ":80"
    getcontent = ""
    httplib2.socket.setdefaulttimeout(5)
    conn = httplib2.Http()
    resp = {}
    try:
        resp,getcontent=conn.request(checkurl)
    finally:
        if  resp.get('status',"")== "200":
            print(ip+"[OK]")
        else:
            print(ip+"[Error]")

def get_net(ip):
    ips = ip.split(".")
    return ".".join(ips[0:3])

if __name__ == "__main__":
    for i in range(500):
        get_iplist(appdomain)
    print(iplist)
    netlist = [get_net(x) for x in iplist]
    netlist = set(netlist)
    print(netlist)
    print(len(iplist),len(set(iplist)),len(netlist))
        # for ip in iplist:
            # checkip(ip)


