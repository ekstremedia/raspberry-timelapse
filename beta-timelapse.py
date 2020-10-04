#!/usr/bin/env python3
from time import sleep
from datetime import datetime, date, time
from colorama import init, Fore, Back, Style
import emoji
init()

# Define variables
red = "\033[1;31;38m"
green = "\033[1;32;38m"
endcolor = "\033[0m"


def successMsg(text):
    print(green+text+endcolor)


def infoMsg(text):
    now = datetime.now()
    timePrint = str('%02d' % now.hour) + ":" + str('%02d' %
                                                   now.minute) + ":" + str('%02d' % now.second)
    print(Fore.BLUE+"ℹ"+Fore.RESET + Fore.GREEN +
          (" ["+timePrint+'] ')+Fore.RESET+" "+text)


infoMsg(Fore.RED+"Raspberry"+Fore.RESET+Fore.GREEN +
        "PI"+Fore.RESET+"-timelapse "+emoji.emojize(":camera:")+" is loading...")
infoMsg("Made by Terje Nesthus ("+Fore.BLUE+"terje"+Fore.RESET +
        Fore.LIGHTBLUE_EX+"@"+Fore.RESET+Fore.BLUE+"nesthus.no"+Fore.RESET+")")
infoMsg("test")
