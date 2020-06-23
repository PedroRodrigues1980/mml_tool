#!/usr/bin/python3.6
encoding='utf_8'

from tkinter import *
from tkinter import filedialog
from Lib import Dx200_RNC
from Lib import Dx200_mcRNC

class Rotas3G(Frame):
    background = 'SystemButtonFace'
    def __init__(self, mainFrame):
        self.mainFrame = Frame(mainFrame, bg=self.background)
        self.mainFrame.pack(side="top", fill="both", expand="true")
        self.RNC = Dx200_RNC.Mml_Command()
        self.mcRNC = Dx200_mcRNC.Mml_Command()
        self.dump = ""

        self.gui_frame()

    def gui_frame(self):
        # ----
        self.frame1 = Frame(self.mainFrame, bg=self.background)
        self.frame1.pack(side = "top" , fill="x", padx = (5,5), pady = (5,0))
        
        self.btn_dump = ttk.Button(self.frame1, text="Dump Rotas", command=self.show_dump)
        self.btn_dump.pack(side = "left")

        self.btn_output = ttk.Button(self.frame1, text="Delete ATM", command=self.delete_rotas_atm)
        self.btn_output.pack(side = "left", padx = (0,0))
        self.btn_output = ttk.Button(self.frame1, text="Delete IP RNC", command=self.delete_rotas_ip_rnc)
        self.btn_output.pack(side = "left", padx = (0,0))
        self.btn_output = ttk.Button(self.frame1, text="Delete IP mcRNC", command=self.delete_rotas_ip_mcrnc)
        self.btn_output.pack(side = "left", padx = (0,0))
        # ---
        self.frame2 = Frame(self.mainFrame, bg=self.background)
        self.frame2.pack(side="bottom", fill="x", padx=(5,5), pady=(5,0))

        self.btn_read = ttk.Button(self.frame2, text="Read", command=self.read)
        self.btn_read.pack(side="left", fill="x", expand="true", ipady= 5)

        self.btn_reset = ttk.Button(self.frame2, text="Reset", command=self.reset)
        self.btn_reset.pack(side="left", fill="x", expand="true", ipady=5)
        # ---
        self.outputBox = Text(self.mainFrame)
        self.outputBox.pack(side="top", fill="both", expand="true", padx=(5,5), pady=(5,0))

    def show_dump(self):
        self.outputBox.delete(1.0, END)
        self.outputBox.insert(END, self.dump)

    def read(self):
        self.dump = self.outputBox.get(1.0,END)
        if len(self.dump) <= 0:
            return
        #--- ATM
        self.zqkb = self.RNC.ZQKB(self.dump)
        self.zlci = self.RNC.ZLCI(self.dump)
        self.zqri = self.RNC.ZQRI(self.dump)
        self.zqrl = self.RNC.ZQRL(self.dump)
        self.zqrb = self.RNC.ZQRB(self.dump)
        #--- mcRnc
        self.ipbr = self.mcRNC.IPBR(self.dump)
        self.ipro = self.mcRNC.IPRO(self.dump)
        
        
    def delete_rotas_atm(self):
        self.outputBox.delete(1.0, END)
        if len(self.dump) <= 1:
            return
        for unit, dest, gate, route, pref, nbr in self.zqkb:
            self.outputBox.insert(END,"ZQKA:{};\n".format(nbr))
            self.outputBox.insert(END,"Y\n")    
        for if_name, if_ip in self.zqri:
            self.outputBox.insert(END,"ZQRG:OMU,0&&1:{};\n".format(if_name))
            self.outputBox.insert(END,"Y\n")
            self.outputBox.insert(END,"ZQMD:EXT:OMU:{};\n".format(if_name))
            self.outputBox.insert(END,"Y\n")   
        for atm, vpi,vci in self.zlci:
            self.outputBox.insert(END,"ZLCS:{},{},{}:LOCK:;\n".format(atm, vpi,vci))
            self.outputBox.insert(END,"ZLCS:{},{}:LOCK:;\n".format(atm, vpi))
            self.outputBox.insert(END,"ZLCD:{},{},{};\n".format(atm, vpi,vci))
            self.outputBox.insert(END,"ZLCD:{},{};\n".format(atm, vpi))
            
    def delete_rotas_ip_rnc(self):
        self.outputBox.delete(1.0, END)
        if len(self.dump) <= 1:
            return
        for ipbr, name, unitName, unitId, vlan, ip in self.zqrb:
            if ipbr == '':
                return
            self.outputBox.insert(END,"ZYGS:S:{},{},{}:MODE=1;\n".format(unitName, unitId, ipbr))
            self.outputBox.insert(END,"ZYGS:D:{},{},{};\n".format(unitName, unitId, ipbr))
            self.outputBox.insert(END,"ZQRA:{},{}:{}:IPV4={}:ID={};\n".format(unitName, unitId, vlan, ip, ipbr))
            self.outputBox.insert(END,"Y\n")
            self.outputBox.insert(END,"ZQRU:DEL:{},:;\n".format(ipbr))

    def delete_rotas_ip_mcrnc(self):
        self.outputBox.delete(1.0, END)
        if len(self.dump) <= 1:
            return
        for ipbr_id, addr, owner, vlan, vrf in self.ipro:
            if ipbr_id == '':
                return
            self.outputBox.insert(END,"delete networking monitoring bfd session {} name {}\n".format(owner, ipbr_id))
            self.outputBox.insert(END,"delete networking ipro owner {} iface {} ipbr-id {} ip-address {}\n".format(owner, vlan, ipbr_id, addr))
        for ipbr_id, ipbr_name, Route_bandwidth, Committed_bandwidth, Committed_DCN, Committed_signaling in self.ipbr:
            self.outputBox.insert(END,"delete networking ipbr ipbr-id {} ipbr-name {}\n".format(ipbr_id, ipbr_name))

    def reset(self):
        self.dump = ""
        self.RNC.reset()
        self.show_dump()
        
    def closeFrame(self):
        try:
            self.mainFrame.destroy()
        except Exception as e:
            print(e)
            pass
