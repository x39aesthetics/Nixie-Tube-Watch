#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  main.py
#  
#  Copyright 2023  <x39@raspberrypi>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import RPi.GPIO as GPIO
import time
import math
import random
import signal
import sys

#Clock/Watch definitions
secs = 0
initTime = int(time.perf_counter())
clockOffset = 0
mode = 0
illum = 1
blinkCount = 0
#Stopwatch Declarations
stopSecs = 0
stopRun = 0
stopPause = 0
stopMinsTen = 0
stopMinsOne = 0
stopSecsTen = 0
stopSecsOne = 0
stopOffset = 0
#Timer definitions
tmrSecs = 0
tmrRun = 0
tmrMinsTen = 0
tmrMinsOne = 0
tmrSecsTen = 0
tmrSecsOne = 0
tmrElapsed = 0
tmrOffset = 0
tmrInit = 0

#Bottom button, shifts between modes
def mode_shift(channel):
    global mode 
    global blinkCount
    mode=(mode+1)%4
    blinkCount = 0
    print('Mode shift')

#Second from bottom button, increments minutes and resets stopwatch    
def left_button(channel):
    global stopRun
    global stopSecs
    global stopMinsTen
    global stopMinsOne
    global stopSecsTen
    global stopSecsOne
    global stopPause
    if mode == 0:
        global clockOffset
        clockOffset = clockOffset + 60
    if mode == 1:
        global tmrInit
        tmrInit = tmrInit + 60
    if mode == 2 and stopRun == 0:
        stopSecs = 0
        stopMinsTen = 0
        stopMinsOne = 0
        stopSecsTen = 0
        stopSecsOne = 0
        stopPause = 0

#Third from bottom button, increments hours and starts/stops stopwatch/timer
def right_button(channel):
    global stopRun
    global stopOffset
    global stopPause
    global blinkCount
    global tmrRun
    global tmrOffset
    global tmrElapsed
    if mode == 0:
        global clockOffset
        clockOffset = clockOffset + 3600
    if mode == 1:
        if tmrRun == 1:
            tmrElapsed = tmrInit - tmrSecs
            tmrRun = 0
            blinkCount = 0 
        else:
            tmrOffset = int(time.perf_counter())
            tmrRun = 1
    if mode == 2:
        if stopRun == 1:
            stopPause = stopSecs
            stopRun = 0
            blinkCount = 0
        else:
            stopOffset = int(time.perf_counter())
            stopRun = 1

#Top button        
def illum_button(channel):
    global illum
    illum = (illum+1)%2

# Pin definitions
#   Tube selectors
hten = 14
hone = 15
mten = 18
mone = 23
#   Digit selector
pinA = 25
pinB = 7
pinC = 8
pinD = 12
#   Input buttons
pinL = 4
pinM = 27
pinN = 22
pinO = 10

# Pin setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(hten, GPIO.OUT)
GPIO.setup(hone, GPIO.OUT)
GPIO.setup(mten, GPIO.OUT)
GPIO.setup(mone, GPIO.OUT)
GPIO.setup(pinA, GPIO.OUT)
GPIO.setup(pinB, GPIO.OUT)
GPIO.setup(pinC, GPIO.OUT)
GPIO.setup(pinD, GPIO.OUT)

