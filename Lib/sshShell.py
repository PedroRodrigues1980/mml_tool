#!/usr/bin/python3.6
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import paramiko
from paramiko.ssh_exception import AuthenticationException, SSHException, BadHostKeyException
from threading import Thread
import time

customerName =['Claro Brasil',
               'TIM Brasil',
               'OI Brasil']

elementNameClaro = [('nok2cs1','10.115.181.128'),
                    ('nok2cs2','10.115.181.129')]

elementNameTIM = [('TIM SSH1', '000.000.000.000'),
                  ('TIM SSH2', '000.000.000.000')]

elementNameOI = [('RC06cs1(NA 5)', '10.115.181.87'),
                 ('RC06cs2(NA 5)', '10.115.181.88'),
                 ('RC07cs1(NA 5)', '10.115.181.96'),
                 ('RC07cs2(NA 5)', '10.115.181.97')]


class CustomNotebook(ttk.Notebook):
    """A ttk Notebook with close buttons on each tab"""
    __initialized = False

    def __init__(self, *args, **kwargs):
        if not self.__initialized:
            #self.__initialize_custom_style()
            self.__inititialized = True

        ttk.Notebook.__init__(self, *args, **kwargs)

        self._active = None

        self.bind("<ButtonPress-3>", self.on_close_press, True)
        self.bind("<ButtonRelease-3>", self.on_close_release)

    def on_close_press(self, event):
        """Called when the button is pressed over the close button"""
        element = self.identify(event.x, event.y)

        index = self.index("@%d,%d" % (event.x, event.y))
        self.state(['pressed'])
        self._active = index

    def on_close_release(self, event):
        """Called when the button is released over the close button"""
        if not self.instate(['pressed']):
            return

        element =  self.identify(event.x, event.y)
        # if event.x, event.y not in tb exception is activated
        try:
            index = self.index("@%d,%d" % (event.x, event.y))
        except Exception:
            return

        if self._active == index:
            self.forget(index)
            self.event_generate("<<NotebookTabClosed>>")

        self.state(["!pressed"])
        self._active = None
    

