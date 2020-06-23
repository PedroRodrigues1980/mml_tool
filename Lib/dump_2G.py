from tkinter import *
#from tkinter import ttk
#from tkinter import filedialog
import datetime
from Lib import Dx200_BSC

   
class Dump_2G(Frame):
    date = datetime.datetime.now()
    background = 'SystemButtonFace'
    dump = ''
    bcf = ''
    bts = []
    pcm = []
    dap = []
    csdap = []
    hnbr = []
    
    def __init__(self, mainFrame):
        Frame.__init__(self, mainFrame)
        self.mainFrame = mainFrame
        
        self.gui_frame()

    def gui_frame(self):
        self.frame1 = Frame(self.mainFrame)
        self.frame1.pack(side = "top" , fill=X, padx = (5,5), pady = (5,0))
        self.frame1.configure(background = self.background)
        
        self.btn_inputs = ttk.Button(self.frame1, style='B.TButton', text="Inputs", command = self.show_dump)
        self.btn_inputs.pack(side = "left", ipadx=5)
   
        self.btn_atm = ttk.Button(self.frame1, text="ATM")
        self.btn_atm.bind("<ButtonRelease-1>", self.atmScript)
        self.btn_atm.pack(side = "left", ipadx=5)
        
        self.btn_abis_eth = ttk.Button(self.frame1, text="ABIS Over ETH")
        self.btn_abis_eth.bind("<ButtonRelease-1>", self.abisOverEthScript)
        self.btn_abis_eth.pack(side = "left", ipadx=5)
        
        self.btn_abis_tdm = ttk.Button(self.frame1, text="ABIS Over TDM")
        self.btn_abis_tdm.bind("<ButtonRelease-1>", self.abisOverTdmScript)
        self.btn_abis_tdm.pack(side = "left", ipadx=5)
        # ---
        self.frame3 = Frame(self.mainFrame)
        self.frame3.pack(side = "bottom", fill = "x", padx = (5,5), pady = (5,0))       
        self.frame3.configure(background = self.background)
        
        self.btn_read = ttk.Button(self.frame3, text="Read Inputs")
        self.btn_read.bind("<ButtonRelease-1>", self.readInputs)
        self.btn_read.pack(side = "left", fill="x", expand="true", anchor="e", ipady=5)
        self.btn_read.config(state="enable")
        
        self.btn_reset = ttk.Button(self.frame3, text="Reset")
        self.btn_reset.bind("<ButtonRelease-1>", self.clearVar)
        self.btn_reset.pack(side = "left", fill="x", expand="true", ipady=5)
        self.btn_reset.config(state="enable")
        # ---  
        self.frame2 = Frame(self.mainFrame)
        self.frame2.pack(side = "top", fill = "both", expand=True, padx = (5,5), pady = (0,0))
        
        self.frame2.configure(background = self.background)
        yscrollbar = ttk.Scrollbar(self.frame2)
        yscrollbar.pack(side=RIGHT, fill=Y)
        self.textBox = Text(self.frame2, wrap=NONE, yscrollcommand=yscrollbar.set)
        self.textBox.pack(side = "top", fill="both", expand=True)
        yscrollbar.config(command=self.textBox.yview)        


    def show_dump(self):
        self.textBox.delete(1.0, END)
        self.textBox.insert(END, self.dump)
        self.btn_read.config(state="enable")
        self.btn_read.bind("<ButtonRelease-1>", self.readInputs)
        self.btn_reset.config(state="enable")
        self.btn_reset.bind("<ButtonRelease-1>", self.clearVar)
    
    def clearVar(self, event):
        self.textBox.delete(1.0,END)
        self.dump = ''
        self.bcf = ''
        self.bts = []
        self.pcm = []
        self.dap = []
        self.csdap = []
        self.hnbr = []
        return()
    
    def closeFrame(self):
        try:
            self.mainFrame.destroy()
        except Exception:
            pass
        return

