from tkinter import *
#from tkinter import ttk
#from tkinter import filedialog
from Lib import Dx200_BSC

   
class Fallback_2G(Frame):
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
        
        self.main_page()

    def main_page(self, event=None):
        self.frame1 = Frame(self.mainFrame)
        self.frame1.pack(side="top" , fill="x", padx=(5,5), pady=(5,0))
        self.frame1.configure(background = self.background)
        
        self.Button1 = ttk.Button(self.frame1, text="Dump")
        self.Button1.bind("<ButtonRelease-1>", self.write_dump)
        self.Button1.pack(side="left", ipadx=5)
   
        self.Button2 = ttk.Button(self.frame1, text="Fallback")
        self.Button2.bind("<ButtonRelease-1>", self.fallback_script)
        self.Button2.pack(side="left", ipadx=5)
        # ---        
        self.frame3 = ttk.Frame(self.mainFrame)
        self.frame3.pack(side="bottom", fill="x", padx=(5,5), pady=(5,0))
        
        self.btn_read = ttk.Button(self.frame3, text="Read Dump")
        self.btn_read.config(state="enable")
        self.btn_read.bind("<ButtonRelease-1>", self.read_dump)
        self.btn_read.pack(side="left", fill="x", expand=True, anchor=W, ipady=5)
        
        self.btn_reset = ttk.Button(self.frame3, text="Reset")
        self.btn_reset.bind("<ButtonRelease-1>", self.clear_var)
        self.btn_reset.pack(side="left", fill="x", expand=True, anchor=W, ipady=5)
        # ---
 
        self.frame2 = ttk.Frame(self.mainFrame)
        self.frame2.pack(side="top", fill="both", expand=True, padx=(5,5), pady=(0,0))
        yscrollbar = ttk.Scrollbar(self.frame2)
        yscrollbar.pack(side=RIGHT, fill=Y)
        self.textBox = Text(self.frame2, wrap=NONE, yscrollcommand=yscrollbar.set)
        self.textBox.pack(side="top", fill="both", expand=True)
        yscrollbar.config(command=self.textBox.yview)
        self.write_dump()

    def write_dump(self, event=None):
        ''' if already insert a dump, when press dump tap this functions will show the data inserted '''
        self.textBox.delete(1.0,END)
        self.textBox.insert(END, self.dump)
        self.btn_read.config(state="enable")
        self.btn_read.bind("<ButtonRelease-1>", self.read_dump)
        self.btn_reset.config(state="enable")
        self.btn_reset.bind("<ButtonRelease-1>", self.clear_var)
    
    def clear_var(self, event):
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
#       Read Dump
#--------------------------------------------------------------------------------------------------------------------------------------    
    def read_dump(self, event):
        self.dump = self.textBox.get("1.0",END)
        if self.dump == '':
            return
        self.dx200 = Dx200_BSC.Mml_Command()
        self.data_ZEEI = self.dx200.ZEEI(self.dump)
        self.data_ZDTI = self.dx200.ZDTI(self.dump)
        self.data_ZEQO = self.dx200.ZEQO(self.dump)
        self.data_ZDSB = self.dx200.ZDSB(self.dump)
        self.data_ZERO = self.dx200.ZERO(self.dump)
        self.data_ZEAO = self.dx200.ZEAO(self.dump)
        
        return()