#-------------------------------------------------------------------------------------------------------------------------------
#   TAB VIEW
#-------------------------------------------------------------------------------------------------------------------------------         
class NewTab():
    def __init__(self, tab):
        self.newtab = tab
        self.outputFrame = Frame(self.newtab)
        self.outputFrame.pack(side = "top", fill="both", expand=True)
        
        yscrollbar = Scrollbar(self.outputFrame)
        yscrollbar.pack(side=RIGHT, fill=Y)
        self.outputText = Text(self.outputFrame, wrap=NONE, bg="BLACK", fg="WHITE", yscrollcommand=yscrollbar.set, state="disabled")
        self.outputText.pack(side = TOP, fill=BOTH, expand=True)
        yscrollbar.config(command=self.outputText.yview)
               
        self.inputFrame = Frame(self.newtab)
        self.inputFrame.pack(side = BOTTOM, fill=X, pady=(10,0))
        
        self.commandLabel = Label(self.inputFrame, text="Command>>")
        self.commandLabel.pack(side = LEFT)
        
        self.inputMML = Entry(self.inputFrame, relief="groove")
        self.inputMML.focus_force()
        self.inputMML.pack(side = LEFT, fill=X, expand=True)     
        
        self.exportBt = Button(self.inputFrame, text='Clear', relief="groove")
        self.exportBt.bind("<ButtonRelease-1>", self.resetOutput)
        self.exportBt.pack(side=RIGHT, anchor=W, padx=(5,0))

        self.copyBt = Button(self.inputFrame, text='Copy All', relief="groove")
        self.copyBt.bind("<ButtonRelease-1>", self.copyToClipboard)
        self.copyBt.pack(side=RIGHT, anchor=W, padx=(5,0))

        self.recordBt = Button(self.inputFrame, text='Record Session', relief="groove", bg='steelblue', fg='white')
        self.recordBt.bind("<ButtonRelease-1>", self.recordHistory)
        self.recordBt.pack(side=RIGHT, anchor=W, padx=(5,0))
        
    #-------------------------------------------------------------------------------------------------------------------------------
    #       BUTTON EVENT
    #-------------------------------------------------------------------------------------------------------------------------------
    def recordHistory(self, event):
        ''' permite o historico da sessão. a diretoria e ficheiro ficam em self.recordFile. o log em self.recordBt'''
        if not self.recordFile:
            try:
                self.recordFile = filedialog.asksaveasfilename(initialdir = "/",title = "Select file",filetypes = (("TXT files","*.txt"),("all files","*.*")))
                self.recordLog = open(self.recordFile,'w',encoding='utf_8')
                self.recordBt.config(text='Stop Record', bg='lightcoral', fg='white')
                self.outputFrame.focus_force()
            except Exception as e:
                self.outputText.insert(END,'{}\n'.format(e))
                
        elif self.recordFile:
            try:
                self.recordLog.close()
                self.recordBt.config(text='Record Session', bg='steelblue', fg='white')
                self.recordFile = ''
                self.outputFrame.focus_force()
            except Exception as e:
                self.outputText.insert(END,'{}\n'.format(e))
        return()
    
    def copyToClipboard(self, event):
        ''' copia o que está na text box para o clipboard '''
        self.outputText.clipboard_clear()
        self.outputText.clipboard_append(self.outputText.get(1.0,END).encode('UTF-8'))
        return()

    def resetOutput(self, event):
        self.inputMML.focus()
        #self.inputMML.grab_set()
        self.outputText.configure(state="normal")
        self.outputText.delete(1.0,END)
        #self.inputMML.grab_release()
        return()
    
    def destroyTopLevel(self, event):
        if self.sshChannel:
            self.sshChannel.close()
        if self.sshSession:
            self.sshSession.close()
        self.destroy()
        return()

        
    #-------------------------------------------------------------------------------------------------------------------------------
    #       EXTERNAL EVENTS
    #-------------------------------------------------------------------------------------------------------------------------------
    def mouseEvent(self, event):
        ''' go to mml command box'''
        self.inputMML.focus_force()
        return()

    def mousePastEvent(self, event):
        ''' past mml command to mml box'''
        cmdList = self.newtab.clipboard_get()
        self.inputMML.focus_force()
        for cmd in cmdList.split('\n'):
            self.inputMML.insert(END,cmd)
            self.sendDataSshChannel()
        return()
    
    def copySelectText(self, event):
        self.selectText = ''
        try:
            self.selectText = event.widget.get(SEL_FIRST, SEL_LAST)
        except Exception:
            pass
        self.outputText.clipboard_clear()
        self.outputText.clipboard_append(self.selectText.encode('UTF-8'))
        return()

    def keyboardEvent(self, event):
        ctrl  = (event.state & 0x4) != 0
        if(ctrl and event.keycode==89): # Ctrl+y
            self.ctrl_Y()
        elif(event.keycode==38):        # Arrow UP
            self.arrowUP()
        elif(event.keycode==40):        # Arrow DOWN
            self.arrowDOWN()
        elif(event.keycode==9):         # Tab
            self.tabBind()
        elif(event.keycode==13):        # Enter
            self.sendDataSshChannel()
        self.inputMML.focus_force()
        return()
    
    def arrowUP(self):
        self.inputMML.focus()
        if not self.mmlCommandHistory:
            return()
        cmd = self.mmlCommandHistory[len(self.mmlCommandHistory)-self.mmlCommandHistoryIndex]
        self.inputMML.delete(0,END)
        self.inputMML.insert(END,cmd)
        self.mmlCommandHistoryIndex += 1
        if self.mmlCommandHistoryIndex > len(self.mmlCommandHistory):
            self.mmlCommandHistoryIndex = len(self.mmlCommandHistory)
        return()

    def arrowDOWN(self):
        self.inputMML.focus()
        if not self.mmlCommandHistory:
            return()
        cmd = self.mmlCommandHistory[abs(self.mmlCommandHistoryIndex - len(self.mmlCommandHistory))]
        self.inputMML.delete(0,END)
        self.inputMML.insert(END,cmd)
        self.mmlCommandHistoryIndex -= 1
        if self.mmlCommandHistoryIndex < 1:
            self.mmlCommandHistoryIndex = 1
        return()
    
    def ctrl_Y(self):
        self.inputMML.focus()
        self.inputMML.delete(0,END)
        self.sendDataSshChannel('\25')
        return()
    
    def tabBind(self):
        tab = 'c7xtermx -n '
        self.inputMML.focus()
        self.inputMML.delete(0,END)
        self.inputMML.insert(END,tab)
        self.inputMML.focus()
        return()