GPIO.setup(pinL, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(pinM, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(pinN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(pinO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.add_event_detect(pinL, GPIO.FALLING, callback=mode_shift, bouncetime=150)
GPIO.add_event_detect(pinN, GPIO.FALLING, callback=left_button, bouncetime=150)
GPIO.add_event_detect(pinO, GPIO.FALLING, callback=right_button, bouncetime=150)
GPIO.add_event_detect(pinM, GPIO.FALLING, callback=illum_button, bouncetime=150)

GPIO.output(pinA, GPIO.LOW)
GPIO.output(pinB, GPIO.LOW)
GPIO.output(pinC, GPIO.LOW)
GPIO.output(pinD, GPIO.LOW)
GPIO.output(hten, GPIO.LOW)
GPIO.output(hone, GPIO.LOW)
GPIO.output(mten, GPIO.LOW)
GPIO.output(mone, GPIO.LOW)


# B2D Table
B2D = [ [GPIO.LOW,GPIO.LOW,GPIO.LOW,GPIO.LOW],
        [GPIO.LOW,GPIO.LOW,GPIO.LOW,GPIO.HIGH],
        [GPIO.LOW,GPIO.LOW,GPIO.HIGH,GPIO.LOW],
        [GPIO.LOW,GPIO.LOW,GPIO.HIGH,GPIO.HIGH],
        [GPIO.LOW,GPIO.HIGH,GPIO.LOW,GPIO.LOW],
        [GPIO.LOW,GPIO.HIGH,GPIO.LOW,GPIO.HIGH],
        [GPIO.LOW,GPIO.HIGH,GPIO.HIGH,GPIO.LOW],
        [GPIO.LOW,GPIO.HIGH,GPIO.HIGH,GPIO.HIGH],
        [GPIO.HIGH,GPIO.LOW,GPIO.LOW,GPIO.LOW],
        [GPIO.HIGH,GPIO.LOW,GPIO.LOW,GPIO.HIGH] ]

# General Display Function, is fed the value each digit should be as well as an enable bit
#   The enable is so that blinking functions can operate at a similar rate as continuous 
#   displays, as otherwise the waiting done by the CPU is lost
def display(d1, d2, d3, d4, enableDisp):
    GPIO.output(mone, enableDisp)
    GPIO.output(pinA, B2D[d4][3])
    GPIO.output(pinB, B2D[d4][2])
    GPIO.output(pinC, B2D[d4][1])
    GPIO.output(pinD, B2D[d4][0])
    time.sleep(.002)
    GPIO.output(mone, GPIO.LOW)
    time.sleep(.001)
        
    GPIO.output(mten, enableDisp)
    GPIO.output(pinA, B2D[d3][3])
    GPIO.output(pinB, B2D[d3][2])
    GPIO.output(pinC, B2D[d3][1])
    GPIO.output(pinD, B2D[d3][0])
    time.sleep(.002)
    GPIO.output(mten, GPIO.LOW)
    time.sleep(.001)
          
    GPIO.output(hone, enableDisp)
    GPIO.output(pinA, B2D[d2][3])
    GPIO.output(pinB, B2D[d2][2])
    GPIO.output(pinC, B2D[d2][1])
    GPIO.output(pinD, B2D[d2][0])
    time.sleep(.002)
    GPIO.output(hone, GPIO.LOW)
    time.sleep(.001)
          
    GPIO.output(hten, enableDisp)
    GPIO.output(pinA, B2D[d1][3])
    GPIO.output(pinB, B2D[d1][2])
    GPIO.output(pinC, B2D[d1][1])
    GPIO.output(pinD, B2D[d1][0])
    time.sleep(.002)
    GPIO.output(hten, GPIO.LOW)
    time.sleep(.001)  


# Stopwatch Display Function
#   The only difference here is that the minsTen, minsOne, and secsTen digits are turned
#   off when initially zeroed
def displayStopwatch(d1, d2, d3, d4, enableDisp):
    GPIO.output(pinA, B2D[d4][3])
    GPIO.output(pinB, B2D[d4][2])
    GPIO.output(pinC, B2D[d4][1])
    GPIO.output(pinD, B2D[d4][0])
    GPIO.output(mone, enableDisp)
    time.sleep(.002)
    GPIO.output(mone, GPIO.LOW)
    time.sleep(.001)
        
    GPIO.output(pinA, B2D[d3][3])
    GPIO.output(pinB, B2D[d3][2])
    GPIO.output(pinC, B2D[d3][1])
    GPIO.output(pinD, B2D[d3][0])
    if(d1==0 and d2==0 and d3==0):
        GPIO.output(mten, GPIO.LOW)
    else:
        GPIO.output(mten, enableDisp)
    time.sleep(.002)
    GPIO.output(mten, GPIO.LOW)
    time.sleep(.001)
          
    GPIO.output(pinA, B2D[d2][3])
    GPIO.output(pinB, B2D[d2][2])
    GPIO.output(pinC, B2D[d2][1])
    GPIO.output(pinD, B2D[d2][0])
    if(d1==0 and d2==0):
        GPIO.output(hone, GPIO.LOW)
    else:
        GPIO.output(hone, enableDisp)
    time.sleep(.002)
    GPIO.output(hone, GPIO.LOW)
    time.sleep(.001)
          
    GPIO.output(pinA, B2D[d1][3])
    GPIO.output(pinB, B2D[d1][2])
    GPIO.output(pinC, B2D[d1][1])
    GPIO.output(pinD, B2D[d1][0])
    if(d1==0):
        GPIO.output(hten, GPIO.LOW)
    else:
        GPIO.output(hten, enableDisp)
    time.sleep(.002)
    GPIO.output(hten, GPIO.LOW)
    time.sleep(.001)  


def clean():
    for x in range(3):
        for y in range(10):
            display(y, (y+2)%10, (y+4)%10, (y+6)%10, GPIO.HIGH)
            
try:
    while True:
                
        secs = int(time.perf_counter())-initTime+clockOffset
        secsone = secs%10
        secsten = int((secs%60-secsone)/10)
            
        # minutes
        mins = int(math.floor(secs/60)%60)
        minsOne = mins%10
        minsTen = int((mins-minsOne)/10)
        # hours
        hrs = int(math.floor(secs/3600)%24)
        hrsOne = hrs%10
        hrsTen = int((hrs-hrsOne)/10)
        
        if stopRun == 1:
            stopSecs = int(time.perf_counter()) - stopOffset + stopPause
        stopSecsOne = stopSecs%10
        stopSecsTen = int((stopSecs%60-stopSecsOne)/10)
        stopMins = int(math.floor(stopSecs/60)%100)
        stopMinsOne = stopMins%10
        stopMinsTen = int((stopMins-stopMinsOne)/10)
        
        if tmrRun == 0:
            tmrSecs = tmrInit-tmrElapsed
        if tmrRun == 1:
            tmrSecs = tmrInit + tmrOffset - int(time.perf_counter()) - tmrElapsed
            if tmrSecs <= 0:
                tmrRun = 0 
                tmrSecs = 0
                tmrInit = 0
        tmrSecsOne = tmrSecs%10
        tmrSecsTen = int((tmrSecs%60-tmrSecsOne)/10)
        tmrMins = int(math.floor(tmrSecs/60)%60)
        tmrMinsOne = tmrMins%10
        tmrMinsTen = int((tmrMins-tmrMinsOne)/10)
        
        if illum == 1:
            if mode == 0:
                display(hrsTen, hrsOne, minsTen, minsOne, GPIO.HIGH)
            if mode == 1:
                if tmrRun == 0:
                    if tmrSecs == 0:
                        display(tmrMinsTen, tmrMinsOne, tmrSecsTen, tmrSecsOne, GPIO.HIGH)
                    if tmrSecs != 0:
                        blinkCount = (blinkCount+1)%73
                        if blinkCount < 42:
                            display(tmrMinsTen, tmrMinsOne, tmrSecsTen, tmrSecsOne, GPIO.HIGH)
                        else:
                            display(tmrMinsTen, tmrMinsOne, tmrSecsTen, tmrSecsOne, GPIO.LOW)
                if tmrRun == 1:
                    display(tmrMinsTen, tmrMinsOne, tmrSecsTen, tmrSecsOne, GPIO.HIGH)
            if mode == 2:
                if stopRun == 0:
                    if stopSecs != 0:
                        blinkCount = (blinkCount+1)%73
                        if (blinkCount < 42):
                            displayStopwatch(stopMinsTen, stopMinsOne, stopSecsTen, stopSecsOne, GPIO.HIGH)
                        else:
                            displayStopwatch(stopMinsTen, stopMinsOne, stopSecsTen, stopSecsOne, GPIO.LOW)
                    else:
                        displayStopwatch(stopMinsTen, stopMinsOne, stopSecsTen, stopSecsOne, GPIO.HIGH)
                if stopRun == 1:
                    displayStopwatch(stopMinsTen, stopMinsOne, stopSecsTen, stopSecsOne, GPIO.HIGH)
            if mode == 3:
                clean()
            
        

except KeyboardInterrupt:
    GPIO.output(hten, GPIO.LOW)
    GPIO.output(hone, GPIO.LOW)
    GPIO.output(mten, GPIO.LOW)
    GPIO.output(mone, GPIO.LOW)
    GPIO.cleanup()
GPIO.cleanup()
