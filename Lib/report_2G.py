from tkinter import *
from tkinter import filedialog

var_x = 16
    
class Report_2G():
    global var_x

    def __init__(self, root, mainFrame, background):
        self.root = root
        self.mainFrame = mainFrame
        self.backgound = background
        
    def main(self):       
        self.root.update()
        self.root_width = self.root.winfo_width()
        self.root_height = self.root.winfo_height()      

        self.mainFrame = Frame(self.root)
        self.mainFrame.pack(fill = BOTH)
        self.mainFrame.configure(background = self.backgound)
        self.frame1 = Frame(self.mainFrame)
        self.frame1.pack(side = TOP , fill=X, padx = (5,0), pady = (5,0))
        self.frame1.configure(background = self.backgound)
        self.Button1 = Button(self.frame1, text="Read ZEEI\ZESI")
        self.Button1.bind("<Button-1>", self.readInputs)
        self.Button1.pack(side = LEFT, ipadx=5)
        self.Button2 = Button(self.frame1, text="Script")
        self.Button2.bind("<Button-1>", self.atmScript)
        self.Button2.pack(side = LEFT, ipadx=5)

          
        self.frame2 = Frame(self.mainFrame)
        self.frame2.pack(side = TOP, fill = X, padx = (5,0), pady = (5,0))
        self.frame2.configure(background = self.backgound)  
        self.inputText = Text(self.frame2, height = self.root_height, width = int(self.root_width/var_x))
        self.inputText.pack(side = LEFT)
        self.outputText = Text(self.frame2, height = self.root_height, width = int(self.root_width/var_x))
        self.outputText.pack(side = LEFT, padx = 5)
       
        self.root.bind('<Configure>', self.rootSize)
        self.dump = ''
        self.bcf = ''
        self.bts = []
        self.pcm = []
        self.dap = []
    
    def rootSize(self, event):
        self.root.update()
        self.root_width = self.root.winfo_width()
        self.root_height = self.root.winfo_height()
        self.Button1.config(text="Read ZEEI\ZESI")
        self.Button2.config(text="Script")
        self.inputText.config(height = self.root_height, width = int(self.root_width/var_x))
        self.outputText.config(height = self.root_height, width = int(self.root_width/var_x))
        return();    

    def readInputs(self, event):

        return()

    def atmScript(self, event):
        if(self.bcf==''):
            return()

        return()

    def abisOverEthScript(self, event):
        if(self.bcf==''):
            return()
        self.outputText.delete(1.0,END)
        return()
    
    def abisOverTdmScript(self, event):
        if(self.bcf==''):
            return()
        self.outputText.delete(1.0,END)
        return()
    
    def closeFrame(self):
        try:
            self.mainFrame.destroy()
        except Exception:
            pass
        return















    
