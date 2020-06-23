#!/usr/bin/python3.6
encoding='utf_8'

class Mml_Command():
    def __init__(self):
        self.ZEEI_Info = []
        self.ZDTI_Info = []
        self.ZEQO_Info = []
        self.ZDSB_Info = []
        self.ZERO_Info = []
        self.ZEAO_Info = []

    def get_value(self, line):
        # para as linhas que têm valores dbm junto ao resto do texto
        line = list(line)
        var = ''
        for c in reversed(line):
            if c == ".":
                break
            if c == " ":
                continue
            var += c
        var = var[::-1]
        return var
        
        
    def ZEEI(self, dump):
        zeei = False
        for line in dump.splitlines():
            if "EEI:BCF=" in line and "RCV" not in line:
                zeei = True
            # read bsc type
            if "BSC" in line[:-len(line)+10] and zeei == True:
                #print(line)
                word = line.split()
                bscType = word[0]
                bscName = word[1]
                #print("BSC TYPE:", bscType," / BSC NAME:", bscName)
                continue
            # read BCF ID,OMU ID and OMU NAME
            if "BCF-" in line and zeei == True:
                #print(line)
                word = line.split()
                bcfId = word[0]
                bcfId = bcfId[4:]
                bcfType = word[1]
                if "MULTI" in word[2] or "EDGE" in word[2] or "MR10" in word[2]:
                    bcfType=bcfType+' '+word[2];
                    
                if(bcfType=="METROSITE"):
                    bcfModel='C';
                elif(bcfType=="ULTRASITE"):
                    bcfModel='P';
                elif(bcfType=="FLEXI EDGE"):
                    bcfModel='E';
                elif(bcfType=="FLEXI MULTI" or bcfType=="FLEXI MR10"):
                    bcfModel='M';

                if bcfModel == 'C':
                    bcf_sig = word[4]
                    omuName = word[5]
                    omuId = word[5]
                elif bcfModel == 'P':
                    bcf_sig = word[4]
                    omuName = word[5]
                    omuId = word[5]
                elif bcfModel == 'E':
                    bcf_sig = word[5]
                    omuName = word[6]
                    omuId = word[6]
                elif bcfModel == 'M':
                    if "SBTS" in line: 
                        bcf_sig = word[6]
                        omuName = word[7]
                        omuId = word[7]
                    else:
                        bcf_sig = word[5]
                        omuName = word[6]
                        omuId = word[6]                       
                dummy_omuId = omuId 
                for letter in dummy_omuId:
                    try:
                        Id = int(letter)
                    except Exception:
                        omuId = omuId.replace(letter,"")
                #print("BCF ID:", bcfId, " / BCF SIG:", bcf_sig, " / OMUNAME:", omuName, " / OMU ID:", omuId)
                continue
            # read BTS ID   
            if "BTS-" in line and zeei == True:
                #print(line)
                word = line.split()
                lac = word[0]
                ci = word[1]
                btsId = word[2]
                btsId = btsId[4:]
                #print("LAC:", lac, " / CI:", ci," / BTS ID:", btsId)
                continue
            # read bts name
            if ("RF/-" in line or "-/-" in line) and zeei == True:
                #print(line)
                word = line.split()
                btsName = word[0]
                #print("BTS NAME:", btsName)
                continue
            # read TRX ID   
            if "TRX-" in line and zeei == True:
                #print(line)
                trx_channel = ''
                trx_pref = ''
                trx_sig = ''
                #print(line)
                word = line.split()
                if "TRX" in word[0]:
                    trx_pos = 0
                elif "TRX" in word[1]:
                    trx_pos = 1
                    
                trxName = word[trx_pos].replace('-','')
                # takeoff one "0" from trxid if the id is 003 ->03
                if len(trxName) > 5:
                    trxName = trxName[0:3]+trxName[4:]
                #print('trxName=',trxName)
                c = ('T','R','X','-')
                trxID = trxName
                for letter in c:
                    trxID = trxID.replace(letter,'')
                #print('trxID=',trxID)
                trx_freq = word[3+trx_pos]
                trx_pcm = word[5+trx_pos]
                
                if "CH" in word[6+trx_pos] and "P" in word[7+trx_pos]:
                    trx_channel = word[6+trx_pos]
                    trx_pref = word[7+trx_pos]
                    trx_sig = word[8+trx_pos]
                elif "CH" in word[6+trx_pos] and not "P" in word[7+trx_pos]:
                    trx_channel = word[6+trx_pos]
                    trx_sig = word[7+trx_pos]
                elif not "CH" in word[6+trx_pos] and "P" in word[6+trx_pos]:
                    trx_pref = word[6+trx_pos]
                    trx_sig = word[7+trx_pos]
                elif not "CH" in word[6] and not "P" in word[6]:
                    trx_sig = word[6+trx_pos]                   
                               
                data = (str(bscType),
                        str(bcfModel),
                        str(bscName),
                        str(omuName),
                        str(omuId),
                        str(bcfType),
                        str(bcfId),
                        str(bcf_sig),
                        str(lac),
                        str(ci),
                        str(btsId),
                        str(btsName),
                        str(trxName),
                        str(trxID),
                        str(trx_freq),
                        str(trx_pcm),
                        str(trx_channel),
                        str(trx_pref),
                        str(trx_sig))
                self.ZEEI_Info.append(data)
                
                    
            if "COMMAND EXECUTED" in line and zeei==True:
                zeei=False
                break
        print("ZEEI -------------------------------------------------------------------") 
        for line in self.ZEEI_Info: 
            print(line)           
        #bscType, bcfModel, bscName, omuName, omuId, bcfType, bcfId, bcf_sig, lac, ci, btsId, btsName, trxName, trxID, trx_freq, trx_pcm, trx_channel, trx_pref, trx_sig
        return self.ZEEI_Info 

    def ZESI(self, dump, pcm):
        zesi = False
        for line in dump.splitlines():
            if "ZESI" in line:
                zesi = True
                continue
            if "COMMAND EXECUTED" in line and zesi:
                zesi = False
                continue
            if len(line.split())>1 and zesi:
                word = line.split()
                if pcm in word[1]:
                    return word[0]
        return

    def ZESB(self, dump, pcm):
        zesb = False
        for line in dump.splitlines():
            if "ZESB" in line:
                zesb = True
                continue
            if "COMMAND EXECUTED" in line and zesb:
                continue
            if len(line.split())>1 and zesb:    
                word = line.split()
                if pcm in word[1]:
                    return word[0]
        return           
        
        
    def ZDTI(self, dump):        
        zdti = False
        readLAPD = False
        for line in dump.splitlines():
            if "DTI:::PCM=" in line:
                zdti = True
                continue
            elif("OMMAND EXECUTED" in line):
                zdti = False
                readLAPD = False
                continue
            if "-----  ---  -------  ---------  -----------  ----  -------" in line:
                readLAPD = True
                continue
            if readLAPD and len(line)>10:
                word = line.split()
                self.ZDTI_Info.append(word)
    
        print("ZDTI -------------------------------------------------------------------")         
        for line in self.ZDTI_Info: 
            print(line)
        # NAME, NUM, UNIT, SIDE, PCM-TSL-TSL, SAPI, STATE   
        return self.ZDTI_Info

    def ZEQO(self, dump):
        zeqo = False
        PLMN = False
        for line in dump.splitlines():
            if "EQO:BTS=" in line:
                zeqo = True
                continue

            if "SEG-" in line and zeqo == True:
                word = line.split()
                seg = word[0]
                seg = seg[5:]
                name = word[1]
                continue
            if "BCF-" in line and zeqo == True:
                word = line.split()
                bcf = word[0]
                bcf = bcf[5:]
                bts = word[1]
                bts = bts[5:]
                continue
            if "CELL IDENTITY............................(CI)....." in line and zeqo == True:
                word = line.split()
                ci = word[-1]
                continue
            if "FREQUENCY BAND IN USE....................(BAND)..." in line and zeqo == True:
                word = line.split()
                band = word[-1]
            if "   NETWORK COLOUR CODE...................(NCC)" in line and zeqo == True:
                word = line.split()
                ncc = word[-1]
                continue
            if "   BTS COLOUR CODE.......................(BCC)" in line and zeqo == True:
                word = line.split()
                bcc = word[-1]
                continue
            if "   MOBILE COUNTRY CODE...................(MCC)" in line and zeqo == True:
                word = line.split()
                mcc = word[-1]
                continue
            if "   MOBILE NETWORK CODE...................(MNC)" in line and zeqo == True:
                word = line.split()
                mnc = word[-1]
                continue
            if "   LOCATION AREA CODE....................(LAC)" in line and zeqo == True:
                word = line.split()
                lac = word[-1]
                continue
            if "BTS HOPPING MODE.........................(HOP)" in line and zeqo == True:
                word = line.split()
                hop = word[-1]
                uhop = '' # inicializar a variavel. Se bcf não for flexi edge não tem este parametro
                continue
            if "UNDERLAY BTS HOPPING MODE................(UHOP)" in line and zeqo == True:
                word = line.split()
                uhop = word[-1]
                continue
            if "   MOBILE ALLOCATION FREQUENCY LIST......(MAL)" in line and zeqo == True:
                word = line.split()
                try:
                    mal = self.get_value(word[-2]+word[-1])
                except Exception:
                    mal = self.get_value(word[-1])
                continue

            if "   HOPPING SEQUENCE NUMBER 1.............(HSN1)" in line and zeqo == True:
                word = line.split()
                hsn1 = word[-1]
                continue
            if "   HOPPING SEQUENCE NUMBER 2.............(HSN2)" in line and zeqo == True:
                word = line.split()
                hsn2 = word[-1]
                continue
            if "PLMN PERMITTED...........................(PLMN)" in line and zeqo == True:
                word = line.split()
                plmn = word[-1]
                PLMN = True
                continue
            if PLMN:
                word = line.split()
                plmn+=word[0]
                PLMN = False
                continue
            if "DIRECTED RETRY USED......................(DR)" in line and zeqo == True:
                word = line.split()
                dr = word[-1]
                continue
            if "CELL RESELECT HYSTERESIS.................(HYS)" in line and zeqo == True:
                word = line.split()
                try:
                    hys = self.get_value(word[-3]+word[-2])
                except Exception:
                    hys = self.get_value(word[-2])
                continue
            if "RXLEV ACCESS MIN.........................(RXP)" in line and zeqo == True:
                word = line.split()
                try:
                    rxp = self.get_value(word[-3]+word[-2])
                except Exception:
                    rxp = self.get_value(word[-2])
                continue    
            if "SMS CB USED..............................(CB)" in line and zeqo == True:
                word = line.split()
                cb = word[-1]
                continue
            if "TRX PRIORITY IN TCH ALLOCATION...........(TRP)" in line and zeqo == True:
                word = line.split()
                trp = word[-1]
                continue
            if "RX DIVERSITY.............................(RDIV)" in line and zeqo == True:
                word = line.split()
                rdiv = word[-1]
                continue
            if "LOWER LIMIT FOR FR TCH RESOURCES.........(FRL)" in line and zeqo == True:
                word = line.split()
                frl = word[-2]
                continue
            if "UPPER LIMIT FOR FR TCH RESOURCES.........(FRU)" in line and zeqo == True:
                word = line.split()
                fru = word[-2]
                continue
            if "   CELL RESELECTION PARAMETER INDEX......(PI)" in line and zeqo == True:
                word = line.split()
                pi = word[-1]
                continue
            if "   CELL RESELECT OFFSET..................(REO)" in line and zeqo == True:
                word = line.split()
                reo = word[-2]
                continue             
            if "   TEMPORARY OFFSET......................(TEO)" in line and zeqo == True:
                word = line.split()
                teo = word[-2]
                continue            
            if "   PENALTY TIME..........................(PET)" in line and zeqo == True:
                word = line.split()
                pet = word[-2]
                continue
            if "   MAIO OFFSET....................(MO)" in line and zeqo == True:
                word = line.split()
                mo = word[-1]
                continue
            if "   MAIO STEP......................(MS)" in line and zeqo == True:
                word = line.split()
                ms = word[-1]
                continue
            if "ROUTING AREA CODE................................(RAC)" in line and zeqo == True:
                word = line.split()
                rac = word[-1]
                continue
            if "DEDICATED GPRS CAPACITY..........................(CDED)" in line and zeqo == True:
                word = line.split()
                cded = word[-2]
                continue            
            if "DEFAULT GPRS CAPACITY............................(CDEF)" in line and zeqo == True:
                word = line.split()
                cdef = word[-2]
                continue  
            if "MAX GPRS CAPACITY................................(CMAX)" in line and zeqo == True:
                word = line.split()
                cmax = word[-2]
                continue  

            if "COMMAND EXECUTED" in line and zeqo == True :
                zeqo = False
                data = (bcf, bts, seg, name, ci, band, ncc, bcc, mcc, mnc, lac, hop, uhop, mal, hsn1, hsn2, plmn, dr, hys, rxp, cb,trp, rdiv, frl, fru, pi, reo, teo, pet, mo, ms, rac, cded, cdef, cmax)
                self.ZEQO_Info.append(data)
                
            
                
                
        print("ZEQO -------------------------------------------------------------------")                 
        for line in self.ZEQO_Info: 
            print(line)
        # bcf, bts, seg, name, ci, band, ncc, bcc, mcc, mnc, lac, hop, uhop, mal, hsn1, hsn2, plmn, dr, hys, rxp, cb,trp, rdiv, frl, fru, pi, reo, teo, pet, mo, ms, rac, cded, cdef, cmax  
        return self.ZEQO_Info


    def ZDSB(self, dump):
        zdsb = False
        readLAPD = False
        for line in dump.splitlines():
            if "DSB:::PCM=" in line:
                zdsb = True
                continue
            elif("OMMAND EXECUTED" in line and zdsb):
                zdsb = False
                readLAPD = False
                continue  
            if "-----  --- ---- ---   -- ----------- ---  ----------------  ---- ------- ---" in line and zdsb:
                readLAPD = True
                continue
            if readLAPD and len(line)>10:
                word = line.split()
                self.ZDSB_Info.append(word)
        print("ZDSB -------------------------------------------------------------------")         
        for line in self.ZDSB_Info: 
            print(line)
        #NAME, NUM, SAPI, TEI, BR, PCM-TSL-TSL, C/M, UNIT, TERM, TERM FUNC, LOG TERM, PCM-TSL, PAR SET 
        return self.ZDSB_Info


    def ZERO(self, dump):
        zero = False
        d_ch = False
        dap = '-' # Flexi MR10 não tem dap, então é necessário inicializar a variavel
        sign = '-' # Flexi MR10 não tem sign, então é necessário inicializar a variavel
        
        for line in dump.splitlines():
            if "ZERO:B" in line:
                zero = True
                continue
            elif("OMMAND EXECUTED" in line and zero):
                zero = False
                continue
            if "BTS-" in line and zero:
                word = line.split()
                bts = word[0]
                bts = bts[4:]
                continue
            if "TRX-" in line and not "DDU       SLAVE (SERVER" in line and zero:
                word = line.split()
                trx = word[0]
                trx = trx[4:]
                continue
            if "GTRX" in line and zero:
                word = line.split()
                gtrx = word[1]
                continue
            if "PREF" in line and zero:
                word = line.split()
                pref = word[-1]
                continue
            if "FREQ" in line and not "FREQUENCY" in line and zero:
                word = line.split()
                freq = word[1]
                tsc = word[3]
                continue
            if "DAP" in line and zero:
                word = line.split()
                dap = word[5]
                continue
            if "SIGN" in line and zero:
                word = line.split()
                if "SIGN" in word[0]: 
                    sign = word[1]
                else:
                    sign = word[5]
                continue
            if "D-CH" in line and zero:
                word = line.split()
                lapd = word[5]
                continue
            if "------------------------------------------------------------------------------" in line and zero:
                d_ch = True
                pcm = ''
                tsl = ''
                channel = []
                continue
            if d_ch and zero:
                word = line.split()
                # save RTSL  PCM-TSL  SUB_TSL  TYPE    I.LEV ADM.STATE     OP.STATE     CH.STATUS
                if len(word) == 7:
                    pcm = word[1]
                    pcm = pcm[:-1]
                    channel.append(word[3])
                    continue
                elif len(word) > 7:
                    pcm = word[1]
                    pcm = pcm[:-1]
                    if tsl == '':
                        tsl = word[2]
                    channel.append(word[4])
                    continue

            if "TRANSCEIVER HAS NO INTERFERING CELLS" in line and zero and d_ch:
                data =(bts, trx, gtrx, pref, freq, tsc, dap, sign, lapd, pcm, tsl, channel)
                self.ZERO_Info.append(data)
                #for ch in channel:
                #    self.ZERO_Info.append(ch)
                d_ch = False
                
            
        print("ZERO -------------------------------------------------------------------")            
        for line in self.ZERO_Info: 
            print(line)
        #bts, trx, gtrx, pref, freq, tsc, dap, sign, lapd, pcm, tsl, channel
        return self.ZERO_Info            
            

    def ZOYV(self, dump):
        zoyv = False
        for line in dump.splitlines():
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
    
    def ZDWQ(self, dump):
        zdwq = False
        for line in dump.splitlines():
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


    def ZEAO(self, dump):
        # estas variaveis são para garantir que vou guardar o valor da primeira vez que identificar as variaveis
        zeao = False
        for line in dump.splitlines():
            if "ZEAO:" in line:
                zeao = True
                continue
            if "COMMAND EXECUTED" in line and zeao:
                zeao = False
                continue
            if "BTS-" in line and "HAS ADJACENT CELL" in line and zeao:
                word = word = line.split()
                bts = word[0]
                bts = bts[4:]
                name = word[1]
                continue 
            if "MOBILE COUNTRY CODE.....................(MCC)" in line and zeao:
                word = word = line.split()
                mcc = word[-1]
                continue
            if "MOBILE NETWORK CODE.....................(MNC)" in line and zeao:
                word = word = line.split()
                mnc = word[-1]
                continue
            if "LOCATION AREA CODE......................(LAC)" in line and zeao:
                word = word = line.split()
                lac = word[-1]
                continue
            if "CELL IDENTIFICATION.....................(CI)" in line and zeao:
                word = word = line.split()
                ci = word[-1]
                continue
            if "NETWORK COLOUR CODE.....................(NCC)" in line and zeao:
                word = word = line.split()
                ncc = word[-1]
                continue
            if "BTS COLOUR CODE.........................(BCC)" in line and zeao:
                word = word = line.split()
                bcc = word[-1]
                continue
            if "FREQUENCY NUMBER OF BCCH................(FREQ)" in line and zeao:
                word = word = line.split()
                freq = word[-1]
                continue
            if "HO MARGIN PBGT..........................(PMRG)" in line and zeao:
                word = word = line.split()
                try:
                    pmrg = self.get_value(word[-3]+word[-2])
                except Exception:
                    pmrg = self.get_value(word[-2])
                continue
            if "HO MARGIN LEV...........................(LMRG)" in line and zeao:
                word = word = line.split()
                try:
                    lmrg = self.get_value(word[-3]+word[-2])
                except Exception:
                    lmrg = self.get_value(word[-2])
                continue 
            if "HO MARGIN QUAL..........................(QMRG)" in line and zeao:
                word = word = line.split()
                try:
                    qmrg = self.get_value(word[-3]+word[-2])
                except Exception:
                    qmrg = self.get_value(word[-2])
                continue 
            if "HO PRIORITY LEVEL.......................(PRI)" in line and zeao:
                word = word = line.split()
                pri = word[-1]
                continue
            if "RX LEV MIN CELL.........................(SL)" in line and zeao:
                word = word = line.split()
                try:
                    sl = self.get_value(word[-3]+word[-2])
                except Exception:
                    sl = self.get_value(word[-2])
                continue 
            if "HO LEVEL UMBRELLA.......................(AUCL)" in line and zeao:
                word = word = line.split()
                try:
                    aucl = self.get_value(word[-3]+word[-2])
                except Exception:
                    aucl = self.get_value(word[-2])
                continue                
            if "SYNCHRONIZED............................(SYNC)" in line and zeao:
                word = word = line.split()
                sync = word[-1]
                continue
            if " DIRECTED RETRY THRESHOLD...............(DRT)" in line and zeao:
                word = word = line.split()
                try:
                    drt = self.get_value(word[-3]+word[-2])
                except Exception:
                    drt = self.get_value(word[-2])
                continue
            if " ADJACENT GPRS ENABLED..................(AGENA)" in line and zeao:
                word = word = line.split()
                agena = word[-1]
                continue
            if " ROUTING AREA CODE......................(RAC)" in line and zeao:
                word = word = line.split()
                rac = word[-1]
                continue
            if "ADJACENT CELL HAS NO REFERENCE CELLS" in line and zeao:
                d = (bts, name, mcc, mnc, lac, ci, ncc, bcc, freq, pmrg, lmrg, qmrg, pri, sl, aucl, sync, drt, agena, rac)
                self.ZEAO_Info.append(d)
                continue
        print("ZEAO -------------------------------------------------------------------")            
        for line in self.ZEAO_Info: 
            print(line)
        #bts, name, mcc, mnc, lac, ci, ncc, bcc, freq, pmrg, lmrg, qmrg, pri, sl, aucl, sync, drt, agena, rac
        return self.ZEAO_Info


