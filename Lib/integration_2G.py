from tkinter import *
#from tkinter import ttk
#from tkinter import filedialog
from Lib import Dx200_BSC

class Integration_2G(Frame):
    background = 'SystemButtonFace'
    dump = ''
    bcf_info = None
    bscType = None
    omuName = None
    omuID = str()
    bcf = None
    lapd = []
    dap = []
    csdap = []       
    bts = []
    trx = []       # tupla com BTS, TRX NAME, TRX ID
    pcm = []
    sctp = []      # SCTP ASSOCIATION NAME, ASSOC IND, UNIT, SCTP USER, ROLE, PARAMETER SET NAME, STATE
    dChannel = []  # NAME, NUM, INTERF ID, SAPI, TEI, ASSOCIATION NAME, STREAM NUMBER, HOST UNIT, STATE
        
    def __init__(self, mainFrame):
        Frame.__init__(self, mainFrame)
        self.mainFrame = mainFrame

        self.createPages()                       
        self.inputView()

    def inputView(self, event=None):
        self.closePages()
        self.createPages()        
        self.inputPage.pack(side="top", fill="both", expand=True)
        self.inputPage.config(background = self.background)
        
        self.frame1_1 = Frame(self.inputPage)
        self.frame1_1.pack(side = "top" , fill="x", padx = (5,5), pady = (5,0))
        self.frame1_1.configure(background = self.background)

        self.btn_inputs = ttk.Button(self.frame1_1, text="Inputs", command = self.show_dump)
        self.btn_inputs.pack(side = "left", ipadx=5)
        self.btn_lockUnlock = ttk.Button(self.frame1_1, text="Lock & Unlock")
        self.btn_lockUnlock.bind("<ButtonRelease-1>", self.lockUnlockView)
        self.btn_lockUnlock.pack(side = "left", ipadx=5)
        self.btn_sctp = ttk.Button(self.frame1_1, text="SCTP")
        self.btn_sctp.bind("<ButtonRelease-1>", self.sctpView )
        self.btn_sctp.pack(side = "left", ipadx=5)
        self.btn_delete = ttk.Button(self.frame1_1, text="Delete")
        self.btn_delete.bind("<ButtonRelease-1>", self.deleteView)
        self.btn_delete.pack(side = "left", ipadx=5)
        self.btn_cleanUp = ttk.Button(self.frame1_1, text="Clean UP")
        self.btn_cleanUp.bind("<ButtonRelease-1>", self.cleanUpView)
        self.btn_cleanUp.pack(side = "left", ipadx=5)
        self.bscLabel = Label(self.frame1_1, text="BSC TYPE: ", anchor=W, bg=self.background, fg="blue")
        self.bscLabel.pack(side = "left",  fill="both", expand=True, padx = (5,0))
        self.bscLabel.config(text="BSC TYPE: {}".format(self.bscType))
        # ---
        self.frame1_3 = Frame(self.inputPage)
        self.frame1_3.pack(side="bottom", fill="x", padx=(5,5), pady=(5,0))
        self.frame1_3.configure(background = self.background)
        
        self.btn_read = ttk.Button(self.frame1_3, text="Read Inputs")
        self.btn_read.bind("<ButtonRelease-1>", self.readInputs)
        self.btn_read.pack(side="left", fill="x", expand=True, anchor=W, ipady=5)
        
        self.btn_reset = ttk.Button(self.frame1_3, text="Reset")
        self.btn_reset.bind("<ButtonRelease-1>", self.clearVar)
        self.btn_reset.pack(side="left", fill="x", expand=True, anchor=W, ipady=5)
        # ---
        self.frame1_2 = Frame(self.inputPage)
        self.frame1_2.pack(side = "top", fill = "both", expand=True, padx = (5,5))
        self.frame1_2.configure(background = self.background)
        yscrollbar = ttk.Scrollbar(self.frame1_2)
        yscrollbar.pack(side=RIGHT, fill=Y)
        self.textBox = Text(self.frame1_2, wrap=NONE, yscrollcommand=yscrollbar.set)
        self.textBox.pack(side = "top", fill="both", expand=True)
        yscrollbar.config(command=self.textBox.yview)       
        # ---
        self.show_dump()
        
    def show_dump(self):
        self.textBox.delete(1.0, END)
        self.textBox.insert(END, self.dump)
        
    def clearVar(self, event):
        self.textBox.delete(1.0,END)
        self.dump = ''
        self.bscType = None
        self.bcf = None
        self.bts = []
        self.omuName = None
        self.omuID = None
        self.trx = []
        self.pcm = []
        self.lapd = []
        self.dap = []
        self.csdap = []
        self.sctp = []

    def createPages(self):
        self.inputPage = Frame(self.mainFrame)
        self.lockUnlockPage = Frame(self.mainFrame)
        self.sctpPage = Frame(self.mainFrame)
        self.sctpUpdatePage = Frame(self.mainFrame)
        self.deletePage = Frame(self.mainFrame)
        self.cleanUpPage = Frame(self.mainFrame)
        
    def closePages(self):
        self.inputPage.destroy()
        self.lockUnlockPage.destroy()
        self.sctpPage.destroy()
        self.sctpUpdatePage.destroy()
        self.deletePage.destroy()
        self.cleanUpPage.destroy()
        
    def closeFrame(self):
        try:
            self.mainFrame.destroy()
        except Exception:
            pass

        
