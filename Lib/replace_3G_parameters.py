#!/usr/bin/python3.6
encoding='utf_8'
import os
import  xml.etree.ElementTree as ET
from tkinter import *
from tkinter import filedialog

class Replace_3G_Parameters(Frame):
    background = 'SystemButtonFace'
    def __init__(self, mainFrame):
        self.mainFrame = Frame(mainFrame, bg=self.background)
        self.mainFrame.pack(side="top", fill="both", expand="true")
        self.inputFile = ""
        self.outputFile = ""
        self.dir = ""
        self.oldSiteName = "'WBTSName'>"
        self.oldWbtsId = "WBTS-"
        self.oldRncId = "RNC-"
        self.newWbtsId = "WBTS-"
        
        self.gui_frame()

    def gui_frame(self):
        # ----
        #self.file = ttk.Button(self.mainFrame, text="Insert xml file", command = self.read_input)
        #self.file.pack(side = "top", fill="x", padx = (5,5), pady = (5,0), ipady=5)
        '''
        # ---
        self.frame1 = Frame(self.mainFrame)
        self.frame1.pack(side="top", fill="x", padx = (5,5), pady = (5,0))
        self.label1 = Label(self.frame1, text="Old Site Name", anchor="e", width=11, bg=self.background)
        self.label1.pack(side="left")
        self.entry1 = Entry(self.frame1)
        self.entry1.pack(side="left")
        '''
        # ----
        self.frame2 = Frame(self.mainFrame)
        self.frame2.pack(side="top", fill="x", padx = (5,5), pady = (5,0))
        self.label2_1 = Label(self.frame2, text="Old WBTS ID", anchor="e", width=11, bg=self.background)
        self.label2_1.pack(side="left")
        self.entry2_1 = Entry(self.frame2)
        self.entry2_1.pack(side="left")
        self.label2_2 = Label(self.frame2, text="New WBTS ID", font='Aril 9 bold', anchor="e", width=11, bg=self.background)
        self.label2_2.pack(side="left")
        self.entry2_2 = Entry(self.frame2)
        self.entry2_2.pack(side="left")
        # ----
        self.frame3 = Frame(self.mainFrame)
        self.frame3.pack(side="top", fill="x", padx = (5,5), pady = (5,0))
        self.label3 = Label(self.frame3, text="Old RNC ID", anchor="e", width=11 , bg=self.background)
        self.label3.pack(side="left")
        self.entry3 = Entry(self.frame3)
        self.entry3.pack(side="left")
        # ----
        self.file = ttk.Button(self.mainFrame, text="Insert File and Replace", command = self.read_input)
        self.file.pack(side = "top", fill="x", padx = (5,5), pady = (5,0), ipady=5)
        # ----
        self.label5 = Label(self.mainFrame, text="", font='Aril 9 bold', width=11, bg=self.background)
        self.label5.pack(side="top", fill="x", padx = (5,5), pady = (5,0))
        
    def read_input(self):
        self.label5.configure(text="")
        self.inputFile = filedialog.askopenfilename(initialdir='/', filetypes = (('File', '*.xml'), ('All files', '*.xml')))
        self.replace()
        
    def replace(self):
        self.clear_var()
        #---------------------------
        #self.oldSiteName += self.entry1.get()+"<"
        self.oldWbtsId += self.entry2_1.get()
        self.oldRncId += self.entry3.get()
        self.newWbtsId += self.entry2_2.get()

        #---------------------------
        if(self.inputFile==""):
            self.label5.configure(text="Input file not found", font='Aril 9 bold', foreground="red")
            return
        #---------------------------
        if(self.oldWbtsId != "WBTS-" and self.oldRncId == "RNC-"):
            self.label5.configure(text="Old RNC Id can not be empty", font='Aril 9 bold', foreground="red")
            return
        #---------------------------
        if(self.oldWbtsId == "WBTS-" and self.oldRncId != "RNC-"):
            self.label5.configure(text="Old WBTS Id can not be empty", font='Aril 9 bold', foreground="red")
            return
        #---------------------------
        if(self.oldWbtsId != "WBTS-" and self.oldRncId != "RNC-" and self.newWbtsId == "WBTS-" ):
            self.label5.configure(text="New WBTS Id can not be empty", font='Aril 9 bold', foreground="red")
            return

        
        self.label5.configure(text="")
        
        for i in range(len(self.inputFile)-1, 0, -1):
            if(self.inputFile[i] == '/' or self.inputFile[i] == '\\'):
                break
            self.outputFile += self.inputFile[i]
            self.dir = self.inputFile[:i]
        self.outputFile = self.outputFile[::-1]
        self.outputFile = "New_"+self.outputFile

        if os.path.exists(self.dir+self.outputFile):
              os.remove(self.dir+self.outputFile)
        f_out = open(self.dir+self.outputFile, "a")           
        with open(self.inputFile, 'r', encoding='utf_8', errors='ignore') as file:
            f = file.readlines()
            for line in f:
                if((self.oldWbtsId+'"' in line or self.oldWbtsId+'/' in line) and self.oldRncId+"/" in line and "WCEL-" in line):
                    oldWcel = self.oldWbtsId.replace("WBTS-","")
                    newWcell = self.newWbtsId.replace("WBTS-","")
                    line = line.replace(oldWcel, newWcell)
                if(self.oldWbtsId+"/" in line and self.oldRncId+"/" in line):
                    line = line.replace(self.oldWbtsId, self.newWbtsId)
                if(self.oldWbtsId+'"' in line and self.oldRncId+"/" in line):
                    line = line.replace(self.oldWbtsId, self.newWbtsId)
                if('<p name="AdjwCId">' in line):
                    oldWcel = self.oldWbtsId.replace("WBTS-","")
                    newWcell = self.newWbtsId.replace("WBTS-","")
                    line = line.replace(oldWcel, newWcell)
                if('<p name="AdjiCI">' in line):
                    oldWcel = self.oldWbtsId.replace("WBTS-","")
                    newWcell = self.newWbtsId.replace("WBTS-","")
                    line = line.replace(oldWcel, newWcell)
                if('<p name="AdjsCI">' in line):
                    oldWcel = self.oldWbtsId.replace("WBTS-","")
                    newWcell = self.newWbtsId.replace("WBTS-","")
                    line = line.replace(oldWcel, newWcell) 
                if('<p name="sac">' in line):
                    oldWcel = self.oldWbtsId.replace("WBTS-","")
                    newWcell = self.newWbtsId.replace("WBTS-","")
                    line = line.replace(oldWcel, newWcell)  
                if('<p name="CId">' in line):
                    oldWcel = self.oldWbtsId.replace("WBTS-","")
                    newWcell = self.newWbtsId.replace("WBTS-","")
                    line = line.replace(oldWcel, newWcell)  
                if('<p name="IPNBId">' in line):
                    oldWcel = self.oldWbtsId.replace("WBTS-","")
                    newWcell = self.newWbtsId.replace("WBTS-","")
                    line = line.replace(oldWcel, newWcell)
                if('<p name="name">' in line):
                    oldWcel = self.oldWbtsId.replace("WBTS-","")
                    oldWcel = oldWcel.zfill(4)
                    newWcell = self.newWbtsId.replace("WBTS-","")
                    newWcell = newWcell.zfill(4)
                    line = line.replace(oldWcel, newWcell)
                    
                f_out.write(line)
                    
        f_out.close()
        self.label5.configure(text="Output file generated", font='Aril 9 bold', foreground="blue")






    def clear_var(self):
        self.outputFile = ""
        self.dir = ""
        self.oldSiteName = "'WBTSName'>"
        self.oldWbtsId = "WBTS-"
        self.oldRncId = "RNC-"
        self.newWbtsId = "WBTS-"





        
    
    def closeFrame(self):
        try:
            self.mainFrame.destroy()
        except Exception as e:
            print(e)
            pass
