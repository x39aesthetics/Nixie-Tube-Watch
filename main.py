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

# Variable definitions
secs = 0

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
        
# Random Delay Table
rdelay = [0,0,0,0,0,0,0.005,0.003,0,0,0,0,0.0025,0.001,0.001,0.002,0.00,0.0005,0.0012,0.0007,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]


def display(d1, d2, d3, d4):
    GPIO.output(mone, GPIO.HIGH)
    GPIO.output(pinA, B2D[d4][3])
    GPIO.output(pinB, B2D[d4][2])
    GPIO.output(pinC, B2D[d4][1])
    GPIO.output(pinD, B2D[d4][0])
    time.sleep(.002)
    GPIO.output(mone, GPIO.LOW)
    time.sleep(.001+rdelay[int(random.random())%30])
        
    GPIO.output(mten, GPIO.HIGH)
    GPIO.output(pinA, B2D[d3][3])
    GPIO.output(pinB, B2D[d3][2])
    GPIO.output(pinC, B2D[d3][1])
    GPIO.output(pinD, B2D[d3][0])
    time.sleep(.002)
    GPIO.output(mten, GPIO.LOW)
    time.sleep(.001+rdelay[int(random.random())%30])
          
    GPIO.output(hone, GPIO.HIGH)
    GPIO.output(pinA, B2D[d2][3])
    GPIO.output(pinB, B2D[d2][2])
    GPIO.output(pinC, B2D[d2][1])
    GPIO.output(pinD, B2D[d2][0])
    time.sleep(.002)
    GPIO.output(hone, GPIO.LOW)
    time.sleep(.001+rdelay[int(random.random())%30])
          
    GPIO.output(hten, GPIO.HIGH)
    GPIO.output(pinA, B2D[d1][3])
    GPIO.output(pinB, B2D[d1][2])
    GPIO.output(pinC, B2D[d1][1])
    GPIO.output(pinD, B2D[d1][0])
    time.sleep(.002)
    GPIO.output(hten, GPIO.LOW)
    time.sleep(.001+rdelay[int(random.random())%30])
      
try:
    while True:
        secs = int(time.perf_counter())
        # minutes
        mins = int(math.floor(secs/60)%60)
        minsone = mins%10
        minsten = int((mins-minsone)/10)
        # hours
        hrs = int(math.floor(secs/3600)%24)
        hrsone = hrs%10
        hrsten = int((hrs-hrsone)/10)
        print( hrsten, hrsone, minsten, minsone, secs)
        display(hrsten, hrsone, minsten, minsone)    
except KeyboardInterrupt:
    GPIO.output(hten, GPIO.LOW)
    GPIO.output(hone, GPIO.LOW)
    GPIO.output(mten, GPIO.LOW)
    GPIO.output(mone, GPIO.LOW)
    GPIO.cleanup()
