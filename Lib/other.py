#!/usr/bin/python3.6
encoding='utf_8'
from tkinter import *
import sqlite3
import os 


class CompareFile(Frame):
    background = 'SystemButtonFace'
    
    def __init__(self, mainFrame):
        Frame.__init__(self, mainFrame)
        self.mainFrame = mainFrame
        self.f1 = ""
        self.f2 = ""
            
        self.gui_frame()
            
    def gui_frame(self):
        self.frame1 = Frame(self.mainFrame, bg=self.background)
        self.frame1.pack(side = "top" , fill="x")
        self.lb_file1 = Label(self.frame1, text="File 1:")
        self.lb_file1.config(bg=self.background)
        self.lb_file1.pack(side = "left", padx = (5,0), pady = (5,0))
        
        self.entry_file1 = Entry(self.frame1, bg=self.background)
        self.entry_file1.pack(side = "left", fill="x", expand=True, padx = (5,0), pady = (5,0))
        self.entry_file1.config(state="disable")
        
        self.btn_file1 = ttk.Button(self.frame1, text="Load", command= self.file_one)
        self.btn_file1.pack(side = "left", padx = (5,5), ipadx = 5, pady = (5,0))

        self.frame2 = Frame(self.mainFrame, bg=self.background)
        self.frame2.pack(side = "top" , fill="x")
        self.lb_file2 = Label(self.frame2, text="File 2:")
        self.lb_file2.config(bg=self.background)
        self.lb_file2.pack(side = "left" , padx = (5,0), pady = (5,0))
        
        self.entry_file2 = Entry(self.frame2)
        self.entry_file2.pack(side = "left", fill="x", expand=True, padx = (5,0), pady = (5,0))
        self.entry_file2.config(state="disable")
        
        self.btn_file2 = ttk.Button(self.frame2, text="Load", command= self.file_two)
        self.btn_file2.pack(side = "left", padx = (5,5), ipadx = 5, pady = (5,0))

        self.textBox = Text(self.mainFrame)
        self.textBox.pack(side = "top" , fill="both", expand=True, padx = (5,5), pady = (5,0))
        
        self.btn_compare = ttk.Button(self.mainFrame, text="Compare", command = self.compare_file)
        self.btn_compare.pack(side="bottom", fill="x", padx = (5,5), pady = (5,0), ipady = 10)

    def callback(self, event):
        print(os.path.dirname(os.path.abspath(event)))
            
    def file_one(self):
        self.f1 = filedialog.askopenfilename(initialdir='/', filetypes = (('File', '*.*'), ('All files', '*.*')))
        self.entry_file1.config(state="normal")
        self.entry_file1.insert(0, self.f1)
        self.entry_file1.config(state="disable")

    def file_two(self):
        self.f2 = filedialog.askopenfilename(initialdir='/', filetypes = (('File', '*.*'), ('All files', '*.*')))
        self.entry_file2.config(state="normal")
        self.entry_file2.insert(0, self.f2)
        self.entry_file2.config(state="disable")

    def compare_file(self):
        if self.f1=="" or self.f2=="":
            self.textBox.insert(END,"Check Files\n")
            return
            
        self.textBox.delete(1.0,END)
        try:
            with open(self.f1, 'r', encoding='ascii', errors='ignore') as file1:
                f1 = file1.readlines()
        except Exception as e:
            self.textBox.insert(END,"File 1:\n{}\n".format(e))

        try:
            with open(self.f2, 'r', encoding='ascii', errors='ignore') as file2:
                f2 = file2.readlines()
        except Exception as e:
            self.textBox.insert(END,"File 2:\n{}\n".format(e))
 
        l1 = 0
        iqual = True
        for line1 in f1:
            #print(line1)
            l1 += 1
            l2 = 0
            for line2 in f2:
                l2 += 1
                if l1 == l2:
                    if not line1 == line2:
                        iqual = False
                        self.textBox.insert(END,"Differences in line: {}\n".format(l1))
                    break    
        if iqual:
            self.textBox.insert(END,"Files are iquals\n")
            

    def closeFrame(self):
        try:
            self.mainFrame.destroy()
        except Exception as e:
            print(e)
            pass