#-------------------------------------------------------------------------------------------------------------------------------
#   SSH SHELL
#------------------------------------------------------------------------------------------------------------------------------- 
class NewConn(NewTab, Thread):
    def __init__(self,tab, ipAddress, username,password):
        super().__init__(tab)
        Thread.__init__(self)
        self.demand = True
        self._running = True
        
        self.ipAddress = ipAddress
        self.username = username
        self.password = password
        
        self.sshChannel = None
        self.sshSession = None
        self.mmlCommandHistory=[]
        self.mmlCommandHistoryIndex = 1

        self.selectText = ''
        self.recordFile = ''
        self.recordLog = ''
        self.openSshConnect()
        
    def run(self):
        while self._running:
            self.receiveDataSshChannel()
            time.sleep(0.2)
            #print(self)

    def terminate(self):
        #print("Terminate thread: {}".format(self))
        self._running = False


    def ativateExternalEvent(self): 
        self.inputMML.focus_set()
        self.outputText.bind("<KeyRelease>", self.keyboardEvent)
        self.outputText.bind("<ButtonRelease-1>", self.mouseEvent)
        self.outputText.bind("<ButtonRelease-3>", self.mousePastEvent)
        self.outputText.bind("<B1-Motion>", self.copySelectText)  
        self.inputMML.bind("<Key>", self.keyboardEvent)
        
    def openSshConnect(self):
        ''' establish ssh conection '''
        ''' create a ssh session and open a shell '''
        if(len(self.username)>50 or len(self.password)>50):
            self.outputText.configure(state="normal")
            self.outputText.insert("System username and password can not be longer than 50 caracters.\n")
            self.outputText.configure(state="disabled")
            return()
        self.outputText.configure(state="normal")
        self.outputText.insert(END,"Authentication to cluster\n")
        self.outputText.configure(state="disabled")
        #print("IP:", self.ipAddress, "Username:", self.username,"Password: ", self.password)
        try:
            #paramiko.util.log_to_file('ssh.log')
            self.sshSession = paramiko.SSHClient();
            self.sshSession.set_missing_host_key_policy(paramiko.AutoAddPolicy());
            self.sshSession.load_system_host_keys()
            self.sshSession.connect(hostname=self.ipAddress, port=22, username=self.username, password=self.password, timeout=None, look_for_keys=False, allow_agent=False);
        except AuthenticationException:
            self.outputText.configure(state="normal")
            self.outputText.insert(END, "Authentication failed, please verify your credentials:\n")
            self.outputText.configure(state="disabled") 
            return(False)
        except SSHException as sshException:
            self.outputText.configure(state="normal")
            self.outputText.insert(END, "Unable to establish SSH connection:")
            self.outputText.configure(state="disabled") 
            return(False)
        except BadHostKeyException as badHostKeyException:
            self.outputText.configure(state="normal")
            self.outputText.insert(END,"Unable to verify server's host key:n")
            self.outputText.configure(state="disabled")
            return(False)
        except Exception as e:
            self.outputText.configure(state="normal")
            self.outputText.insert(END, "Operation error: {}\n".format(e))
            self.outputText.configure(state="disabled") 
            return(False)
               
        #print(self.sshSession.get_transport().is_active())
        self.sshChannel = self.sshSession.invoke_shell()
        #inicia thread para ler
        self.start()
        # activa eventos externos
        self.ativateExternalEvent()
        


    
    def sendDataSshChannel(self, externalEvent=None):
        ''' execute by mml command ENTER '''
        cmd = self.inputMML.get()
        self.inputMML.delete(0,END)
        if externalEvent:
            cmd=externalEvent 
        #print(cmd)
        try:
            self.inputMML.focus()
            self.sshChannel.send(cmd+'\n')
            if not externalEvent and not len(cmd)==0:
                self.mmlCommandHistory.append(cmd)
                self.mmlCommandHistoryIndex = 1
        except Exception:
            pass
           
    def receiveDataSshChannel(self):
        ''' auto execute by THREAD  '''
        #print("Receive data to shell")
        if not self.sshChannel:
            return()
        alldata = ''
        while True:      
            if self.sshChannel.recv_ready():
                self.outputText.configure(state="normal")
                alldata += self.sshChannel.recv(99999999).decode("utf-8");
                #print(alldata);       
                self.outputText.insert(END,alldata)
                try:
                    self.recordLog.write(str(alldata)+'\n')
                except Exception:
                    pass
                self.outputText.see(END)
            else:
                last_line = alldata.split("\r")
                if last_line == "" or last_line=="\n" or last_line =="\r":
                    break
                #print(last_line)
                break
        
        self.outputText.configure(state="disabled")
        return()

    def receiveLastCommand(self):
        #print("Receive data to shell")
        if not self.sshChannel:
            return()
        lastCommand = ''
        while True:      
            if self.sshChannel.recv_ready():
                lastCommand += self.sshChannel.recv(99999999).decode("utf-8");
                #print(lastCommand);       
                self.inputMML.insert(END,lastCommand)
                self.inputMLL.focus()
            else:
                last_line = lastCommand.split("\r")
                if last_line == "" or last_line=="\n" or last_line =="\r":
                    break
                #print(last_line)
                break
        return()        



