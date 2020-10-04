#!/usr/bin/env python3
from time import sleep
from datetime import datetime, date, time
from colorama import init, Fore, Back, Style
#from picamera import PiCamera
import emoji
init()


def infoMsg(text):
    now = datetime.now()
    timePrint = str('%02d' % now.hour) + ":" + str('%02d' %
                                                   now.minute) + ":" + str('%02d' % now.second)
    print(Fore.BLUE+"ℹ"+Fore.RESET + Fore.GREEN +
          (" ["+timePrint+'] ')+Fore.RESET+" "+text)


infoMsg(Fore.RED+"Raspberry"+Fore.RESET+Fore.GREEN +
        "PI"+Fore.RESET+"-timelapse "+emoji.emojize(":camera:")+" is loading...")
infoMsg("Made by Terje Nesthus ("+Fore.LIGHTBLUE_EX+"terje"+Fore.RESET +
        Fore.BLUE+"@"+Fore.RESET+Fore.LIGHTBLUE_EX+"nesthus.no"+Fore.RESET+")")
