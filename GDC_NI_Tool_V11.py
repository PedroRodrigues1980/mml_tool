#!/usr/bin/python3.6
encoding='utf_8'
import sys #, traceback
import os
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from ttkthemes import themed_tk as tk
import datetime

from Lib import dump_2G
from Lib import fallback_2G
from Lib import report_2G
from Lib import integration_2G
from Lib import database
from Lib import sshShell
from Lib import other
from Lib import rotas_3G
from Lib import replace_3G_parameters

class MainWindow():
    date = datetime.datetime.now()
    licence = 2021;
    def __init__(self, root, background):
        self.root = root;
        self.background = background;
        self.root.title("GDC NI TOOL")
        
        self.mainHeight = 350 # width for the Tk root
        self.mainWidth = 600 # height for the Tk root
        # get screen width and height
        #self.mainHeightScreen = self.root.winfo_screenheight() # width of the screen
        #self.mainWidthScreen = self.root.winfo_screenwidth() # height of the screen
        # calculate x and y coordinates for the Tk root window
        #x = (self.mainHeightScreen/2) - (self.mainHeight/2)
        #y = (self.mainWidthScreen/2) - (self.mainWidth/2)
        #self.root.geometry('%dx%d+%d+%d' % (self.mainWidth, self.mainHeight, y, x))
        #self.root.geometry('%dx%d+%d+%d' % (self.mainWidth, self.mainHeight, 0, 0))
        self.root.geometry("800x350+0+0")
        self.root.minsize(self.mainWidth, self.mainHeight)

        self.menuBar = Menu(self.root)  # declaracao da barra de menus
        self.menus()                    # contrucao dos menus

        self.build_main_frame()
        self.startPages()
        self.no_licence()
        
    def build_main_frame(self):
        self.mainFrame = Frame(self.root)
        self.mainFrame.pack(fill = BOTH, expand = True)
        self.mainFrame.configure(background = self.background)
        

    def menus(self):
        info = Label(self.root, text="Program developed by Pedro Rodrigues", anchor=W, padx = 5)
        info.pack(side = BOTTOM, fill=X)
        info.configure(background = self.background)
        
        # file menu
        fileMenu = Menu(self.menuBar, tearoff=0)
        fileMenu.add_command(label='---------', command='')
        fileMenu.add_separator()
        fileMenu.add_command(label='Exit', command=lambda: self.root.destroy())
        self.menuBar.add_cascade(label='File', menu=fileMenu)
        
        # 2G Menu
        _2G_Menu = Menu(self.menuBar, tearoff=0)
        _2G_Menu.add_cascade(label='Dump', command=self.dump2GView)
        _2G_Menu.add_cascade(label='Integration', command=self.integration2GView)
        _2G_Menu.add_cascade(label='Fallback', command=self.fallback)
        _2G_Report = Menu(_2G_Menu, tearoff=0)
        _2G_Report.add_cascade(label='2G Report OI', command=self.report_2G_OI)
        _2G_Menu.add_cascade(label='2G_Report', menu=_2G_Report)

        self.menuBar.add_cascade(label='GSM-2G', menu=_2G_Menu)

        # 3G Menu
        _3G_Menu = Menu(self.menuBar, tearoff=0)
        _3G_Menu.add_cascade(label='Rotas', command=self.rotas_3G_view)
        _3G_Menu.add_cascade(label='Remanejamento', command=self.replace_parameters)
        self.menuBar.add_cascade(label='UMTS-3G', menu=_3G_Menu)

        # 4G Menu
        _4G_Menu = Menu(self.menuBar, tearoff=0)
        self.menuBar.add_cascade(label='LTE-4G', menu=_4G_Menu)

        # SSH Button
        ssh = Menu(self.menuBar, tearoff=0)
        #ssh.add_command(label='Program developed by Pedro Rodrigues. \nThis program aims to assist the tasks of the NI GDC,\n however it is the Engineer responsibility to verify that all data generated is correct.\n', command='')
        self.menuBar.add_command(label='SSH Cluster', command=self.sshShellView)

        # dataBase Button
        ssh = Menu(self.menuBar, tearoff=0)
        #ssh.add_command(label='Program developed by Pedro Rodrigues. \nThis program aims to assist the tasks of the NI GDC,\n however it is the Engineer responsibility to verify that all data generated is correct.\n', command='')
        self.menuBar.add_command(label='Database', command=self.dbView)


        # Others
        other = Menu(self.menuBar, tearoff=0)
        other.add_cascade(label='Compare Files', command=self.compare_file)
        other.add_cascade(label='MML Commands', command=self.mml_commands)
        other.add_cascade(label='Radio Modules', command=self.radio_modules)
        self.menuBar.add_cascade(label='Others', menu=other)

        self.root.config(menu=self.menuBar)
        return()

    def startPages(self):
        self.report2G = report_2G.Report_2G(self.root, self.mainFrame, self.background)
        #self.fallback = fallback_2G.Fallback_2G(self.root)

    def sshShellView(self):
        try:
            #print(self.sshPage.active())
            self.sshPage
            if not self.sshPage.active():
                del self.sshPage
                self.sshPage = sshShell.SshShell(self.root)
        except AttributeError:
            self.sshPage = sshShell.SshShell(self.root)        
            return


    def integration2GView(self):
        self.closeFrames()
        try:
            self.integration2G.closeFrame()
            self.integration2G = integration_2G.Integration_2G(self.mainFrame)
        except Exception as e:
            self.integration2G = integration_2G.Integration_2G(self.mainFrame)

    def dump2GView(self):
        self.closeFrames()
        try:
            self.fallback.closeFrame()
            self.fallback = dump_2G.Dump_2G(self.mainFrame)
        except Exception as e:
            self.fallback = dump_2G.Dump_2G(self.mainFrame)
    
    def fallback(self):
        self.closeFrames()
        try:
            self.dump2G.closeFrame()
            self.dump2G = fallback_2G.Fallback_2G(self.mainFrame)
        except Exception as e:
            self.dump2G = fallback_2G.Fallback_2G(self.mainFrame)
               
    def report_2G_OI(self):
        self.closeFrames()
        return()

    def rotas_3G_view(self):
        self.closeFrames()
        try:
            self.rotas3G.closeFrame()
            self.rotas3G = rotas_3G.Rotas3G(self.mainFrame)
        except Exception as e:
            self.rotas3G = rotas_3G.Rotas3G(self.mainFrame)

    def replace_parameters(self):
        self.closeFrames()
        try:
            self.replaceParameters.closeFrame()
            self.replaceParameters = replace_3G_parameters.Replace_3G_Parameters(self.mainFrame)
        except Exception as e:
            self.replaceParameters = replace_3G_parameters.Replace_3G_Parameters(self.mainFrame)    
    
    def dbView(self):
        self.closeFrames()
        try:
            self.db.closeFrame()
            self.db = database.Database(self.mainFrame)
        except Exception as e:
            self.db = database.Database(self.mainFrame)       

    
    def compare_file(self):
        self.closeFrames()
        try:
            self.cnp.closeFrame()
            self.cnp = other.CompareFile(self.mainFrame)
        except Exception as e:
            self.cnp = other.CompareFile(self.mainFrame)

    def mml_commands(self):
        self.closeFrames()
        try:
            self.mmlCmd.closeFrame()
            self.mmlCmd = other.MMLcmd(self.mainFrame)
        except Exception as e:
            self.mmlCmd = other.MMLcmd(self.mainFrame)

    def radio_modules(self):
        self.closeFrames()
        try:
            self.radioModules.closeFrame()
            self.radioModules = other.Radio_Modules(self.mainFrame)
        except Exception as e:
            self.radioModules = other.Radio_Modules(self.mainFrame)        


























        
    def no_licence(self):
        if(self.date.year>self.licence): #, self.date.month, self.date.day
            while True:
                pass
        
    def closeFrames(self):
        self.mainFrame.destroy()
        self.build_main_frame()
        
        self.report2G.closeFrame()
        self.root.update()
        return()        
        

if __name__ == '__main__':      
    # variaveil global
    path = os.getcwd();
    background = 'SystemButtonFace'
    
    root = tk.ThemedTk()
    root.get_themes()
    root.set_theme("winxpblue")
    
    root.iconbitmap(r'{}\\Img\\logo.ico'.format(path))
    app = MainWindow(root,background);

    root.mainloop();
