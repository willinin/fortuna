#encoding:utf-8
from generator import *
from accumulator import *
import threading

class Seed_Manager(object):
    FileName='./seed/seed'
    size=64
    accumulator ='' #加速器的实例

    def __init__(self,acc):
        self.accumulator = acc
        self.ReadSeedFile()
        pthread = threading.Thread(target=self.autoUpdate)
        pthread.start()

    #读种子文件,打开失败则新建
    def ReadSeedFile(self):
        try:
           fp=open(self.FileName,'rb')
           s=fp.read(64)
           if len(s)!=64:
              fp.close()
              self.WriteSeedFile()
        except:
           fp=open(self.FileName, 'wb')
           #self.accumulator.R['generator'].Reseed('123456790')
           fp.write(self.accumulator.RandomData(64))
           fp.close()
        return s
  
    #写种子文件
    def WriteSeedFile(self):
        with open(self.FileName, 'wb') as fp:
            fp.write(self.accumulator.RandomData(64))
        fp.close()

    #更新种子文件
    def UpdateSeedFile(self):
        s = open(self.FileName).read()
        assert len(s) == 64
        self.accumulator.R['generator'].Reseed(s)
        with open(self.FileName, 'wb') as fp:
            fp.write(self.accumulator.RandomData(64))
        fp.close()

    #每隔10分钟自动存储种子文件
    def autoUpdate(self):
        currenttime=time.time()
        while 1:
            if time.time()-currenttime >=600:
                self.UpdateSeedFile()
                currenttime=time.time()
