#!/usr/bin/python3.6
from tkinter import *
import sqlite3
import os 

class LoadDatabase():
     #class created to see ConnDatabase that have been previously inputted#
    def __init__(self, tableFrame, connection, table_name): 
        self.mainFrame = tableFrame
        self.connection = connection
        self.table_name = table_name
        self.labels = ""
        
        self.cursor = self.connection.execute('SELECT * FROM {}'.format(self.table_name))
        self.column_names = [description[0] for description in self.cursor.description]
        for label in self.column_names:
            self.labels+=str(label)+"\t\t"
        
        self.create_label()
        self.show_data()
        
    def create_label(self):
        self.searchFrame = Frame(self.mainFrame)
        self.searchFrame.pack(side="top", fill="x", pady=(0,5))
        
        col_names = StringVar()
        self.colNamecCombo = ttk.Combobox(self.searchFrame, value=col_names, width=24)
        col_names = self.column_names
        #col_names[0] = ""
        self.colNamecCombo['value'] = col_names
        self.colNamecCombo.current(5)
        self.colNamecCombo.bind("<<ComboboxSelected>>", self.search_data_from_table)
        self.colNamecCombo.pack(side="left", padx=(5,0), ipady=2)
        
        self.filterEntry = ttk.Entry(self.searchFrame, justify = "left", width=18)
        self.filterEntry.pack(side="left", anchor="nw", padx=(5,0), ipady=2)
        self.filterEntry.bind("<Return>", self.search_data_from_table)
        self.filterButton = ttk.Button(self.searchFrame, text="Search", command=self.search_data_from_table)
        self.filterButton.pack(side="left", anchor="nw", padx=(6,0), ipadx=9)
            
        self.tableFrame = Frame(self.mainFrame)
        self.tableFrame.pack(side="top", fill="both", expand=True, padx=(5,5))
        
        yscrollbar = ttk.Scrollbar(self.tableFrame, orient="vertical")
        yscrollbar.pack(side="right", fill="y", pady=(0,15))
        xscrollbar = ttk.Scrollbar(self.tableFrame, orient="horizontal")
        xscrollbar.pack(side="bottom", fill="x")
        self.table = Text(self.tableFrame, wrap=NONE, xscrollcommand=xscrollbar.set, yscrollcommand=yscrollbar.set)
        self.table.pack(side="top", fill=BOTH, expand=True)
        yscrollbar.config(command=self.table.yview)
        xscrollbar.config(command=self.table.xview)
        

    def show_data(self):
        # load table data
        bdData = self.cursor
        
        # clear box
        self.table.delete(1.0,END)
        
        # inserir nome das colunas
        labels = self.labels.split()
        for i in range (1,len(labels)):
            if i == 1 or i == 2 or i == 3 or i == 4 or i == 5:
                self.table.insert(END, labels[i]+"\t\t")
                continue
            self.table.insert(END, labels[i]+"\t\t\t")
        self.table.insert(END, "\n")
        
        # inserir --- por baixo do nome das colunas
        for label in range (1,len(labels)):
            for c in labels[label]:
                self.table.insert(END, "-")
            if label == 1 or label == 2 or label == 3 or label == 4 or label == 5:
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
                    if column == 1 or column == 2 or column == 3 or column == 4 or column == 5:
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

    def search_data_from_table(self, event=None):
        searchItem = ''
        search_key = self.filterEntry.get()
        col_sel = self.colNamecCombo.get()
        
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



class Database(Frame):
    path = os.getcwd()
    database = path+'\\db\\DataBase.db'
    
    def __init__(self, root):
        Frame.__init__(self, root)
        self.root = root
        self.database_page()
        
    def database_page(self):
        self.mainFrame = Frame(self.root)
        self.mainFrame.pack(side="top", fill="both", expand=True)

        self.optionFrame = Frame(self.mainFrame)
        self.optionFrame.pack(side="top", fill="x", padx=(0,0))
        
        self.clientFrame = ttk.Frame(self.optionFrame)
        self.clientFrame = LabelFrame(self.optionFrame, text="Client")
        self.clientFrame.pack(side="left", padx=(5,0))
        
        self.client = IntVar(self.mainFrame)
        self.client.set(1)
        labels = [("OI"   , 1),
                  ("CLARO", 2),
                  ("TIM"  , 3)]
        for (label, value) in labels:
            checkbutton = Checkbutton(self.clientFrame, text=label, variable=self.client, onvalue = value)
            checkbutton.pack( side="left", anchor="center", fill="x")
            checkbutton.configure(state=NORMAL)

        self.controllerFrame = Frame(self.optionFrame)
        self.controllerFrame = LabelFrame(self.optionFrame, text="Controller")
        self.controllerFrame.pack(side="left", padx=(5,5))
        
        self.controller = IntVar(self.mainFrame)
        self.controller.set(1)
        labels = [("BSC", 1),
                  ("RNC", 2)]
        for (label, value) in labels:
            checkbutton = Checkbutton(self.controllerFrame, text=label, variable=self.controller, onvalue = value)
            checkbutton.pack( side="left", anchor="center", fill="x", ipadx=2)
            checkbutton.configure(state=NORMAL)
        
        self.loadBT = ttk.Button(self.optionFrame, text="Load", command=self.select_table_from_bd)
        self.loadBT.pack(side="left", ipadx=9, ipady=7, pady=(7,0))


        self.tableFrame = Frame(self.mainFrame)
        self.tableFrame.pack(side="top", fill="both", expand=True, pady=(5,5))

        # connect to Database
        try:
            self.path = os.getcwd()
            self.connection = sqlite3.connect(self.database)
        except Exception:
            print("Erro abrir DB")
            return()
        
        return()


    def select_table_from_bd(self):
        if(self.client.get()==1):
            if self.controller.get()==1:
                table_name = "tb_oi_bsc"
            if self.controller.get()==2:
                table_name = "tb_oi_rnc"
        elif(self.client.get()==2):
            if self.controller.get()==1:
                table_name = "tb_claro_bsc"
            if self.controller.get()==2:
                table_name = "tb_claro_rnc"
        elif(self.client.get()==3):
            if self.controller.get()==1:
                table_name = "tb_tim_bsc"
            if self.controller.get()==2:
                table_name = "tb_tim_rnc"
                
        # if not the first load table, than first delete all data and show new data        
        try:
            self.tableFrame.destroy()
        except Exception:
            pass
        self.tableFrame = Frame(self.mainFrame)
        self.tableFrame.pack(side="top", fill="both", expand=True)
        
        self.dbTable = LoadDatabase(self.tableFrame, self.connection, table_name)

            

    def closeFrame(self):
        
        try:
            self.root.destroy()
            self.connection.close()
        except Exception:
            pass
        
