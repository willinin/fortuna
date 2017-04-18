#encoding:utf-8
import sys,os
from generator import Generator
from hashlib import sha256
from Crypto.Cipher import AES
from evdev import InputDevice
from select import select
from binascii import b2a_hex, a2b_hex
import math
import time
import threading

class Accumulator(object):
    # the status of Accumulator
    R = {'P':[b''] * 64,'reseedcnt':0,'generator':0,'last_seed':0}
    MINPOOLSIZE = 64
    ExitFlag=0

    def __init__(self,gen):
        self.ListenEvent()
        self.InitializePRNG(gen)

    #监听事件，这里仅包含2个事件，即点击鼠标和敲击键盘
    #notice: linux使用evdev，windows下使用Pyhook
    def ListenEvent(self):
        key = threading.Thread(target=self.KeyboardEvent)
        key.start()
        mouse = threading.Thread(target=self.MouseEvent)
        mouse.start()

    def InitializePRNG(self,gen):
        self.R['P']=[b'']*64
        self.R['reseedcnt']=0
        self.R['generator']=gen
        self.R['generator'].InitializeGenerator()
        #最近一次生成种子的时间
        self.R['last_seed']=0

    #重新产生种子,并生成随机数
    def RandomData(self,n):
        #n: Number of bytes of random data to generate
        #r: The string of PRNG
        p = self.R['P']
        #print len(p[0])
        if len(p[0])>=self.MINPOOLSIZE and time.time()-self.R['last_seed']>0.1:
            self.R['reseedcnt']+=1
            s=b''
            for i in range(32):
                if 2**i % self.R['reseedcnt']==0:
                    s+=sha256(p[i]).hexdigest()
                    p[i]=b''
            self.R['generator'].Reseed(s)
            self.R['last_seed']=time.time()
        return self.R['generator'].Pseudo_Randomdata(n)

    #加入随机事件
    def AddRandomEvent(self,s,i,e):
        #s:源编号范围  i:池子编号范围
        #e:时间数据,字符串。
        assert 1<=len(str(e))<=32
        assert 0<=s<=255
        assert 0<=i<=31
        p = self.R['P']
        temp_s = "%02x" %s
        temp_e = "%02x" %len(str(e))
        p[i]=p[i]+a2b_hex(temp_s)+a2b_hex(temp_e)+str(e)
        #print str(p[i])

    def KeyboardEvent(self):
        id = 0
        dev = InputDevice('/dev/input/event1')
        while 1:
            select([dev],[],[])
            for event in dev.read():
                #print "code:%s value:%s" % (event.code, event.value)
                if event.code!=0:
                    self.AddRandomEvent(id,id%32,time.time())
                    #print event.value
                    if event.value == 16:
                        raw_input()
                        self.ExitFlag=1
                        break

    def MouseEvent(self):
        id =1
        dev = InputDevice('/dev/input/event2')
        while 1:
            select([dev],[],[])
            for event in dev.read():
                #print "code:%s value:%s" % (event.code, event.value)
                if event.code!=0:
                    self.AddRandomEvent(id,id%32,time.time())

    def display_R(self):
        print "reseedcnt is %d" % int(self.R['reseedcnt'])
        print "last_seed is %s" % str(self.R['last_seed']) 
    
    def Change_Flag(self):
        if self.ExitFlag==0:
           self.ExitFlag=1
        else:
           self.ExitFlag=0

if __name__ == "__main__":
    #this section just for test
    test = Accumulator()
    while test.ExitFlag==0:
        pass
    print str(test.R['P'])
    print "-----end-----"