#--------------------------------------------------------------------------------------------------------------------------------------
#       Views
#--------------------------------------------------------------------------------------------------------------------------------------  
    def lockUnlockView(self, event):
        self.closePages()
        self.createPages()      
        self.lockUnlockPage.pack(side="top", fill="both", expand=True)
        self.lockUnlockPage.config(background = self.background)
        # ---
        frame1_1 = Frame(self.lockUnlockPage)
        frame1_1.pack(side = "top" , fill=X, padx = (5,5), pady = (5,0))
        frame1_1.configure(background = self.background)
                    
        Button1 = ttk.Button(frame1_1, text="Inputs")
        Button1.bind("<ButtonRelease-1>", self.inputView)
        Button1.pack(side = "left", ipadx=5)
        
        Button2 = ttk.Button(frame1_1, text="Lock & Unlock")
        Button2.bind("<ButtonRelease-1>", )
        Button2.pack(side = "left", ipadx=5)
        
        Button3 = ttk.Button(frame1_1, text="SCTP")
        Button3.bind("<ButtonRelease-1>", self.sctpView)
        Button3.pack(side = "left", ipadx=5)
        
        Button4 = ttk.Button(frame1_1, text="Delete")
        Button4.bind("<ButtonRelease-1>", self.deleteView)
        Button4.pack(side = "left", ipadx=5)
        
        Button5 = ttk.Button(frame1_1, text="Clean UP")
        Button5.bind("<ButtonRelease-1>", self.cleanUpView)
        Button5.pack(side = "left", ipadx=5)
        
        bscLabel = Label(frame1_1, text="BSC TYPE: ", anchor=W, bg=self.background, fg="blue")
        bscLabel.pack(side = "left",  fill="both", expand=True, padx = (5,0))
        bscLabel.config(text="BSC TYPE: {}".format(self.bscType))
        # ---        
        frame1_2 = Frame(self.lockUnlockPage)
        frame1_2.pack(side = "top", fill=X, padx = (5,5))
        frame1_2.configure(background = self.background)
        
        frame1_2_1 = Frame(frame1_2)
        frame1_2_1 = LabelFrame(frame1_2)
        frame1_2_1.pack(side = "left", fill=X)
        frame1_2_1.configure(bg = self.background)
        
        var = IntVar(self.mainFrame)
        var.set(1)
        labels = [("LOCK"  , 1),
                  ("UNLOCK", 2)]
        for (label, value) in labels:
            checkbutton = Checkbutton(frame1_2_1, text=label, variable=var, onvalue = value, command = lambda: self.lockUnlockScript(var, var1, outputBox))
            checkbutton.pack( side = "left", anchor=CENTER, fill = X)
            checkbutton.configure(state=NORMAL)
        # ---            
        frame1_2_2 = Frame(frame1_2)
        frame1_2_2 = LabelFrame(frame1_2)
        frame1_2_2.pack(side="left", fill="x", expand=True, padx = (5,0))
        frame1_2_2.configure(bg = self.background)
        
        var1 = IntVar(self.lockUnlockPage)
        var1.set(6)
        labels1 = [("TRX" , 1),
                  ("LAPD", 2),
                  ("BTS" , 3),
                  ("BCF" , 4),
                  ("OMU" , 5),
                  ("ALL" , 6)]
        for (label, value) in labels1:
            radiobutton = Radiobutton(frame1_2_2, text=label, variable=var1, value=value, command = lambda: self.lockUnlockScript(var, var1, outputBox))
            radiobutton.pack( side = "left", anchor=CENTER, fill = "x")
        # ---        
        frame1_3 = Frame(self.lockUnlockPage)
        frame1_3.pack(side="top", fill="both", expand=True, padx = (5,5), pady = (5,0))
        frame1_3.configure(background = self.background)
        yscrollbar = ttk.Scrollbar(frame1_3)
        yscrollbar.pack(side=RIGHT, fill=Y)
        outputBox = Text(frame1_3, wrap=NONE, yscrollcommand=yscrollbar.set)
        outputBox.pack(side = "top", fill="both", expand=True)
        yscrollbar.config(command=outputBox.yview)
        # ---        
        self.lockUnlockScript(var, var1, outputBox)
        
        return()

    
    def sctpView(self, event=None, preSelect=None):
        self.closePages()
        self.createPages()
        self.sctpPage.pack(side="top", fill="both", expand=True)
        self.sctpPage.config(background = self.background)
        # ---        
        frame1_1 = Frame(self.sctpPage)
        frame1_1.pack(side = "top" , fill=X, padx = (5,5), pady = (5,0))
        frame1_1.configure(background = self.background)
        
        Button1 = ttk.Button(frame1_1, text="Inputs")
        Button1.bind("<ButtonRelease-1>", self.inputView)
        Button1.pack(side = "left", ipadx=5)
        
        Button2 = ttk.Button(frame1_1, text="Lock & Unlock")
        Button2.bind("<ButtonRelease-1>", self.lockUnlockView)
        Button2.pack(side = "left", ipadx=5)
        
        Button3 = ttk.Button(frame1_1, text="SCTP")
        Button3.bind("<ButtonRelease-1>", )
        Button3.pack(side = "left", ipadx=5)
        
        Button4 = ttk.Button(frame1_1, text="Delete")
        Button4.bind("<ButtonRelease-1>", self.deleteView)
        Button4.pack(side = "left", ipadx=5)
        
        Button5 = ttk.Button(frame1_1, text="Clean UP")
        Button5.bind("<ButtonRelease-1>", self.cleanUpView)
        Button5.pack(side = "left", ipadx=5)
        
        bscLabel = Label(frame1_1, text="BSC TYPE: ", anchor=W, bg=self.background, fg="blue")
        bscLabel.pack(side = "left",  fill="both", expand=True, padx = (5,0))
        bscLabel.config(text="BSC TYPE: {}".format(self.bscType))
        # ---
        frame1_2 = Frame(self.sctpPage)
        frame1_2 = LabelFrame(self.sctpPage)
        frame1_2.pack(side = "top", fill=X, padx = (5,5))
        frame1_2.configure(bg = self.background)

        
        var = IntVar(self.sctpPage)
        if(str(preSelect)!="None"):
            var.set(preSelect)
        else:
            var.set(1)
        labels = [("Interrogate" , 1),
                  ("Activate"    , 2),
                  ("Deactivate"  , 3),
                  ("Update"      , 4)]
        for (label, value) in labels:
            radiobutton = Radiobutton(frame1_2, text=label, variable=var, value=value, command = lambda: self.sctpScript(var, outputBox))
            radiobutton.pack( side = "left", anchor=CENTER, fill = X)

        frame1_3 = Frame(self.sctpPage)
        frame1_3.pack(side = "top", fill="both", expand=True, padx = (5,5), pady = (5,0))
        frame1_3.configure(background = self.background)
        yscrollbar = ttk.Scrollbar(frame1_3)
        yscrollbar.pack(side=RIGHT, fill=Y)
        outputBox = Text(frame1_3, wrap=NONE, yscrollcommand=yscrollbar.set)
        outputBox.pack(side = "top", fill="both", expand=True)
        yscrollbar.config(command=outputBox.yview)
        # ---        
        self.sctpScript(var, outputBox)
        
        return()
    
    def sctpUpdateView(self, event=None):
        self.closePages()
        self.createPages()
        self.sctpUpdatePage.pack(side="top", fill="both", expand=True)
        self.sctpUpdatePage.config(background = self.background)
        # ---   
        frame1_1 = Frame(self.sctpUpdatePage)
        frame1_1.pack(side = "top" , fill=X, padx = (5,5), pady = (5,0))
        frame1_1.configure(background = self.background)
        
        Button1 = ttk.Button(frame1_1, text="Inputs")
        Button1.bind("<ButtonRelease-1>", self.inputView)
        Button1.pack(side = "left", ipadx=5)
        
        Button2 = ttk.Button(frame1_1, text="Lock & Unlock")
        Button2.bind("<ButtonRelease-1>", self.lockUnlockView)
        Button2.pack(side = "left", ipadx=5)
        
        Button3 = ttk.Button(frame1_1, text="SCTP")
        Button3.bind("<ButtonRelease-1>", self.sctpView)
        Button3.pack(side = "left", ipadx=5)
        
        Button4 = ttk.Button(frame1_1, text="Delete")
        Button4.bind("<ButtonRelease-1>", self.deleteView)
        Button4.pack(side = "left", ipadx=5)
        
        Button5 = ttk.Button(frame1_1, text="Clean UP")
        Button5.bind("<ButtonRelease-1>",self.cleanUpView)
        Button5.pack(side = "left", ipadx=5)
        
        bscLabel = Label(frame1_1, text="BSC TYPE: ", anchor=W, bg=self.background, fg="blue")
        bscLabel.pack(side = "left",  fill="both", expand=True, padx = (5,0))
        bscLabel.config(text="BSC TYPE: {}".format(self.bscType))
        
        frame1_2 = Frame(self.sctpUpdatePage)
        frame1_2 = LabelFrame(self.sctpUpdatePage)
        frame1_2.pack(side = "top", fill=X, padx = (5,5))
        frame1_2.configure(bg = self.background)

        var = IntVar(self.mainFrame)
        var.set(4)
        labels = [("Interrogate" , 1),
                  ("Activate"    , 2),
                  ("Deactivate"  , 3),
                  ("Update"      , 4)]
        for (label, value) in labels:
            radiobutton = Radiobutton(frame1_2, text=label, variable=var, value=value, command = lambda: self.sctpUpdateScript(var, outputBox))
            radiobutton.pack( side = "left", anchor=CENTER, fill = X)
 
        frame1_3 = Frame(self.sctpUpdatePage)
        frame1_3.pack(side = "top", fill=X, padx = (5,5), pady = (5,0))
        frame1_3.configure(bg = self.background)
        Label1 = Label(frame1_3, text="Site IP:", bg=self.background)
        Label1.pack(side = "left", ipadx=5)
        Entry1 = Entry(frame1_3)
        Entry1.pack(side = "left", ipadx=5)
        label = Label(frame1_3, text="", bg=self.background)
        label.pack(side = "left", padx = (5,5), pady = (5,0))

        frame1_4 = Frame(self.sctpUpdatePage)
        frame1_4.pack(side = "top", fill="both", expand=True, padx = (5,5), pady = (5,0))
        frame1_4.configure(background = self.background)
        yscrollbar = ttk.Scrollbar(frame1_4)
        yscrollbar.pack(side=RIGHT, fill=Y)
        outputBox = Text(frame1_4, wrap=NONE, yscrollcommand=yscrollbar.set)
        outputBox.pack(side = "top", fill="both", expand=True)
        yscrollbar.config(command=outputBox.yview)
        self.sctpUpdateScript(var, outputBox)
        
        btn_read = ttk.Button(self.sctpUpdatePage, text="Read Input")
        btn_read.bind("<ButtonRelease-1>", '')
        btn_read.pack(side = "left", padx = (5,5), pady = (5,0))

        if not self.sctp:
            label.config(text="INTERROGATE SCTP ASSOCIATION")
            interrogateOption = 1
            self.sctpScript(interrogateOption, outputBox)
            return()
        if self.sctp and not self.zqri:
            label.config(text="INTERROGATE NETWORK INTERFACES AND IP ADDRESSES")
            return()
            
        return()

    def deleteView(self, event):
        self.closePages()
        self.createPages()
        self.deletePage.pack(side="top", fill="both", expand=True)
        self.deletePage.config(background = self.background)
        # --- 
        frame1_1 = Frame(self.deletePage)
        frame1_1.pack(side = "top" , fill=X, padx = (5,5), pady = (5,0))
        frame1_1.configure(background = self.background)
        
        Button1 = ttk.Button(frame1_1, text="Inputs")
        Button1.bind("<ButtonRelease-1>", self.inputView)
        Button1.pack(side = "left", ipadx=5)
        
        Button2 = ttk.Button(frame1_1, text="Lock & Unlock")
        Button2.bind("<ButtonRelease-1>", self.lockUnlockView)
        Button2.pack(side = "left", ipadx=5)
        
        Button3 = ttk.Button(frame1_1, text="SCTP")
        Button3.bind("<ButtonRelease-1>", self.sctpView )
        Button3.pack(side = "left", ipadx=5)
        
        Button4 = ttk.Button(frame1_1, text="Delete")
        Button4.bind("<ButtonRelease-1>", self.deleteView)
        Button4.pack(side = "left", ipadx=5)
        
        Button5 = ttk.Button(frame1_1, text="Clean UP")
        Button5.bind("<ButtonRelease-1>", self.cleanUpView)
        Button5.pack(side = "left", ipadx=5)
        
        bscLabel = Label(frame1_1, text="BSC TYPE: ", anchor=W, bg=self.background, fg="blue")
        bscLabel.pack(side = "left",  fill="both", expand=True, padx = (5,0))
        bscLabel.config(text="BSC TYPE: {}".format(self.bscType))
        # ---         
        frame1_2 = Frame(self.deletePage)
        frame1_2 = LabelFrame(self.deletePage)
        frame1_2.pack(side = "top", fill=X, padx = (5,5))
        frame1_2.configure(background = self.background)
        
        var = IntVar(self.mainFrame)
        var.set(6)
        labels = [("TRX" , 1),
                  ("LAPD", 2),
                  ("BTS" , 3),
                  ("BCF" , 4),
                  ("OMU" , 5),
                  ("ALL" , 6)]
        for (label, value) in labels:
            radiobutton = Radiobutton(frame1_2, text=label, variable=var, value=value, command = lambda: self.deleteScript(var, outputBox))
            radiobutton.pack( side="left", anchor=CENTER, fill="x")
        # ---         
        frame1_3 = Frame(self.deletePage)
        frame1_3.pack(side = "top", fill="both", expand=True, padx = (5,5), pady = (5,0))
        frame1_3.configure(background = self.background)
        yscrollbar = ttk.Scrollbar(frame1_3)
        yscrollbar.pack(side=RIGHT, fill=Y)
        outputBox = Text(frame1_3, wrap=NONE, yscrollcommand=yscrollbar.set)
        outputBox.pack(side="top", fill="both", expand=True)
        yscrollbar.config(command=outputBox.yview)
        # ---         
        self.deleteScript(var, outputBox)
        return()

    def cleanUpView(self, event):
        self.closePages()
        self.createPages()
        self.cleanUpPage.pack(side="top", fill="both", expand=True)
        self.cleanUpPage.config(background = self.background)
        # --- 
        frame1_1 = Frame(self.cleanUpPage)
        frame1_1.pack(side = "top" , fill=X, padx = (5,5), pady = (5,0))
        frame1_1.configure(background = self.background)
        
        Button1 = ttk.Button(frame1_1, text="Inputs")
        Button1.bind("<ButtonRelease-1>", self.inputView)
        Button1.pack(side = "left", ipadx=5)
        
        Button2 = ttk.Button(frame1_1, text="Lock & Unlock")
        Button2.bind("<ButtonRelease-1>", self.lockUnlockView)
        Button2.pack(side = "left", ipadx=5)
        
        Button3 = ttk.Button(frame1_1, text="SCTP")
        Button3.bind("<ButtonRelease-1>", self.sctpView )
        Button3.pack(side = "left", ipadx=5)
        
        Button4 = ttk.Button(frame1_1, text="Delete")
        Button4.bind("<ButtonRelease-1>", self.deleteView)
        Button4.pack(side = "left", ipadx=5)
        
        Button5 = ttk.Button(frame1_1, text="Clean UP")
        Button5.bind("<ButtonRelease-1>", self.cleanUpView)
        Button5.pack(side = "left", ipadx=5)
        
        bscLabel = Label(frame1_1, text="BSC TYPE: ", anchor=W, bg=self.background, fg="blue")
        bscLabel.pack(side = "left",  fill="both", expand=True, padx = (5,0))
        bscLabel.config(text="BSC TYPE: {}".format(self.bscType))
        # ---         
        frame1_2 = Frame(self.cleanUpPage)
        frame1_2.pack(side = "top", fill="both", expand=True, padx = (5,5))
        frame1_2.configure(background = self.background)
        
        yscrollbar = ttk.Scrollbar(frame1_2)
        yscrollbar.pack(side=RIGHT, fill=Y)
        outputBox = Text(frame1_2, wrap=NONE, yscrollcommand=yscrollbar.set)
        outputBox.pack(side="top", fill="both", expand=True)
        yscrollbar.config(command=outputBox.yview)
        # ---         
        self.cleanUpScript(outputBox)
        return()
    
