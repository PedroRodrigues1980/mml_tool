#!/usr/bin/python3.6
encoding='utf_8'

class Mml_Command():
    def __init__(self):
        self.ZLCI_Info = []
        self.ZQMI_Info = []
        self.ZQRI_Info = []
        self.ZQKB_Info = []
        self.ZQRL_Info = []
        self.ZQRB_Info = []
        self.ZYGS_Info = []
            
    def ZLCI(self, dump):
        self.reset()
        atm = ''
        vpi = ''
        vci = ''
        zlci = False
        data_line_vc = False
        for line in dump.splitlines():
            if "ZLCI:" in line and "VC" in line:
                zlci = True
                continue
            if "-----   -----   -----   ------" in line and zlci:
                data_line_vc = True
                continue
            if data_line_vc and zlci:
                if line == '':
                    continue
                word = line.split()
                atm = word[0]
                vpi = word[1]
                vci = word[2]
                d = (atm, vpi, vci)
                self.ZLCI_Info.append(d)
                zlci = False
                data_line_vc = False
                break          
        #atm, vpi,vci
        return self.ZLCI_Info 

    def ZQRI(self, dump):
        self.reset()
        if_name = ''
        if_ip = ''
        zqri = False
        trigger_line = False
        for line in dump.splitlines():
            if "ZQRI:" in line:
                zqri = True
                continue
            if "OMU-0" in line and zqri:
                word = line.split()
                if_name = word[1]
                trigger_line = True
                continue
            if trigger_line and "->" in line and zqri:
                if line == '':
                    continue
                word = line.split()
                if_ip = word[-1]
                if_ip = if_ip.replace("->","")
                trigger_line = False
                continue
            if "COMMAND EXECUTED" in line and zqri:
                zqri = False
                d = (if_name, if_ip)
                self.ZQRI_Info.append(d)
                break
        #print(self.ZQRI_Info)
        #if_name, if_ip
        return self.ZQRI_Info
         

    def ZQRL(self, dump):
        self.reset()
        ipbr = ''
        name = ''
        route_bw = ''
        committed_bw = ''
        committed_sig = ''
        committed_dcn = ''
        ifc = ''
        ratio = ''
        zqrl = False
        trigger_line = False
        for line in dump.splitlines():
            if "ZQRL:ID=" in line:
                zqrl = True
                continue
            if " ---- ---- ---------------- --------- --------- --------- --------- ---  -----" in line and zqrl:
                trigger_line = True
                continue
            if trigger_line and zqrl:
                if line == '':
                    continue
                word = line.split()
                ipbr = word[1]
                name = word[2]
                route_bw = word[3]
                committed_bw = word[4]
                committed_sig = word[5]
                committed_dcn = word[6]
                ifc = word[7]
                ratio = word[8]
                trigger_line = False
                continue
            if "COMMAND EXECUTED" in line and zqrl:
                d = (ipbr, name, route_bw, committed_bw, committed_sig, committed_dcn, ifc, ratio)
                self.ZQRL_Info.append(d)
                break
        #print(self.ZQRL_Info)
        #ipbr, name, route_bw, committed_bw, committed_sig, committed_dcn, ifc, ratio
        return self.ZQRL_Info
                
    def ZQRB(self, dump):
        self.reset()
        ipbr = ''
        name = ''
        unitName = ''
        unitId = ''
        vlan = ''
        ip = ''
        zqrb = False
        trigger_line = False
        trigger_line2 = False
        unitName = ""
        unitId = ""
        for line in dump.splitlines():
            if "ZQRB" in line:
                zqrb = True
                continue
            if "-------- -------- -------------- ---- ---------------- ---- -------------------" in line and zqrb:
                trigger_line = True
                continue
            if "NPGE" in line and zqrb:
                word = line.split()
                unit = word[0]
                vlan = word[1]
                ip = word[2]
                unit = unit.replace("-"," ")
                for c_pos in range(0,len(unit)):
                    if unit[c_pos] == " ":
                        break
                    else:
                        unitName += unit[c_pos]
                unitId = unit[c_pos+1:]
                trigger_line = False
                trigger_line2 = True
                continue
            if trigger_line2 and zqrb:
                if line == '':
                    continue
                word = line.split()
                name = word[1]
                ipbr = word[2]
                break
        d = (ipbr, name, unitName, unitId, vlan, ip)
        self.ZQRB_Info.append(d)
        #print(self.ZQRB_Info)
        #ipbr, name, unitName, unitId, vlan, ip
        return self.ZQRB_Info                
        
        
    def ZQKB(self, dump):
        self.reset()
        unit = ''
        dest = ''
        gate = ''
        route = ''
        pref = ''
        nbr = ''
        zqkb = False
        trigger_line = False
        for line in dump.splitlines():
            if "ZQKB::" in line:
                zqkb = True
                continue
            if "OMU" in line and zqkb:
                word = line.split()
                unit = word[0]
                dest = word[1]
                gate = word[2]
                route = word[3]
                pref = word[4]
                nbr = word[5]
                d = (unit, dest, gate, route, pref, nbr)
                self.ZQKB_Info.append(d)
                break
        
        #unit, dest, gate, route, pref, nbr
        return self.ZQKB_Info


    def reset(self):
        self.ZLCI_Info = []
        self.ZQMI_Info = []
        self.ZQRI_Info = []
        self.ZQKB_Info = []
        self.ZQRL_Info = []
        self.ZQRB_Info = []
        self.ZYGS_Info = []        

















    