#--------------------------------------------------------------------------------------------------------------------------------------
#       Read INPUTS
#--------------------------------------------------------------------------------------------------------------------------------------    
    def readInputs(self, event):
        self.dump = self.textBox.get("1.0",END)
        read = Dx200_BSC.Mml_Command()
        zeei = read.ZEEI(self.dump)
        for bscType, bcfModel, bscName, omuName, omuId, bcfType, bcfId, bcf_sig, lac, ci, btsId, btsName, trxName, trxID, trx_freq, trx_pcm, trx_channel, trx_pref, trx_sig in zeei:
            self.bcf = bcfId
            if btsId not in self.bts:
                self.bts.append(btsId)
            if trx_pcm not in self.pcm:
                self.pcm.append(trx_pcm)
        for pcm in self.pcm:
            dap = read.ZESI(self.dump, pcm)
            if dap not in self.dap and not dap == "None":
                self.dap.append(dap)
        for pcm in self.pcm:
            csdap = read.ZESB(self.dump, pcm)
            if csdap not in self.csdap and not csdap == "None":
                self.csdap.append(csdap) 
        return()

#--------------------------------------------------------------------------------------------------------------------------------------
#       Create Scripts
#--------------------------------------------------------------------------------------------------------------------------------------
    def atmScript(self, event):
        self.textBox.delete(1.0, END)
        self.btn_read.config(state="disable")
        self.btn_read.unbind("<ButtonRelease-1>")
        self.btn_reset.config(state="disable")
        self.btn_reset.unbind("<ButtonRelease-1>")
        if(self.bcf==''):
            return()
        self.textBox.insert(END,"ZEEI:BCF={};\n".format(self.bcf))
        self.textBox.insert(END,"ZEEI:BCF={}:RCV;\n".format(self.bcf))
        self.textBox.insert(END,"ZEEL:BL:BCF={};\n".format(self.bcf))
        self.textBox.insert(END,"ZEOL:{};\n".format(self.bcf))
        self.textBox.insert(END,"ZEOH:{}-{}-{}:BCF={};\n".format(self.date.year, self.date.month, self.date.day, self.bcf))
        self.textBox.insert(END,"ZEFO:{}:ALL;\n".format(self.bcf))
        self.textBox.insert(END,"ZEFO:{}:IOP;\n".format(self.bcf))
        self.textBox.insert(END,"ZERO:BCF={};\n".format(self.bcf))
        self.textBox.insert(END,"ZQWL:BCF={};\n".format(self.bcf))
        self.textBox.insert(END,"ZEWO:{};\n".format(self.bcf))
        self.textBox.insert(END,"ZAHO:;\n".format(self.bcf))
        for bts in self.bts:
            self.textBox.insert(END,"ZEAO:BTS={};\n".format(bts))
            self.textBox.insert(END,"ZECP:BTS={}:LONG;\n".format(bts))
            self.textBox.insert(END,"ZEAV:BTS={};\n".format(bts))
            self.textBox.insert(END,"ZEAI:BTS={};\n".format(bts))
            self.textBox.insert(END,"ZEAP:BTS={};\n".format(bts))
            self.textBox.insert(END,"ZEQO:BTS={}:ALL;\n".format(bts))
            self.textBox.insert(END,"ZEUO:BTS={};\n".format(bts))
            self.textBox.insert(END,"ZEHO:BTS={};\n".format(bts))
            self.textBox.insert(END,"ZERO:BTS={};\n".format(bts))
        for pcm in self.pcm:
            self.textBox.insert(END,"ZDTI:::PCM={};\n".format(pcm))
            self.textBox.insert(END,"ZDSB:::PCM={};\n".format(pcm))
            self.textBox.insert(END,"ZYEF:ET,{};\n".format(pcm))
            self.textBox.insert(END,"ZAEF:ET,{};\n".format(pcm))
            self.textBox.insert(END,"ZYMO:ET,{};\n".format(pcm))
        for dap in self.dap:
            if dap == None:
                continue
            self.textBox.insert(END,"ZESI:ID={}:TRXS;\n".format(dap))
            self.textBox.insert(END,"ZESI:ID={};\n".format(dap))
        for csdap in self.csdap:
            if csdap == None:
                continue
            self.textBox.insert(END,"ZESB:CID={};\n".format(csdap))
        return()

    def abisOverEthScript(self, event):
        self.textBox.delete(1.0, END)
        self.btn_read.config(state="disable")
        self.btn_read.unbind("<ButtonRelease-1>")
        self.btn_reset.config(state="disable")
        self.btn_reset.unbind("<ButtonRelease-1>")
        if(self.bcf==''):
            return()
        self.textBox.insert(END,"ZEEI:BCF={};\n".format(self.bcf))
        self.textBox.insert(END,"ZEEI:BCF={}:RCV;\n".format(self.bcf))
        self.textBox.insert(END,"ZEEL:BL:BCF={};\n".format(self.bcf))
        self.textBox.insert(END,"ZEOL:{};\n".format(self.bcf))
        self.textBox.insert(END,"ZEOH:{}-{}-{}:BCF={};\n".format(self.date.year, self.date.month, self.date.day, self.bcf))
        self.textBox.insert(END,"ZEFO:{}:ALL;\n".format(self.bcf))
        self.textBox.insert(END,"ZEFO:{}:IOP;\n".format(self.bcf))
        self.textBox.insert(END,"ZERO:BCF={};\n".format(self.bcf))
        for bts in self.bts:
            self.textBox.insert(END,"ZEAO:BTS={};\n".format(bts))
            self.textBox.insert(END,"ZECP:BTS={}:LONG;\n".format(bts))
            self.textBox.insert(END,"ZEAV:BTS={};\n".format(bts))
            self.textBox.insert(END,"ZEAI:BTS={};\n".format(bts))
            self.textBox.insert(END,"ZEAP:BTS={};\n".format(bts))
            self.textBox.insert(END,"ZEQO:BTS={}:ALL;\n".format(bts))
            self.textBox.insert(END,"ZEUO:BTS={};\n".format(bts))
            self.textBox.insert(END,"ZEHO:BTS={};\n".format(bts))
            self.textBox.insert(END,"ZERO:BTS={};\n".format(bts))
        self.textBox.insert(END,"ZOYV:IUA::;\n")
        self.textBox.insert(END,"ZOYV:IUA::A;\n")
        self.textBox.insert(END,"ZDWQ;\n")
        return()
    
    def abisOverTdmScript(self, event):
        self.textBox.delete(1.0, END)
        self.btn_read.config(state="disable")
        self.btn_read.unbind("<ButtonRelease-1>")
        self.btn_reset.config(state="disable")
        self.btn_reset.unbind("<ButtonRelease-1>")
        if(self.bcf==''):
            return()
        self.textBox.insert(END,"ZEEI:BCF={};\n".format(self.bcf))
        self.textBox.insert(END,"ZEEI:BCF={}:RCV;\n".format(self.bcf))
        self.textBox.insert(END,"ZEEL:BL:BCF={};\n".format(self.bcf))
        self.textBox.insert(END,"ZEOL:{};\n".format(self.bcf))
        self.textBox.insert(END,"ZEOH:{}-{}-{}:BCF={};\n".format(self.date.year, self.date.month, self.date.day, self.bcf))
        self.textBox.insert(END,"ZEFO:{}:ALL;\n".format(self.bcf))
        self.textBox.insert(END,"ZEFO:{}:IOP;\n".format(self.bcf))
        self.textBox.insert(END,"ZERO:BCF={};\n".format(self.bcf))
        for bts in self.bts:
            self.textBox.insert(END,"ZEAO:BTS={};\n".format(bts))
            self.textBox.insert(END,"ZECP:BTS={}:LONG;\n".format(bts))
            self.textBox.insert(END,"ZEAV:BTS={};\n".format(bts))
            self.textBox.insert(END,"ZEAI:BTS={};\n".format(bts))
            self.textBox.insert(END,"ZEAP:BTS={};\n".format(bts))
            self.textBox.insert(END,"ZEQO:BTS={}:ALL;\n".format(bts))
            self.textBox.insert(END,"ZEUO:BTS={};\n".format(bts))
            self.textBox.insert(END,"ZEHO:BTS={};\n".format(bts))
            self.textBox.insert(END,"ZERO:BTS={};\n".format(bts))
        for hnbr in self.hnbr:    
            self.textBox.insert(END,"ZESL:{};\n".format(hnbr))
        self.textBox.insert(END,"ZOYV:IUA::;\n")
        self.textBox.insert(END,"ZDWQ;\n")    
        return()

















    