#--------------------------------------------------------------------------------------------------------------------------------------
#       Read 
#--------------------------------------------------------------------------------------------------------------------------------------
    def readInputs(self, event):
        self.dump = self.textBox.get("1.0",END)
        read = Dx200_BSC.Mml_Command()
        self.bcf_info = read.ZEEI(self.dump)
        for bscType, bcfModel, bscName, omuName, omuId, bcfType, bcfId, bcf_sig, lac, ci, btsId, btsName, trxName, trxID, trx_freq, trx_pcm, trx_channel, trx_pref, trx_sig in self.bcf_info:
            self.omuName = omuName
            self.omuID = omuId
            self.bscType = bcfType
            self.bcf = bcfId
            t = (btsId, trxName, trxID)
            self.trx.append(t)
            if btsId not in self.bts:
                self.bts.append(btsId)
            if trx_pcm not in self.pcm:
                self.pcm.append(trx_pcm)

        print(self.pcm)       
        for pcm in self.pcm:
            dap = read.ZESI(self.dump, pcm)
            if dap not in self.dap and not dap == None:
                self.dap.append(dap)
                
            csdap = read.ZESB(self.dump, pcm)
            print(csdap)
            if csdap not in self.csdap and not csdap == None:
                self.csdap.append(csdap) 

                
        zdti = read.ZDTI(self.dump)
        for NAME, NUM, UNIT, SIDE, PCM_TSL_TSL, SAPI, STATE  in zdti:
            if NAME not in self.lapd:
                self.lapd.append(NAME)

        self.bscLabel.config(text="BSC TYPE: {}".format(self.bscType))
        return()

    def readSctp(self):
        return()

    def readZOYV(self):
        zoyv = False
        for line in self.dump.splitlines():
            if "ZOYV:IUA:" in line:
                zoyv = True
                continue
            if zoyv and self.omuID in line:               
                word = line.split()
                if self.omuID in word[0]:
                    d = (word[0], word[1], word[2], word[3], word[4], word[5], word[6])
                    self.sctp.append(d)
            if "COMMAND EXECUTED" in line and zoyv:
                break
        #print(self.sctp)        
        return()
    
    def readZDWQ(self):
        zdwq = False
        for line in self.dump.splitlines():
            if "DWQ;" in line:
                zdwq = True
                continue
            if zdwq and self.omuID in line:               
                word = line.split()
                if self.omuID in word[5]:
                    d = (word[0], word[1], word[2], word[3], word[4], word[5], word[6], word[7], word[8])
                    self.dChannel.append(d)
            if "COMMAND EXECUTED" in line and zdwq:
                break
        #print(self.dChannel)

        
        return()

















    
