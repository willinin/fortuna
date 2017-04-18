#encoding:utf-8
from generator import *
from accumulator import *
from seedmanager import *
import sys,os
import optparse

icon =  """\033[1;32m
     _____          _
     |  ___|__  _ __| |_ _   _ _ __   __ _
     | |_ / _ \| '__| __| | | | '_ \ / _` |
     |  _| (_) | |  | |_| |_| | | | | (_| |
     |_|  \___/|_|   \__|\__,_|_| |_|\__,_|

   code-date:2017-04-17  author:willin\033[0m"""

if __name__ == "__main__":
    #this section is for gui
    print '\033[1;33m--------------------bupt homework--------------------------\033[0m'
    print icon
    #print '\033[1;33m-----------------------------------------------------------\033[0m'
    print '''\033[1;35m  usage:
          -g x or --generator x for generating the number of random-number-Bytes
          -n y or --number y for the times of generating random-number
          -u or --update for update seedfile
          -G for display the status of G in generator
          -R for display the status of R in accumulator\033[0m'''
    print '\033[1;33m--------------------version 2.0----------------------------\033[0m'

    print '\033[1;34m   [+]Initing  the generator! \033[0m'
    generator = Generator()
    generator.InitializeGenerator()
    print '\033[1;34m   [+]Initing the  accumulator! \033[0m'
    accumulator = Accumulator(generator)
    print '\033[1;34m   [+]Initing  the seedmanager! \033[0m'
    seedmanager =Seed_Manager(accumulator)
    #print '\033[1;33m-----------------------------------------------------------\033[0m'

    #this is section is for ui
    parse=optparse.OptionParser()
    parse.add_option('-g','--generator',dest='gen',action='store',type=int,default=0)
    parse.add_option('-u','--update',dest='up',action='store_true')
    parse.add_option('-G',dest='status_g',action='store_true')
    parse.add_option('-R',dest='status_r',action='store_true')
    parse.add_option('-n','--number',dest='num',action='store',type=int,default=1)
    options,args=parse.parse_args()
    #print '\n'
    for i in range(options.num):
       print '\033[1;33m-----------------------------------------------------------\033[0m'
       print "Please keyBoarding randomly!"
       while accumulator.ExitFlag==0:
             continue
       print '\n'
       if options.gen!=0:
          print "the hex of random-number is: "
          print b2a_hex(accumulator.RandomData(options.gen))
       #print '\n'
       if options.up == True:
          seedmanager.UpdateSeedFile()
       if options.status_g == True:
          generator.display_G()
       if options.status_r == True:
          accumulator.display_R()
       accumulator.Change_Flag()
    

    print '\033[1;33m--------------------end and bye--------------------------\033[0m'
    sys.exit(0)