#-------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------
class MMLcmd(Frame):
    background = 'SystemButtonFace'
    
    def __init__(self, mainFrame):
        Frame.__init__(self, mainFrame)
        self.mainFrame = mainFrame
        self.file = path = os.getcwd() + "\File\MML_CMD.txt";
        print(self.file)
        self.gui_frame()
            
    def gui_frame(self):
        self.frame1 = Frame(self.mainFrame, bg=self.background)
        self.frame1.pack(side = "top" , fill="x")
        self.lb_search = Label(self.frame1, text="Search")
        self.lb_search.config(bg=self.background)
        self.lb_search.pack(side = "left", padx = (5,0), pady = (5,0))
        
        self.entry_search = Entry(self.frame1)
        self.entry_search.pack(side = "left", fill="x", expand=True, padx = (5,0), pady = (5,0))
        self.entry_search.bind("<Return>", self.search)

        self.btn_showAll = ttk.Button(self.frame1, text="All")
        self.btn_showAll.pack(side = "right", padx = (0,5), ipadx = 5, pady = (5,0))
        self.btn_showAll.bind("<ButtonRelease-1>", self.show_all)
        
        self.btn_search = ttk.Button(self.frame1, text="Search")
        self.btn_search.pack(side = "right", padx = (5,0), ipadx = 5, pady = (5,0))
        self.btn_search.bind("<ButtonRelease-1>", self.search)
        
        
        self.textFrame = Frame(self.mainFrame, bg=self.background)
        self.textFrame.pack(side="top" , fill="both", expand=True, padx = (5,5), pady = (5,0))
        yscrollbar = ttk.Scrollbar(self.textFrame)
        yscrollbar.pack(side="right", fill="y")         
        self.textBox = Text(self.textFrame, wrap=NONE, yscrollcommand=yscrollbar.set)
        self.textBox.pack(side = "top" , fill="both", expand=True)
        yscrollbar.config(command=self.textBox.yview)
        
    def search(self, event):
        self.textBox.delete(1.0,END)
        searhItem = self.entry_search.get().upper()
        self.textBox.tag_config('header', foreground="blue",font="bold")
        with open(self.file, 'r', encoding='utf_8', errors='ignore') as file:
            f = file.readlines()
            cmd_detect = False
            for line in f:
                if "<" in line and searhItem in line:
                    self.textBox.insert(END, line, "header")
                    cmd_detect = True
                    continue
                if cmd_detect and not "<END>" in line:
                    self.textBox.insert(END,line)
                    continue
                if cmd_detect and "<END>" in line:
                    self.textBox.insert(END,"\n")
                    cmd_detect = False
                    continue
            file.close()

    def show_all(self, event):
        self.textBox.delete(1.0,END)
        self.textBox.tag_config('header', foreground="blue",font="bold")
        with open(self.file, 'r', encoding='utf_8', errors='ignore') as file:
            f = file.readlines()
            for line in f:
                if "<" in line and not "<END>" in line:
                    self.textBox.insert(END, line, "header")
                    cmd_detect = True
                    continue
                if cmd_detect and not "<END>" in line:
                    self.textBox.insert(END,line)
                    continue                
                if "<END>" in line:
                    self.textBox.insert(END,"\n")
                    cmd_detect = False
                    continue
            file.close()
            
    
    def closeFrame(self):
        try:
            self.mainFrame.destroy()
        except Exception as e:
            print(e)
            pass