#----------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------
    def create_OMU(self):         
        for row in self.ZEEI_Info:
            bscType, bcfModel, bscName, omuName, omuId, bcfType, bcfId, bcf_sig, lac, ci, btsId, btsName, trxName, trxID, trx_freq, trx_pcm, trx_channel, trx_pref, trx_sig = row
            break
        for row in self.ZDSB_Info:
            if len(row) == 13:
                name, num, sapi, tei, br, pcm_tsl_tsl, c_m, unit, term, term_func, log_term, pcm_tsl, par_set = row
            elif len(row) == 12:
                name, num, sapi, tei, br, pcm_tsl_tsl, unit, term, term_func, log_term, pcm_tsl, par_set = row
            else:
                return "Erro a ler ZDSB. Verificar nº de elementos na linha"
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
        
        return 'ZDSE:'+str(omuName)+':'+str(unit_type)+','+str(unit_index)+':'+str(sapi)+','+str(tei)+':'+str(br)+','+str(pcm_tls)+','+str(tls)+':N,'+str(par_set)+';\n\n'
        
        
    def lock_trx(self):
        cmd = ""
        for bscType, bcfModel, bscName, omuName, omuId, bcfType, bcfId, bcf_sig, lac, ci, btsId, btsName, trxName, trxID, trx_freq, trx_pcm, trx_channel, trx_pref, trx_sig in self.bcf_info:
            cmd += "ZERS:BTS{},TRX={}:L;".format(btsId, trxID)
        return cmd




    
