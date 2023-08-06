import win32com.client
import pythoncom
import os, sys
import inspect
import sqlite3
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pprint import pprint

class XASessionEvents:
    status = False
    
    def OnLogin(self,code,msg):
        print("OnLogin : ", code, msg)
        XASessionEvents.status = True
    
    def OnLogout(self):
        print('OnLogout')

    def OnDisconnect(self):
        print('OnDisconnect')

    def OnSendPacketSize(self):
        print('OnSendPacketSize')

    def OnConnectTimeOut(self):
        print('OnConnectTimeOut')


class XAQueryEvents:
    status = False
    
    def OnReceiveData(self,szTrCode):
        print("OnReceiveData : %s" % szTrCode)
        XAQueryEvents.status = True
    
    def OnReceiveMessage(self,systemError,messageCode,message):
        print("OnReceiveMessage : ", systemError, messageCode, message)
        XAQueryEvents.status = True


class XARealEvents:
    pass

class ebest:
    def __init__(self,id,pwd,cert='',url='demo.ebestsec.co.kr',svrtype=0,port=200001):
        self.id = id
        self.pwd = pwd
        self.cert = cert
        self.url = url
        self.svrtype=svrtype
        self.port = port
        self.account = self.login(self.id, self.pwd, self.cert, self.url, self.svrtype, self.port)
        

    def login(self, id ,pwd,cert,url,svrtype,port):
        session = win32com.client.DispatchWithEvents("XA_Session.XASession",XASessionEvents)
        connect = session.ConnectServer(url,port)

        if not connect:
            nErrCode = session.GetLastError()
            strErrMsg = session.GetErrorMessage(nErrCode)
            print(nErrCode, strErrMsg)
            return None
        
        session.Login(id,pwd,cert,svrtype,0)

        while XASessionEvents.status == False:
            pythoncom.PumpWaitingMessages()
        XASessionEvents.status = False

        data = {}
        num_of_account = session.GetAccountListCount()
        for i in range(num_of_account):
            account_code = session.GetAccountList(i)
            account_name = session.GetAcctDetailName(account_code)
            data[account_name] = account_code
        return data


    def t8424(self, gubun1=''):
        '''
        업종전체조회
        '''
        query = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery",XAQueryEvents)
        
        MYNAME = inspect.currentframe().f_code.co_name
        INBLOCK = "%sInBlock" % MYNAME
        OUTBLOCK = "%sOutBlock" % MYNAME
        OUTBLOCK1 = "%sOutBlock1" %MYNAME
        RESFILE = r"C:\eBEST\xingAPI\Res\%s.res"%MYNAME

        query.LoadFromResFile(RESFILE)
        query.SetFieldData(INBLOCK,"gubun1",0,gubun1)
        query.Request(0)
        while XAQueryEvents.status == False:
            pythoncom.PumpWaitingMessages()
        XAQueryEvents.status = False
        data = {}
        block_count = query.GetBlockCount(OUTBLOCK)
        name_lst = ['hname','upcode']

        for i in range(block_count):
            hname = query.GetFieldData(OUTBLOCK,name_lst[0],i).strip()
            upcode = query.GetFieldData(OUTBLOCK,name_lst[1],i).strip()
            data[hname] = upcode
        return data


    def t1101(self, shcode):
        '''
        주식 현재가 호가 조회
        '''
        query = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery",XAQueryEvents)
        
        MYNAME = inspect.currentframe().f_code.co_name
        INBLOCK = "%sInBlock" % MYNAME
        OUTBLOCK = "%sOutBlock" % MYNAME
        OUTBLOCK1 = "%sOutBlock1" %MYNAME
        RESFILE = r"C:\eBEST\xingAPI\Res\%s.res"%MYNAME

        query.LoadFromResFile(RESFILE)
        query.SetFieldData(INBLOCK,"shcode",0,shcode)
        query.Request(0)
        
        while XAQueryEvents.status == False:
            pythoncom.PumpWaitingMessages()
        XAQueryEvents.status = False
        
        data = {}
        block_count = query.GetBlockCount(OUTBLOCK)
        name_lst = ['hname','price','sign','change','diff','volume','jnilclose',
            'offerho1','bidho1','offerrem1','bidrem1','preoffercha1','prebidcha1',
            'offerho2','bidho2','offerrem2','bidrem2','preoffercha2','prebidcha2',
            'offerho3','bidho3','offerrem3','bidrem3','preoffercha3','prebidcha3',
            'offerho4','bidho4','offerrem4','bidrem4','preoffercha4','prebidcha4',
            'offerho5','bidho5','offerrem5','bidrem5','preoffercha5','prebidcha5',
            'offerho6','bidho6','offerrem6','bidrem6','preoffercha6','prebidcha6',
            'offerho7','bidho7','offerrem7','bidrem7','preoffercha7','prebidcha7',
            'offerho8','bidho8','offerrem8','bidrem8','preoffercha8','prebidcha8',
            'offerho9','bidho9','offerrem9','bidrem9','preoffercha9','prebidcha9',
            'offerho10','bidho10','offerrem10','bidrem10','preoffercha10','prebidcha10',
            'offer','bid','preoffercha','prebidcha','hotime','yeprice','yevolme',
            'yesign','yechange','yediff','tmoffer','tmbid','ho_status','shcode',
            'uplmtprice','dnlmtprice','open','high','low',
            ]
        
        for i in range(block_count):
            for name in name_lst:
                data[name] = query.GetFieldData(OUTBLOCK,name,i).strip()
                if name in ('diff','yediff'):
                    if data[name] == '':
                        data[name] = 0
                    data[name] = float(data[name])
                elif name not in ('hname','sign','hotime','yesign','ho_status','shcode'):
                    if data[name] == '':
                        data[name] = 0
                    data[name] = int(data[name])
        return data


    def t8411(self, 단축코드, 시작일자, 종료일자, 단위=1, 요청건수=2000, 조회영업일수='0', 연속일자='', 연속시간='', 압축여부='N',result=[],연속조회=0):
        '''
        주식차트(틱/n틱)
        ''' 
        query = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery",XAQueryEvents)
        MYNAME = inspect.currentframe().f_code.co_name
        INBLOCK = "%sInBlock" % MYNAME
        OUTBLOCK = "%sOutBlock" % MYNAME
        OUTBLOCK1 = "%sOutBlock1" % MYNAME
        RESFILE = r"C:\eBEST\xingAPI\Res\%s.res"%MYNAME

        query.LoadFromResFile(RESFILE)
        query.SetFieldData(INBLOCK, "shcode",0,단축코드)
        query.SetFieldData(INBLOCK, "ncnt",0,단위)
        query.SetFieldData(INBLOCK, "qrycnt",0,요청건수)
        query.SetFieldData(INBLOCK, "nday",0,조회영업일수)
        query.SetFieldData(INBLOCK, "sdate",0,시작일자)
        query.SetFieldData(INBLOCK, "edate",0,종료일자)
        query.SetFieldData(INBLOCK, "cts_date",0,연속일자)
        query.SetFieldData(INBLOCK, "cts_time",0,연속시간)
        query.SetFieldData(INBLOCK, "comp_yn",0,압축여부)
        query.Request(연속조회)

        while XAQueryEvents.status == False:
            pythoncom.PumpWaitingMessages()
        XAQueryEvents.status = False

        연속일자_c = query.GetFieldData(OUTBLOCK,'cts_date',0).strip()
        연속시간_c = query.GetFieldData(OUTBLOCK,'cts_time',0).strip()
        #print(연속일자_c, 연속시간_c)
        nCount = query.GetBlockCount(OUTBLOCK1)
        for i in range(nCount):
            날짜 = query.GetFieldData(OUTBLOCK1, 'date',i).strip()
            시간 = query.GetFieldData(OUTBLOCK1, 'time',i).strip()
            시가 = int(query.GetFieldData(OUTBLOCK1, 'open',i).strip())
            #고가 = int(query.GetFieldData(OUTBLOCK1, 'high',i).strip())
            #저가 = int(query.GetFieldData(OUTBLOCK1, 'low',i).strip())
            #종가 = int(query.GetFieldData(OUTBLOCK1, 'close',i).strip())
            거래량 = int(query.GetFieldData(OUTBLOCK1, 'jdiff_vol',i).strip())

            #lst = [날짜,시간,시가,고가,저가,종가,거래량]
            lst = [날짜,시간,시가,거래량]
            result.insert(i,lst)
        

        if 연속일자_c !='' and 연속시간_c != '':
            time.sleep(3.1)
            self.t8411(단축코드, 시작일자, 종료일자, 단위, 요청건수, 조회영업일수,연속일자_c, 연속시간_c, 압축여부,result,1)

        # df = pd.DataFrame(data=result, columns=['date','time','open','high','low','close','volume'])
        df = pd.DataFrame(data=result, columns=['date','time','price','volume'])
        return df


    def t1901(self, shcode):
        '''
        ETF 현재가(시세) 조회
        '''
        query = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery",XAQueryEvents)
        
        MYNAME = inspect.currentframe().f_code.co_name
        INBLOCK = "%sInBlock" % MYNAME
        OUTBLOCK = "%sOutBlock" % MYNAME
        OUTBLOCK1 = "%sOutBlock1" %MYNAME
        RESFILE = r"C:\eBEST\xingAPI\Res\%s.res"%MYNAME

        query.LoadFromResFile(RESFILE)
        query.SetFieldData(INBLOCK,"shcode",0,shcode)
        query.Request(0)
        
        while XAQueryEvents.status == False:
            pythoncom.PumpWaitingMessages()
        XAQueryEvents.status = False
        
        data = {}
        block_count = query.GetBlockCount(OUTBLOCK)
        name_lst = [
            'hname',
            'price',
            'sign',
            'change',
            'diff',
            'volume',
            'recprice',
            'avg',
            'uplmtprice',
            'dnlmtprice',
            'jnilvolume',
            'volumediff',
            'open',
            'opentime',
            'high',
            'hightime',
            'low',
            'lowtime',
            'high52w',
            'high52wdate',
            'low52w',
            'low52wdate',
            'exhratio',
            'flmtvol',
            'per',
            'listing',
            'jkrate',
            'vol',
            'shcode',
            'value',
            'highyear',
            'highyeardate',
            'lowyear',
            'lowyeardate',
            'upname',
            'upcode',
            'upprice',
            'upsign',
            'upchange',
            'updiff',
            'futname',
            'futcode',
            'futprice',
            'futsign',
            'futchange',
            'futdiff',
            'nav',
            'navsign',
            'navchange',
            'navdiff',
            'cocrate',
            'kasis',
            'subprice',
            'offerno1',
            'bidno1',
            'dvol1',
            'svol1',
            'dcha1',
            'scha1',
            'ddiff1',
            'sdiff1',
            'offerno2',
            'bidno2',
            'dvol2',
            'svol2',
            'dcha2',
            'scha2',
            'ddiff2',
            'sdiff2',
            'offerno3',
            'bidno3',
            'dvol3',
            'svol3',
            'dcha3',
            'scha3',
            'ddiff3',
            'sdiff3',
            'offerno4',
            'bidno4',
            'dvol4',
            'svol4',
            'dcha4',
            'scha4',
            'ddiff4',
            'sdiff4',
            'offerno5',
            'bidno5',
            'dvol5',
            'svol5',
            'dcha5',
            'scha5',
            'ddiff5',
            'sdiff5',
            'fwdvl',
            'ftradmdcha',
            'ftradmddiff',
            'fwsvl',
            'ftradmscha',
            'ftradmsdiff',
            'upname2',
            'upcode2',
            'upprice2',
            'jnilnav',
            'jnilnavsign',
            'jnilnavchange',
            'jnilnavdiff',
            'etftotcap',
            'spread',
            'leverage',
            'taxgubun',
            'opcom_nmk',
            'lp_nm1',
            'lp_nm2',
            'lp_nm3',
            'lp_nm4',
            'lp_nm5',
            'etf_cp',
            'etf_kind',
            'vi_gubun',
            'etn_kind_cd',
            'lastymd',
            'payday',
            'lastdate',
            'issuernmk',
            'last_sdate',
            'last_edate',
            'lp_holdvol',
            'listdate',
            'etp_gb',
            'etn_elback_yn',
            'settletype',
            'idx_asset_class1',
            'ty_text',
        ]

        type_lst = [
            'string',
            'long',
            'string',
            'long',
            'float',
            'float',
            'long',
            'long',
            'long',
            'long',
            'float',
            'long',
            'long',
            'string',
            'long',
            'string',
            'long',
            'string',
            'long',
            'string',
            'long',
            'string',
            'float',
            'float',
            'float',
            'long',
            'long',
            'float',
            'string',
            'long',
            'long',
            'string',
            'long',
            'string',
            'string',
            'string',
            'float',
            'string',
            'float',
            'float',
            'string',
            'string',
            'float',
            'string',
            'float',
            'float',
            'float',
            'string',
            'float',
            'float',
            'float',
            'float',
            'long',
            'string',
            'string',
            'long',
            'long',
            'long',
            'long',
            'float',
            'float',
            'string',
            'string',
            'long',
            'long',
            'long',
            'long',
            'float',
            'float',
            'string',
            'string',
            'long',
            'long',
            'long',
            'long',
            'float',
            'float',
            'string',
            'string',
            'long',
            'long',
            'long',
            'long',
            'float',
            'float',
            'string',
            'string',
            'long',
            'long',
            'long',
            'long',
            'float',
            'float',
            'long',
            'long',
            'float',
            'long',
            'long',
            'float',
            'string',
            'string',
            'float',
            'float',
            'string',
            'float',
            'float',
            'long',
            'float',
            'long',
            'string',
            'string',
            'string',
            'string',
            'string',
            'string',
            'string',
            'string',
            'string',
            'string',
            'string',
            'string',
            'string',
            'string',
            'string',
            'string',
            'string',
            'string',
            'string',
            'string',
            'string',
            'string',
            'string',
            'string',

        ]
        
        for i in range(block_count):
            for name_,type_ in zip(name_lst,type_lst):
                data[name_] = query.GetFieldData(OUTBLOCK,name_,i).strip()
                if type_ == 'long':
                    if data[name_] =='': data[name_] = 0
                    data[name_] = int(data[name_])
                elif type_ == 'float':
                    if data[name_] =='': data[name_] = 0
                    data[name_] = float(data[name_])
        return data


    def t1902(self, 단축코드, 시간, result = [], 연속조회 = 0):
        '''
        ETF 시간별추이
        ''' 
        query = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery",XAQueryEvents)
        MYNAME = inspect.currentframe().f_code.co_name
        INBLOCK = "%sInBlock" % MYNAME
        OUTBLOCK = "%sOutBlock" % MYNAME
        OUTBLOCK1 = "%sOutBlock1" % MYNAME
        RESFILE = r"C:\eBEST\xingAPI\Res\%s.res"%MYNAME
        
        query.LoadFromResFile(RESFILE)
        query.SetFieldData(INBLOCK, "shcode",0,단축코드)
        query.SetFieldData(INBLOCK, "time",0,시간)
        query.Request(연속조회)

        while XAQueryEvents.status == False:
            pythoncom.PumpWaitingMessages()
        XAQueryEvents.status = False

        시간_c = query.GetFieldData(OUTBLOCK,'time',0).strip()
        nCount = query.GetBlockCount(OUTBLOCK1)

        columns = [
            '시간',
            '현재가',
            '전일대비구분',
            '전일대비',
            '누적거래량',
            'NAV대비',
            'NAV',
            '전일대비',
            '추적오차',
            '괴리',
            '지수',
            '전일대비',
            '전일대비율',
        ]

        names = [
            'time',
            'price',
            'sign',
            'change',
            'volume',
            'navdiff',
            'nav',
            'navchange',
            'crate',
            'grate',
            'jisu',
            'jichange',
            'jirate',
        ]

        types = [
            'string',
            'long',
            'string',
            'long',
            'float',
            'float',
            'float',
            'float',
            'float',
            'float',
            'float',
            'float',
            'float',
        ]
        for i in range(nCount):
            lst = []
            for name_,type_ in zip(names,types):
                tmp = query.GetFieldData(OUTBLOCK1,name_,i).strip()
                if type_ == 'long':
                    if tmp=='': tmp = 0
                    tmp = int(tmp)
                elif type == 'float':
                    if tmp=='': tmp = 0
                    tmp = float(tmp)
                lst.append(tmp)
            result.insert(i,lst)
        

        if 시간_c !='':
            print(시간_c)
            time.sleep(3.1)
            self.t1902(단축코드, 시간_c, result, 1)

        df = pd.DataFrame(data=result, columns=columns)
        return df


    def t1903(self, 단축코드, 일자, result = [], 연속조회 = 0):
        '''
        ETF 일별추이
        ''' 
        query = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery",XAQueryEvents)
        MYNAME = inspect.currentframe().f_code.co_name
        INBLOCK = "%sInBlock" % MYNAME
        OUTBLOCK = "%sOutBlock" % MYNAME
        OUTBLOCK1 = "%sOutBlock1" % MYNAME
        RESFILE = r"C:\eBEST\xingAPI\Res\%s.res"%MYNAME
        
        query.LoadFromResFile(RESFILE)
        query.SetFieldData(INBLOCK, "shcode",0,단축코드)
        query.SetFieldData(INBLOCK, "date",0,일자)
        query.Request(연속조회)

        while XAQueryEvents.status == False:
            pythoncom.PumpWaitingMessages()
        XAQueryEvents.status = False

        일자_c = query.GetFieldData(OUTBLOCK,'date',0).strip()
        nCount = query.GetBlockCount(OUTBLOCK1)

        columns = [
            '일자',
            '현재가',
            '전일대비구분',
            '전일대비',
            '누적거래량',
            'NAV대비',
            'NAV',
            '전일대비',
            '추적오차',
            '괴리',
            '지수',
            '전일대비',
            '전일대비율',
        ]

        names = [
            'date',
            'price',
            'sign',
            'change',
            'volume',
            'navdiff',
            'nav',
            'navchange',
            'crate',
            'grate',
            'jisu',
            'jichange',
            'jirate',
        ]

        types = [
            'string',
            'long',
            'string',
            'long',
            'float',
            'float',
            'float',
            'float',
            'float',
            'float',
            'float',
            'float',
            'float',
        ]
        for i in range(nCount):
            lst = []
            for name_,type_ in zip(names,types):
                tmp = query.GetFieldData(OUTBLOCK1,name_,i).strip()
                if type_ == 'long':
                    if tmp == '': tmp = 0
                    tmp = int(tmp)
                elif type == 'float':
                    if tmp == '': tmp = 0
                    tmp = float(tmp)
                lst.append(tmp)
            result.insert(i,lst)
        

        if 일자_c !='':
            print(일자_c)
            time.sleep(3.1)
            self.t1903(단축코드, 일자_c, result, 1)
        df = pd.DataFrame(data=result, columns=columns)
        return df
    

    def t1904(self, 단축코드, 적용일자, 정렬기준='1'):
        '''
        ETF 구성종목조회
        '''
        query = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery",XAQueryEvents)
        
        MYNAME = inspect.currentframe().f_code.co_name
        INBLOCK = "%sInBlock" % MYNAME
        OUTBLOCK = "%sOutBlock" % MYNAME
        OUTBLOCK1 = "%sOutBlock1" %MYNAME
        RESFILE = r"C:\eBEST\xingAPI\Res\%s.res"%MYNAME

        query.LoadFromResFile(RESFILE)
        query.SetFieldData(INBLOCK,"shcode",0,단축코드)
        query.SetFieldData(INBLOCK,"date",0,적용일자)
        query.SetFieldData(INBLOCK,"sgb",0,정렬기준)
        query.Request(0)
        
        while XAQueryEvents.status == False:
            pythoncom.PumpWaitingMessages()
        XAQueryEvents.status = False
        
        columns = [
            '단축코드',
            '한글명',
            '현재가',
            '전일대비구분',
            '전일대비',
            '등락율',
            '누적거래량',
            '거래대금(백만)',
            '단위증권수(계약수/원화현금/USD현금/창고증권)',
            '액면금액/설정현금액',
            '평가금액',
            '구성시가총액',
            'PDF적용일자',
            '비중(평가금액)',
            'ETF종목과등락차',
        ]

        names = [
            'shcode',
            'hname',
            'price',
            'sign',
            'change',
            'diff',
            'volume',
            'value',
            'icux',
            'parprice',
            'pvalue',
            'sigatvalue',
            'profitdate',
            'weight',
            'diff2',
        ]

        types = [
            'string',
            'string',
            'long',
            'string',
            'long',
            'float',
            'long',
            'long',
            'long',
            'long',
            'long',
            'long',
            'string',
            'float',
            'float',
        ]
        result = []
        block_count = query.GetBlockCount(OUTBLOCK1)
        for i in range(block_count):
            lst = []
            for name_,type_ in zip(names,types):
                tmp = query.GetFieldData(OUTBLOCK1,name_,i)
                if type_ == 'long':
                    if tmp =='': tmp = 0
                    tmp = int(tmp)
                elif type_ == 'float':
                    if tmp =='': tmp = 0
                    tmp = float(tmp)
                lst.append(tmp)
            result.append(lst)
        df = pd.DataFrame(data=result,columns=columns)
        return df

    def t1906(self, shcode):
        '''
        ETFLP호가
        '''
        query = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery",XAQueryEvents)
        
        MYNAME = inspect.currentframe().f_code.co_name
        INBLOCK = "%sInBlock" % MYNAME
        OUTBLOCK = "%sOutBlock" % MYNAME
        OUTBLOCK1 = "%sOutBlock1" %MYNAME
        RESFILE = r"C:\eBEST\xingAPI\Res\%s.res"%MYNAME

        query.LoadFromResFile(RESFILE)
        query.SetFieldData(INBLOCK,"shcode",0,shcode)
        query.Request(0)
        
        while XAQueryEvents.status == False:
            pythoncom.PumpWaitingMessages()
        XAQueryEvents.status = False
        
        data = {}
        block_count = query.GetBlockCount(OUTBLOCK)
        columns = [
            '한글명',
'현재가',
'전일대비구분',
'전일대비',
'등락율',
'누적거래량',
'LP매도호가수량1',
'LP매수호가수량1',
'LP매도호가수량2',
'LP매수호가수량2',
'LP매도호가수량3',
'LP매수호가수량3',
'LP매도호가수량4',
'LP매수호가수량4',
'LP매도호가수량5',
'LP매수호가수량5',
'LP매도호가수량6',
'LP매수호가수량6',
'LP매도호가수량7',
'LP매수호가수량7',
'LP매도호가수량8',
'LP매수호가수량8',
'LP매도호가수량9',
'LP매수호가수량9',
'LP매도호가수량10',
'LP매수호가수량10',
'전일종가',
'매도호가1',
'매수호가1',
'매도호가수량1',
'매수호가수량1',
'직전매도대비수량1',
'직전매수대비수량1',
'매도호가2',
'매수호가2',
'매도호가수량2',
'매수호가수량2',
'직전매도대비수량2',
'직전매수대비수량2',
'매도호가3',
'매수호가3',
'매도호가수량3',
'매수호가수량3',
'직전매도대비수량3',
'직전매수대비수량3',
'매도호가4',
'매수호가4',
'매도호가수량4',
'매수호가수량4',
'직전매도대비수량4',
'직전매수대비수량4',
'매도호가5',
'매수호가5',
'매도호가수량5',
'매수호가수량5',
'직전매도대비수량5',
'직전매수대비수량5',
'매도호가6',
'매수호가6',
'매도호가수량6',
'매수호가수량6',
'직전매도대비수량6',
'직전매수대비수량6',
'매도호가7',
'매수호가7',
'매도호가수량7',
'매수호가수량7',
'직전매도대비수량7',
'직전매수대비수량7',
'매도호가8',
'매수호가8',
'매도호가수량8',
'매수호가수량8',
'직전매도대비수량8',
'직전매수대비수량8',
'매도호가9',
'매수호가9',
'매도호가수량9',
'매수호가수량9',
'직전매도대비수량9',
'직전매수대비수량9',
'매도호가10',
'매수호가10',
'매도호가수량10',
'매수호가수량10',
'직전매도대비수량10',
'직전매수대비수량10',
'매도호가수량합',
'매수호가수량합',
'직전매도대비수량합',
'직전매수대비수량합',
'수신시간',
'예상체결가격',
'예상체결수량',
'예상체결전일구분',
'예상체결전일대비',
'예상체결등락율',
'시간외매도잔량',
'시간외매수잔량',
'동시구분',
'단축코드',
'상한가',
'하한가',
'시가',
'고가',
'저가',

        ]
        names = [
'hname',
'price',
'sign',
'change',
'diff',
'volume',
'lp_offerrem1',
'lp_bidrem1',
'lp_offerrem2',
'lp_bidrem2',
'lp_offerrem3',
'lp_bidrem3',
'lp_offerrem4',
'lp_bidrem4',
'lp_offerrem5',
'lp_bidrem5',
'lp_offerrem6',
'lp_bidrem6',
'lp_offerrem7',
'lp_bidrem7',
'lp_offerrem8',
'lp_bidrem8',
'lp_offerrem9',
'lp_bidrem9',
'lp_offerrem10',
'lp_bidrem10',
'jnilclose',
'offerho1',
'bidho1',
'offerrem1',
'bidrem1',
'preoffercha1',
'prebidcha1',
'offerho2',
'bidho2',
'offerrem2',
'bidrem2',
'preoffercha2',
'prebidcha2',
'offerho3',
'bidho3',
'offerrem3',
'bidrem3',
'preoffercha3',
'prebidcha3',
'offerho4',
'bidho4',
'offerrem4',
'bidrem4',
'preoffercha4',
'prebidcha4',
'offerho5',
'bidho5',
'offerrem5',
'bidrem5',
'preoffercha5',
'prebidcha5',
'offerho6',
'bidho6',
'offerrem6',
'bidrem6',
'preoffercha6',
'prebidcha6',
'offerho7',
'bidho7',
'offerrem7',
'bidrem7',
'preoffercha7',
'prebidcha7',
'offerho8',
'bidho8',
'offerrem8',
'bidrem8',
'preoffercha8',
'prebidcha8',
'offerho9',
'bidho9',
'offerrem9',
'bidrem9',
'preoffercha9',
'prebidcha9',
'offerho10',
'bidho10',
'offerrem10',
'bidrem10',
'preoffercha10',
'prebidcha10',
'offer',
'bid',
'preoffercha',
'prebidcha',
'hotime',
'yeprice',
'yevolume',
'yesign',
'yechange',
'yediff',
'tmoffer',
'tmbid',
'ho_status',
'shcode',
'uplmtprice',
'dnlmtprice',
'open',
'high',
'low',

        ]

        types = [
'string',
'long',
'string',
'long',
'float',
'long',
'long',
'long',
'long',
'long',
'long',
'long',
'long',
'long',
'long',
'long',
'long',
'long',
'long',
'long',
'long',
'long',
'long',
'long',
'long',
'long',
'long',
'long',
'long',
'long',
'long',
'long',
'long',
'long',
'long',
'long',
'long',
'long',
'long',
'long',
'long',
'long',
'long',
'long',
'long',
'long',
'long',
'long',
'long',
'long',
'long',
'long',
'long',
'long',
'long',
'long',
'long',
'long',
'long',
'long',
'long',
'long',
'long',
'long',
'long',
'long',
'long',
'long',
'long',
'long',
'long',
'long',
'long',
'long',
'long',
'long',
'long',
'long',
'long',
'long',
'long',
'long',
'long',
'long',
'long',
'long',
'long',
'long',
'long',
'long',
'long',
'string',
'long',
'long',
'string',
'long',
'float',
'long',
'long',
'string',
'string',
'long',
'long',
'long',
'long',
'long',

        ]
        
        for i in range(block_count):
            for name_,type_ in zip(names,types):
                data[name_] = query.GetFieldData(OUTBLOCK,name_,i).strip()
                if type_ == 'long':
                    if data[name_] =='': data[name_] = 0
                    data[name_] = int(data[name_])
                elif type_ == 'float':
                    if data[name_] =='': data[name_] = 0
                    data[name_] = float(data[name_])
        return data


if __name__ == '__main__':
    ebest = ebest(id=,pwd=,cert='')
    pprint(ebest.t1101('091170'))
    pprint(ebest.t8424())
    print(ebest.account)
    # df = ebest.t8411('091170','20220720','20220720')
    # print(df)
    pprint(ebest.t1901('091170'))
    # print(ebest.t1903('091170',''))
    print(ebest.t1904('091170','20220701'))
    pprint(ebest.t1906('091170'))




