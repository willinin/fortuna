#encoding:utf-8
from hashlib import sha256
from Crypto.Cipher import AES
from Crypto.Util import Counter
from Crypto import Random
from binascii import b2a_hex, a2b_hex
import math

def Expand_key(text):
  #将密钥拓展为16字节整数倍的字符串
  #这里先将数字转化为字符串
  temp = "%032X" % text
  text = a2b_hex(temp)
  length = 16
  count = len(text)
  add = length - (count % length)
  text = text + ('\0' * add)
  return text


class Generator(object):
  # G: Generator state, G = (K, C)
  G={'K':b'','C':0}

  def InitializeGenerator(self):
    self.G['K']=b''
    self.G['C']=0
    #self.G={'K':self.K,'C'=self.C}

  def Reseed(self,s):
    # s: New or additional seed
    k = sha256(self.G['K']+s).hexdigest()
    #将k转为字符串
    self.G['K']=a2b_hex(k)
    self.G['C']+=1
    #print self.G['K']

  def GenerateBlocks(self, k):
    # k: Nmber of blocks to generate
    # return r : 16进制的伪随机字符串
    assert self.G['C']!=0
    r = b''
    ctr = Counter.new(128,initial_value=self.G['C'])
    cryptor=AES.new(self.G['K'], AES.MODE_CTR,counter=ctr)
    for i in range(1,k):
      #保证分组的长度是16的整数倍,此时C是明文
      text=Expand_key(self.G['C'])
      r += cryptor.encrypt(text)
      self.G['C'] += 1
    #return b2a_hex(r)
    return r

  def Pseudo_Randomdata(self, n):
    # n: Number of bytes of random data to generate
    # r :16进制的伪随机字符串
    assert 0 <= n <= 2**20
    r = self.GenerateBlocks(int(math.ceil(n / 16)))[:n]
    self.G['K'] = self.GenerateBlocks(2)
    #return b2a_hex(r)
    return r

  def display_G(self):
      print "G['K'] is %s" %self.G['K']
      print "G['C'] is %032X" %self.G['C']
      
if __name__ == "__main__":
  #this section just for test!
  t=Generator()
  t.InitializeGenerator()
  TestSeed='123456789'
  t.Reseed(TestSeed)
  print b2a_hex(t.Pseudo_Randomdata(64))