#--------------------------------------------------------------------------------------------------------------------------------------
#       Create Scripts
#--------------------------------------------------------------------------------------------------------------------------------------
    def fallback_script(self, event):
        self.textBox.delete(1.0,END);
        self.btn_read.config(state="disable")
        self.btn_read.unbind("<ButtonRelease-1>")
        self.btn_reset.config(state="disable")        
        if len(self.dump) < 1:
            return
        self.textBox.insert(END,"CREATE OMU:\n");
        self.textBox.insert(END,self.dx200.create_OMU())
        self.create_OMU()
        self.create_LAPD()
        self.create_BCF()
        self.create_BTS()
        self.create_TRX()
        self.create_ADJS()
        self.configure_BTS()


    def create_OMU(self):         
        self.textBox.insert(END,"CREATE OMU:\n");
        for row in self.data_ZEEI:
            bscType, bcfModel, bscName, omuName, omuId, bcfType, bcfId, bcf_sig, lac, ci, btsId, btsName, trxName, trxID, trx_freq, trx_pcm, trx_channel, trx_pref, trx_sig = row
            break
        for row in self.data_ZDSB:
            if len(row) == 13:
                name, num, sapi, tei, br, pcm_tsl_tsl, c_m, unit, term, term_func, log_term, pcm_tsl, par_set = row
            elif len(row) == 12:
                name, num, sapi, tei, br, pcm_tsl_tsl, unit, term, term_func, log_term, pcm_tsl, par_set = row
            else:
                self.textBox.delete(1.0,END);
                self.textBox.insert(END,"Erro a ler ZDSB. Verificar nº de elementos na linha")
                return
            if (name == omuName):
                break
            
        unit_type = ''    
        for c in unit:
            try:
                unit_index = int(c)
            except Exception:
                unit_type += c
        unit_type = unit_type[:-1]

        index = 0 # esta variavel vai guardar a posição do ultimo "-"
        n = 0     # n é a posição do caracter que estou a ler 
        for c in pcm_tsl_tsl:
            try:
                num = int(c)
            except Exception:
                index = n
            n += 1
        pcm_tls = pcm_tsl_tsl[:index]
        tls = pcm_tsl_tsl[index+1:]
        
        self.textBox.insert(END,'ZDSE:'+str(omuName)+':'+str(unit_type)+','+str(unit_index)+':'+str(sapi)+','+str(tei)+':'+str(br)+','+str(pcm_tls)+','+str(tls)+':N,'+str(par_set)+';\n\n');
        pass

    def create_LAPD(self):
        self.textBox.insert(END,'CREATE LAPD´s\n');
        for row in self.data_ZEEI:
            bscType, bcfModel, bscName, omuName, omuId, bcfType, bcfId, bcf_sig, lac, ci, btsId, btsName, trxName, trxID, trx_freq, trx_pcm, trx_channel, trx_pref, trx_sig = row
            break
        for row in self.data_ZDSB:
            if len(row) == 13:
                name, num, sapi, tei, br, pcm_tsl_tsl, c_m, unit, term, term_func, log_term, pcm_tsl, par_set = row
            elif len(row) == 12:
                name, num, sapi, tei, br, pcm_tsl_tsl, unit, term, term_func, log_term, pcm_tsl, par_set = row
            else:
                self.textBox.delete(1.0,END);
                self.textBox.insert(END,"Erro a ler ZDSB. Verificar nº de elementos na linha")
                return
            if (name == omuName): # lapd da omu já foi criado anteriormente
                continue
            
            unit_type = ''    
            for c in unit:
                try:
                    unit_index = int(c)
                except Exception:
                    unit_type += c
            unit_type = unit_type[:-1]

            index = 0 # esta variavel vai guardar a posição do ultimo "-"
            n = 0     # n é a posição do caracter que estou a ler 
            for c in pcm_tsl_tsl:
                try:
                    num = int(c)
                except Exception:
                    index = n
                n += 1
            pcm_tls = pcm_tsl_tsl[:index]
            tls = pcm_tsl_tsl[index+1:]
            
            self.textBox.insert(END,'ZDSE:'+str(name)+':'+str(unit_type)+','+str(unit_index)+':'+str(sapi)+','+str(tei)+':'+str(br)+','+str(pcm_tls)+','+str(tls)+':N,'+str(par_set)+';\n');

    def create_BCF(self):
        self.textBox.insert(END,'\nCREATE BCF\n');
        for row in self.data_ZEEI:
            bscType, bcfModel, bscName, omuName, omuId, bcfType, bcfId, bcf_sig, lac, ci, btsId, btsName, trxName, trxID, trx_freq, trx_pcm, trx_channel, trx_pref, trx_sig = row
            break
        self.textBox.insert(END,'ZEFC:'+str(bcfId)+','+str(bcfModel)+':DNAME='+str(omuName)+';\n');

    def create_BTS(self):
        self.textBox.insert(END,'\nCREATE BTS\n');
        for row in self.data_ZEQO:
            bcf, bts, seg, name, ci, band, ncc, bcc, mcc, mnc, lac, hop, uhop, mal, hsn1, hsn2, plmn, dr, hys, rxp, cb,trp, rdiv, frl, fru, pi, reo, teo, pet, mo, ms, rac, cded, cdef, cmax = row
            self.textBox.insert(END,'ZEQC:BCF={},BTS={},NAME={},:CI={},BAND={}:NCC={},BCC={}:MCC={},MNC={},LAC={}:HOP={},HSN1={};\n'.format(
                                        bcf, bts, name, ci, band, ncc, bcc, mcc, mnc, lac, hop, hsn1))
            
    def create_TRX(self):
        self.textBox.insert(END,'\nCREATE TRX´s\n');
        for row in self.data_ZERO:
            bts, trx, gtrx, pref, freq, tsc, dap, sign, lapd, pcm, tsl, channel = row
            self.textBox.insert(END,'ZERC:BTS={},TRX={}:PREF={},DAP={},GTRX={}:FREQ={},TSC={},PCMTSL={}-{}:DNAME={}:SIGN={},CH0={},CH1={},CH2={},CH3={},CH4={},CH5={},CH6={},CH7={}:;\n'.format(
                                        bts, trx, pref, dap, gtrx, freq, tsc, pcm, tsl, lapd, sign, channel[0], channel[1], channel[2], channel[3], channel[4], channel[5], channel[6], channel[7]))
       

    def create_ADJS(self):   
        self.textBox.insert(END,'\nCREATE ADJs´s\n');
        for row in self.data_ZEAO:
            bts, name, mcc, mnc, lac, ci, ncc, bcc, freq, pmrg, lmrg, qmrg, pri, sl, aucl, sync, drt, agena, rac = row
            self.textBox.insert(END,'ZEAC:BTS={}::CI={},LAC={},MCC={},MNC={}:BCC={},NCC={},FREQ={}:LMRG={},QMRG={},PMRG={},RAC={},SYNC={},AUCL={},SL={},AGENA={},DRT={},PRI={};\n'.format(
                                        bts, ci, lac, mcc, mnc, bcc, ncc, freq, lmrg, qmrg, pmrg, rac, sync, aucl, sl, agena, drt, pri))
        

    def configure_BTS(self):
        self.textBox.insert(END,'\nCONFIGURE BTS\n');
        for row in self.data_ZEQO:
            bcf, bts, seg, name, ci, band, ncc, bcc, mcc, mnc, lac, hop, uhop, mal, hsn1, hsn2, plmn, dr, hys, rxp, cb,trp, rdiv, frl, fru, pi, reo, teo, pet, mo, ms, rac, cded, cdef, cmax = row
            self.textBox.insert(END,'ZEQV:BTS={}:EGENA=N,GENA=N;\n'.format(bts))
            self.textBox.insert(END,'ZEQA:BTS={}:MO={},MS={},MAL={};\n'.format(bts, mo, ms, mal))
            self.textBox.insert(END,'ZEQM:BTS={}:RDIV={},CB={},TRP={};\n'.format(bts, rdiv, cb, trp))
            plmn = list(plmn)
            self.textBox.insert(END,'ZEQF:BTS={}:DR={},PLMN={}&&{};\n'.format(bts, dr, plmn[0], plmn[-1]))
            self.textBox.insert(END,'ZEQM:BTS={}:FRL={},FRU={},;\n'.format(bts, frl, fru))
            self.textBox.insert(END,'ZEQM:BTS={}:::PI={},PET={},REO={},TEO={};\n'.format(bts, pi, pet, reo, teo))
            self.textBox.insert(END,'ZEQG:BTS={}:RXP={},HYS={};\n'.format(bts, rxp, hys))
            self.textBox.insert(END,'ZEQV:BTS={}:CDED={},CDEF={},CMAX={},RAC={};\n'.format(bts, cded, cdef, cmax, rac))
            self.textBox.insert(END,'ZEQV:BTS={}:EGENA=Y,GENA=Y;\n'.format(bts))






    
