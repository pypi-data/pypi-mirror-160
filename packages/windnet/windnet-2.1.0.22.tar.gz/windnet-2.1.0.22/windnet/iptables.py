# /*
#  * @Author: Guofeng He 
#  * @Date: 2022-06-09 15:13:19 
#  * @Last Modified by:   Guofeng He 
#  * @Last Modified time: 2022-06-09 15:13:19 
#  */

from sys import argv
if "Linux" in platform.system():
    import iptc

def add_snat_easy(nic_name:str,src_net:str)->str:
    rule_d = {'comment':"test from misas",
    'src':src_net,
    'target':"MASQUERADE",
    'out-interface':nic_name
    }
    iptc.easy.insert_rule('nat',"POSTROUTING",rule_d)
    pass

def del_snat_easy(nic_name:str,src_net:str)->str:
    rule_d = {'comment':"test from misas",
    'src':src_net,
    'target':"MASQUERADE",
    'out-interface':nic_name
    }
    iptc.easy.delete_rule('nat',"POSTROUTING",rule_d)
    pass

def add_snat(nic_name:str,src_net:str)->str:
    rule = iptc.Rule()
    rule.target = iptc.Target(rule,"MASQUERADE")
    rule.src = src_net
    rule.out_interface = nic_name
    chain = iptc.Chain(iptc.Table(iptc.Table.NAT), "POSTROUTING")
    chain.append_rule(rule)
    pass
    
def del_snat(nic_name:str,src_net:str)->str:
    rule = iptc.Rule()
    rule.target = iptc.Target(rule,"MASQUERADE")
    rule.src = src_net
    rule.out_interface = nic_name
    chain = iptc.Chain(iptc.Table(iptc.Table.NAT), "POSTROUTING")
    chain.delete_rule(rule)
    pass

if __name__ == "__main__":
    if len(argv)==2 and argv[1]=="add":
        add_snat("eth0","192.0.6.0/24")
    if len(argv)==2 and argv[1]=="del":
        del_snat("eth0","192.0.6.0/24")

    if len(argv)==2 and argv[1]=="addeasy":
        add_snat_easy("eth0","192.0.6.0/24")
    if len(argv)==2 and argv[1]=="deleasy":
        del_snat_easy("eth0","192.0.6.0/24")