#--------------------------------------------------------------------------------------------------------------------------------------
#       Create Scripts
#--------------------------------------------------------------------------------------------------------------------------------------
    def lockUnlockScript(self, varLockUnlock, varSelect, outputBox):
        outputBox.delete('1.0', END)
        if not self.bcf:           
            outputBox.insert(END,"BCF not found\n")
            return()
        varLockUnlock = str(varLockUnlock.get())
        varSelect = str(varSelect.get())

        # lock method
        if(varLockUnlock=="1"):
            if(varSelect=="1"): # lock TRX
                for item in self.trx:
                    bts, trxName, trxID = item
                    outputBox.insert(END,"ZERS:BTS={},TRX={}:L;\n".format(bts, trxID))
            elif(varSelect=="2"): # lock LAPD
                for lapd in self.lapd:
                    outputBox.insert(END,"ZDTC:{}:AD;\n".format(lapd))
            elif(varSelect=="3"): # lock BTS
                for bts in self.bts:
                    outputBox.insert(END,"ZEQS:BTS={}:L;\n".format(bts))
            elif(varSelect=="4"): # lock BCF
                outputBox.insert(END,"ZEFS:{}:L;\n".format(self.bcf))
            elif(varSelect=="5"): # lock OMU    
                outputBox.insert(END,"ZDTC:{}:AD;\n".format(self.omuName))
            elif(varSelect=="6"): #lock All
                outputBox.insert(END,"ZDTC:{}:AD;\n".format(self.omuName))
                outputBox.insert(END,"ZEFS:{}:L;\n".format(self.bcf))
                for bts in self.bts:
                    outputBox.insert(END,"ZEQS:BTS={}:L;\n".format(bts))
                for item in self.trx:
                    bts, trxName, trxID = item
                    outputBox.insert(END,"ZERS:BTS={},TRX={}:L;\n".format(bts, trxID))
                for lapd in self.lapd:
                    outputBox.insert(END,"ZDTC:{}:AD;\n".format(lapd))
            return()
        
        # unlock method
        elif(varLockUnlock=="2"):
            if(varSelect=="1"): # unlock TRX
                for item in self.trx:
                    bts, trxName, trxID = item
                    outputBox.insert(END,"ZERS:BTS={},TRX={}:U;\n".format(bts, trxID))
            elif(varSelect=="2"): # unlock LAPD
                for lapd in self.lapd:
                    outputBox.insert(END,"ZDTC:{}:WO;\n".format(lapd))
            elif(varSelect=="3"): # unlock BTS
                for bts in self.bts:
                    outputBox.insert(END,"ZEQS:BTS={}:U;\n".format(bts))
            elif(varSelect=="4"): # unlock BCF
                outputBox.insert(END,"ZEFS:{}:U;\n".format(self.bcf))
            elif(varSelect=="5"): # unlock OMU    
                outputBox.insert(END,"ZDTC:{}:WO;\n".format(self.omuName))
            elif(varSelect=="6"): # unlock All
                outputBox.insert(END,"ZDTC:{}:WO;\n".format(self.omuName))
                for lapd in self.lapd:
                    outputBox.insert(END,"ZDTC:{}:WO;\n".format(lapd))
                for item in self.trx:
                    bts, trxName, trxID = item
                    outputBox.insert(END,"ZERS:BTS={},TRX={}:U;\n".format(bts, trxID))
                for bts in self.bts:
                    outputBox.insert(END,"ZEQS:BTS={}:U;\n".format(bts))
                outputBox.insert(END,"ZEFS:{}:U;\n".format(self.bcf))   
            return()
        return()

    def sctpScript(self, var, outputBox):
        try:
            var = str(var.get())
        except Exception:
            var = str(var)
        outputBox.delete('1.0', END)
        if not self.bcf:           
            outputBox.insert(END,"BCF not found\n")
            return()
        if(var=='1'): # interrogate
            outputBox.delete('1.0', END)
            outputBox.insert(END,"ZOYV:IUA:NAME=BCF{}OMU:A;\n".format(self.omuID))
            for item in self.trx:
                bts, trxName, trxID = item
                outputBox.insert(END,"ZOYV:IUA:NAME=BCF{}{}:A;\n".format(self.bcf, trxName))
            return()
        elif(var=='2'): # activate
            outputBox.delete('1.0', END)
            outputBox.insert(END,"ZOYS:IUA:BCF{}OMU:ACT;\n".format(self.omuID))
            for item in self.trx:
                bts, trxName, trxID = item
                outputBox.insert(END,"ZOYS:IUA:BCF{}{}:ACT;\n".format(self.bcf, trxName))
            return()
        elif(var=='3'): # deactivate
            outputBox.delete('1.0', END)
            outputBox.insert(END,"ZOYS:IUA:BCF{}OMU:DOWN;\n".format(self.omuID))
            for item in self.trx:
                bts, trxName, trxID = item
                outputBox.insert(END,"ZOYS:IUA:BCF{}{}:DOWN;\n".format(self.bcf, trxName))
        elif(var=='4'):
            outputBox.delete('1.0', END)
            self.sctpUpdateView()
        return()
    
    def sctpUpdateScript(self, var, outputBox):
        outputBox.delete('1.0', END)
        if not self.bcf:           
            outputBox.insert(END,"BCF not found\n")
            return()
        var = str(var.get())
        if(var=='1'):
            self.sctpView(None, "1")
            return()
        elif(var=='2'):
            self.sctpView(None, "2")
            return()
        elif(var=='3'):
            self.sctpView(None, "3")
            return()
        return()

    def deleteScript(self, var, outputBox):
        outputBox.delete('1.0', END)
        var = str(var.get())
        if var == "1": # delete TRX
            if not self.trx:           
                outputBox.insert(END,"TRXs not found\n")
                return()
            for item in self.trx:
                bts, trxName, trxID = item
                outputBox.insert(END,"ZERD:BTS={},TRX={};\n".format(bts, trxID))
            return()
        if var == "2": # delete LAPD
            if not self.lapd:           
                outputBox.insert(END,"PCMs not found\n")
                return()
            for lapd in self.lapd:
                outputBox.insert(END,"ZDSD:{}:;\n".format(lapd))
            return()
        if var == "3": # delete BTS
            if not self.bts:           
                outputBox.insert(END,"BTSs not found\n")
                return()
            for bts in self.bts:
                outputBox.insert(END,"ZEQD:BTS={}:N;\n".format(bts))
            return()
        if var == "4": # delete BCF
            if not self.bcf:           
                outputBox.insert(END,"BCF not found\n")
                return()
            outputBox.insert(END,"ZEFD:{}:;\n".format(self.bcf))
            return()
        if var == "5": # delete OMU
            if not self.omuName:           
                outputBox.insert(END,"OMU not found\n")
                return()
            outputBox.insert(END,"ZDSD:{}:;\n".format(self.omuName))
            return()
        if var == "6": # delete ALL
            if self.lapd: 
                for lapd in self.lapd:
                    outputBox.insert(END,"ZDSD:{}:;\n".format(lapd))
            if self.trx:            
                for item in self.trx:
                    bts, trxName, trxID = item
                    outputBox.insert(END,"ZERD:BTS={},TRX={};\n".format(bts, trxID))
            if self.bts:               
                for bts in self.bts:
                    outputBox.insert(END,"ZEQD:BTS={}:N;\n".format(bts))
            if self.bcf:         
                outputBox.insert(END,"ZEFD:{}:;\n".format(self.bcf))
            if self.omuName:    
                outputBox.insert(END,"ZDSD:{}:;\n".format(self.omuName))                     
        return()

    def cleanUpScript(self, outputBox):
        outputBox.delete('1.0', END)
        if not self.lapd:
            outputBox.insert(END,"PCMs not found\n")
            return()
        outputBox.insert(END,"######## LOCK LAPDs ########\n")
        for lapd in self.lapd:
            outputBox.insert(END,"ZDTC:{}:AD;\n".format(lapd))
        outputBox.insert(END,"######## DELETE  LAPDs ########\n")
        for lapd in self.lapd:
            outputBox.insert(END,"ZDSD:{};\n".format(lapd))
        outputBox.insert(END,"######## DELETE  DAP ########\n")
        for dap in self.dap:
            outputBox.insert(END,"ZESG:ID={};\n".format(dap))
        outputBox.insert(END,"######## DELETE  CSDAP ########\n")
        for csdap in self.csdap:
            outputBox.insert(END,"ZESV:CID={};\n".format(csdap))
        for pcm in self.pcm:
            outputBox.insert(END,"######## ET-PCM {} ########\n".format(pcm))
            outputBox.insert(END,"ZUSI:ET,{};\n".format(pcm))
            outputBox.insert(END,"ZUSC:ET,{}:TE,FCD;\n".format(pcm))
            outputBox.insert(END,"ZUSC:ET,{}:SE;\n".format(pcm))
            outputBox.insert(END,"ZUSC:ET,{}:SE;\n".format(pcm))
            outputBox.insert(END,"ZAHO:ET,{};\n".format(pcm))
            outputBox.insert(END,"ZYEF:ET,{};\n".format(pcm))
            outputBox.insert(END,"ZYMO:ET,{};\n".format(pcm))
            outputBox.insert(END,"ZDSB:::PCM={};\n".format(pcm))
            outputBox.insert(END,"ZDTI:::PCM={};\n".format(pcm))
        return()
        
