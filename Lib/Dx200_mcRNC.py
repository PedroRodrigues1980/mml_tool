#!/usr/bin/python3.6
encoding='utf_8'

class Mml_Command():
    def __init__(self):
        self.ipbr_Info = []
        self.ipro_Info = []
        self.bfd_Info = []
            
    def IPBR(self, dump):
        self.reset()
        ipbr_id = ''
        ipbr_name = ''
        Route_bandwidth = ''
        Committed_bandwidth = ''
        Committed_DCN = ''
        Committed_signaling = ''
        ipbr = False
        for line in dump.splitlines():
            if "show networking ipbr ipbr-id" in line:
                ipbr = True
                continue
            if "IPBR ID" in line and ipbr:
                word = line.split()
                ipbr_id = word[3]
                continue
            if "IPBR name" in line and ipbr:
                word = line.split()
                ipbr_name = word[3]
                continue
            if "Route bandwidth" in line and ipbr:
                word = line.split()
                Route_bandwidth = word[3]
                continue
            if "Committed bandwidth" in line and ipbr:
                word = line.split()
                Committed_bandwidth  = word[3]
                continue
            if "Committed DCN" in line and ipbr:
                word = line.split()
                Committed_DCN  = word[4]
                continue
            if "Committed signaling" in line and ipbr:
                word = line.split()
                Committed_signaling  = word[4]
                d = (ipbr_id, ipbr_name, Route_bandwidth, Committed_bandwidth, Committed_DCN, Committed_signaling)
                self.ipbr_Info.append(d)
                break
        print(self.ipbr_Info)
        #ipbr_id, ipbr_name, Route_bandwidth, Committed_bandwidth, Committed_DCN, Committed_signaling
        return self.ipbr_Info 

    def IPRO(self, dump):
        ipro = False
        trigger_line = False
        for line in dump.splitlines():
            if "show networking ipro ipbr" in line:
                ipro = True
                continue
            if "---- --------------- --------------- --------------- ------------------ ---------------" in line and ipro:
                trigger_line = True
                continue
            if ipro and trigger_line:
                word = line.split()
                ipbr_id = word[0]
                addr = word[1]
                owner = word[2]
                vlan = word[3]
                vrf = word[5]
                d = (ipbr_id, addr, owner, vlan, vrf)
                self.ipro_Info.append(d)
                break
        print(self.ipro_Info)
        #ipbr_id, addr, owner, vlan, vrf
        return self.ipro_Info
    
    def reset(self):
        self.ipbr_Info = []
        self.ipro_Info = []
        self.bfd_Info = [] 
















            