#-------------------------------------------------------------------------------------------------------------------------------
#   MAIN PAGE
#-------------------------------------------------------------------------------------------------------------------------------     
class SshShell(CustomNotebook):
    def __init__(self, root):
        self.root = root
        self.sshConnetions = [] # ssh obj
        self.sshShellStatus = True
        
        self.createMainView()
        
      
    def createMainView(self):
        self.sshShellStatus = True
        self.sshView = Toplevel(self.root)
        self.sshView.title("SSH Cluster Connection")
        self.ssh_Height = 650 
        self.ssh_Width = 900 
        self.mainHeightScreen = self.sshView.winfo_screenheight() # width of the screen
        self.mainWidthScreen = self.sshView.winfo_screenwidth() # height of the screen
        self.sshView.geometry('%dx%d+%d+%d' % (self.ssh_Width, self.ssh_Height, self.mainWidthScreen-self.ssh_Width-15, 0))
        self.sshView.minsize(800,600)

        self.sshView.focus_force()
        self.customersFrame = Frame(self.sshView)
        self.customersFrame = LabelFrame(self.sshView, text="Customers:")      
        self.customersFrame.pack(side = "top", fill="both", padx=(5,5))
        
        self.customerNameFrame = Frame(self.customersFrame)
        self.customerNameFrame.pack(side=LEFT, padx=(5,0))       
        self.customerNamelabel = Label(self.customerNameFrame, text="Customer Name")
        self.customerNamelabel.pack(side=TOP, anchor=W)
        customer = StringVar()
        self.customerNamecCombo = ttk.Combobox(self.customerNameFrame, value=customer)
        self.customerNamecCombo['value'] = customerName
        self.customerNamecCombo.current(2)
        self.customerNamecCombo.bind("<<ComboboxSelected>>", self.customerSelect)
        self.customerNamecCombo.pack(side="top", pady=(0,5))
        
        self.elementeNameFrame = Frame(self.customersFrame)
        self.elementeNameFrame.pack(side=LEFT, padx=(5,0)) 
        self.elementNameLabel = Label(self.elementeNameFrame, text="Element Name")
        self.elementNameLabel.pack(side=TOP, anchor=W)
        element = StringVar()
        self.elementNameCombo = ttk.Combobox(self.elementeNameFrame, value=element)
        self.elementNameCombo.bind("<<ComboboxSelected>>", self.elementSelect)
        self.elementNameCombo.pack(side="top", pady=(0,5))

        self.natAddressFrame = Frame(self.customersFrame)
        self.natAddressFrame.pack(side=LEFT, padx=(5,0)) 
        self.natAddressLabel1 = Label(self.natAddressFrame, text="NAT Address")
        self.natAddressLabel1.pack(side=TOP, anchor=W)
        self.natAddressLabel2 = Label(self.natAddressFrame, text="",relief="groove", width=15, anchor=W)
        self.natAddressLabel2.pack(side="top", pady=(0,5))
        
        self.usernameFrame = Frame(self.customersFrame)
        self.usernameFrame.pack(side=LEFT, padx=(5,0)) 
        self.usernameLabel = Label(self.usernameFrame, text="Username")
        self.usernameLabel.pack(side=TOP, anchor=W)
        self.username = Entry(self.usernameFrame)
        self.username.pack(side="top", pady=(0,5))
        self.username.insert(END,'d56496')

        self.passwordFrame = Frame(self.customersFrame)
        self.passwordFrame.pack(side=LEFT, padx=(5,0)) 
        self.passwordLabel = Label(self.passwordFrame, text="Password")
        self.passwordLabel.pack(side=TOP, anchor=W)
        self.password = Entry(self.passwordFrame, show='*')
        self.password.pack(side="top", pady=(0,5))
        self.password.insert(END,'Tele$123')

        self.connectFrame = Frame(self.customersFrame)
        self.connectFrame.pack(side=RIGHT, anchor=E, padx=(5,5))
        self.connectButton = Button(self.connectFrame, text="Connect", relief="groove", bg="steelblue", fg="white")
        self.connectButton.bind("<ButtonRelease-1>", self.addConnection)
        self.connectButton.pack(side="top", anchor="e", pady=(10,5), ipady=5, ipadx=9)

        self.defaultComboValues()
        
        self.notebook = CustomNotebook(self.sshView) 
        self.notebook.pack(side="top", expand=True, fill="both", padx=(5,5), pady=(0,5))

        
        self.sshView.protocol("WM_DELETE_WINDOW", self.destroyTopLevel)
         
    def addConnection(self, event):
        self.newtab = tk.Frame(self.notebook)
        self.notebook.add(self.newtab, text=self.elementName)
        
        ipAddress = self.elementIP
        username  = self.username.get()
        password  = self.password.get()
        ssh_conn = NewConn(self.newtab, ipAddress, username,password)
        self.sshConnetions.append(ssh_conn)

        
    def defaultComboValues(self):
        '''valores iniciais para as variaveis'''
        self.costumerID = customerName[2]
        self.elementName, self.elementIP = elementNameOI[0]
        self.customerSelect(None)
        self.elementSelect(None)
        
    def customerSelect(self, event):
        '''identifica o Customer Name e carrega no Combo Element Name os valores desse cliente'''
        self.costumerID = self.customerNamecCombo.get()
        #print(self.costumerID)
        connectionName = []
        #element name Claro
        if(self.costumerID==customerName[0]):
            for self.elementName, self.elementIP in elementNameClaro:
                connectionName.append(self.elementName)
            self.elementNameCombo['value'] = connectionName
            self.elementNameCombo.current(0)
        #element name TIM
        elif(self.costumerID==customerName[1]):
            for self.elementName, self.elementIP in elementNameTIM:
                connectionName.append(self.elementName)
            self.elementNameCombo['value'] = connectionName
            self.elementNameCombo.current(0)
        #element name OI
        elif(self.costumerID==customerName[2]):
            for self.elementName, self.elementIP in elementNameOI:
                connectionName.append(self.elementName)
            self.elementNameCombo['value'] = connectionName
            self.elementNameCombo.current(0)
        self.elementSelect(None)
        return()

     
    def elementSelect(self, event):
        '''identifica a ligacao que está no Element Name e atribui o IP ao NAT Address'''
        self.costumerID = self.customerNamecCombo.get()
        self.elementID = self.elementNameCombo.get()
        #print(self.costumerID, self.elementID)
        connectionName = []
        #element name Claro
        if(self.costumerID==customerName[0]):
            for name, ip in elementNameClaro:
                if name == self.elementNameCombo.get():
                    self.natAddressLabel2.config(text=ip)
                    self.elementName = name
                    self.elementIP = ip
        #element name TIM
        elif(self.costumerID==customerName[1]):
            for name, ip in elementNameTIM:
                if name == self.elementNameCombo.get():
                    self.natAddressLabel2.config(text=ip)
                    self.elementName = name
                    self.elementIP = ip
        #element name OI
        elif(self.costumerID==customerName[2]):
            for name, ip in elementNameOI:
                if name == self.elementNameCombo.get():
                    self.natAddressLabel2.config(text=ip)
                    self.elementName = name
                    self.elementIP = ip
        return()
    
    
    def destroyTopLevel(self):
        try:
            for ssh in self.sshConnetions:
                ssh.terminate()
        except Exception as e:
            print("Problemas a terminar thread:{}".format(e))
        self.sshView.destroy()
        self.sshShellStatus = False

    def active(self):
        return self.sshShellStatus

  