#-------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------
class Radio_Modules(Frame):
    background = 'SystemButtonFace'
    table_name = 'Radio_Module'
    path = os.getcwd()
    database = path+'\\db\\DataBase.db'
    def __init__(self, mainFrame):
        Frame.__init__(self, mainFrame)
        self.mainFrame = mainFrame
        
        self.gui_frame()
        self.conn_DB()
        self.show_data()
        
    def gui_frame(self):
        self.frame1 = Frame(self.mainFrame, bg=self.background)
        self.frame1.pack(side = "top" , fill="x")
        self.lb_search = Label(self.frame1, text="Radio Name:")
        self.lb_search.config(bg=self.background)
        self.lb_search.pack(side = "left", padx = (5,0), pady = (5,0))
        
        self.entry_search = Entry(self.frame1)
        self.entry_search.pack(side = "left", padx = (5,0), pady = (5,0))
        self.entry_search.bind("<Return>", self.search)

        self.btn_showAll = ttk.Button(self.frame1, text="Search")
        self.btn_showAll.pack(side = "left", padx = (5,0), ipadx = 5, pady = (5,0))
        self.btn_showAll.bind("<ButtonRelease-1>", self.search)
        
        self.btn_search = ttk.Button(self.frame1, text="BataBase")
        self.btn_search.pack(side = "left", padx = (5,0), ipadx = 5, pady = (5,0))
        self.btn_search.bind("<ButtonRelease-1>", self.search_all)
        
        
        self.tableFrame = Frame(self.mainFrame, bg=self.background)
        self.tableFrame.pack(side="top" , fill="both", expand=True, padx = (5,5), pady = (5,0))
        
        yscrollbar = ttk.Scrollbar(self.tableFrame)
        yscrollbar.pack(side="right", fill="y", pady=(0,15))
        xscrollbar = ttk.Scrollbar(self.tableFrame, orient="horizontal")
        xscrollbar.pack(side="bottom", fill="x")        
        self.table = Text(self.tableFrame, wrap=NONE, xscrollcommand=xscrollbar.set, yscrollcommand=yscrollbar.set)
        self.table.pack(side="top", fill=BOTH, expand=True)
        yscrollbar.config(command=self.table.yview)
        xscrollbar.config(command=self.table.xview)
        

    def conn_DB(self):
        self.labels = ""
        # connect to Database
        try:
            self.connection = sqlite3.connect(self.database)
        except Exception as e:
            self.table.insert(END,"{}\n".format(e))
            return()
        # load table data
        self.cursor = self.connection.execute('SELECT * FROM {}'.format(self.table_name))
        self.column_names = [description[0] for description in self.cursor.description]
        for label in self.column_names:
            self.labels+=str(label)+"\t\t"

            
    def search(self, event=None):
        searchItem = ''
        search_key = self.entry_search.get()
        col_sel = 'NAME'
        
        for column in self.column_names:
            if search_key == "":
                break
            if col_sel != "" and search_key != "":
                searchItem = '{} LIKE "%{}%"'.format(col_sel, search_key)
                break
            if searchItem != "":
                searchItem += " OR "
            searchItem += '{} = "{}"'.format(column, search_key)
        
        if not searchItem:
            ''' enter key without search, load all data '''
            self.cursor = self.connection.execute('SELECT * FROM {}'.format(self.table_name))
            self.show_data()
            return
        
        self.cursor = self.connection.execute('SELECT * FROM {} WHERE {}'.format(self.table_name, searchItem))
        self.show_data()
        return 

    def search_all(self, event):
        self.cursor = self.connection.execute('SELECT * FROM {}'.format(self.table_name))
        self.show_data()
        
    def show_data(self, event=None):
        # clear box
        self.table.delete(0.0,END)
        
        bdData = self.cursor
         
        # inserir nome das colunas
        labels = self.labels.split()
        for i in range (1,len(labels)):
            if i == 1 or i == 2 or i == 3:
                self.table.insert(END, labels[i]+"\t")
                continue
            if i == 4:
                self.table.insert(END, labels[i]+"\t\t")
                continue
            self.table.insert(END, labels[i]+"\t\t\t")
        self.table.insert(END, "\n")
        
        # inserir --- por baixo do nome das colunas
        for label in range (1,len(labels)):
            for c in labels[label]:
                self.table.insert(END, "-")
            if label == 1 or label == 2 or label == 3:
                self.table.insert(END, "\t")
                continue
            if label == 4:
                self.table.insert(END, "\t\t")
                continue
            self.table.insert(END, "\t\t\t")
        self.table.insert(END, "\n")    

        # inserir dados 
        line = 3
        self.table.tag_add("here", "1.0", "1.end")
        self.table.tag_config("here", background="lightGrey")
        self.table.tag_add("here", "2.0", "2.end")
        self.table.tag_config("here", background="lightGrey")
        
        for data_row in bdData:
            column = 0
            for data_col in data_row:
                if column != 0:
                    if column == 1 or column == 2 or column == 3:
                        self.table.insert(END, str(data_col)+"\t")
                    elif column == 4:
                        self.table.insert(END, str(data_col)+"\t\t")
                    else:
                        self.table.insert(END, str(data_col)+"\t\t\t")
                column += 1
            #colocar cor de fundo nas linhas pares
            if(line % 2) == 0:
                self.table.tag_add("here", ""+str(line)+".0", str(line)+".end")
                self.table.tag_config("here", background="lightGrey")
  
            self.table.insert(END, "\n")
            line+=1


    def closeFrame(self):
        try:
            self.mainFrame.destroy()
        except Exception:
            pass

        try:
            self.connection.close()
        except Exception:
            pass


