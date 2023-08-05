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

def login(id,pwd,cert='',url='demo.ebestsec.co.kr',svrtype=0,port=200001):
    session = win32com.client.DispatchWithEvents("XA_Session.XASession",XASessionEvents)
    connecet = session.ConnectServer(url,port)

    if not connecet:
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


def CSPAQ13700():
    pass


def t8424(gubun1=''):
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



def t1101(shcode):
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
    return data


def t8411(단축코드, 시작일자, 종료일자, 단위=1, 요청건수=2000, 조회영업일수='0', 연속일자='', 연속시간='', 압축여부='N',result=[],연속조회=0):
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
        t8411(단축코드, 시작일자, 종료일자, 단위, 요청건수, 조회영업일수,연속일자_c, 연속시간_c, 압축여부,result,1)

    # df = pd.DataFrame(data=result, columns=['date','time','open','high','low','close','volume'])
    df = pd.DataFrame(data=result, columns=['date','time','price','volume'])
    return df



if __name__ == '__main__':
    account_lst = login(id='riew710',pwd='00aa') # 국내해외주식 / 국내선물옵션 / 해외선물
    pprint(t1101('091170'))
    print()
    pprint(t8424())
    print()
    print(account_lst)
    df = t8411('091170','20220719','20220720')
    print(df)


