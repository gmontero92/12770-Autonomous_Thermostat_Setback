#import some library
import pandas as pd
import numpy as np
import os
import time
from time import sleep
from datetime import datetime, timedelta
#import some library
import pandas as pd
import numpy as np
import os
import time
from time import sleep
from datetime import datetime, timedelta
import RPi.GPIO as GPIO
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import dht11
import sys

#create a parameter to get GPIO reading
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(25,GPIO.IN) #data button
GPIO.setup(16,GPIO.IN) #stop button
GPIO.setup(18,GPIO.OUT) #led
instance_in = dht11.DHT11(pin = 14)
instance_out = dht11.DHT11(pin = 23)

#define operation and sampling frequency
fop=4#Hz
Ts=5#s
delta_Ts=timedelta(seconds=Ts)
fs = 1/Ts#Hz
n=fop/fs
while GPIO.input(16):
    if not GPIO.input(25):
        while not GPIO.input(25):
            GPIO.output(18,True) #Turn on the light
        count=0
        #create empty dataframe csv
        current_time =datetime.now()
        file = open("/home/pi/Documents/Autonomous thermostat setback/02 Collected Data/"+str(current_time)+".csv", "a")
        if os.stat("/home/pi/Documents/Autonomous thermostat setback/02 Collected Data/"+str(current_time)+".csv").st_size == 0:
                file.write("Date','Time,'in_temp','out_temp'\n")
        beginning=datetime.now()
        while GPIO.input(25):
            current_delta=datetime.now()-beginning
            if current_delta>=count*delta_Ts:
                GPIO.output(18,False) #Turn off the light
                result = instance_in.read()
                temp_in  = result.temperature
                result = instance_out.read()
                temp_out  = result.temperature
                current_time =datetime.now()
                file.write(str(current_time)+","+str(temp_in)+","+str(temp_out)+"\n")
                count+=1
                GPIO.output(18,True) #Turn on the light            
        GPIO.output(18,False) #Turn off the light
        file.close()
        while not GPIO.input(25):
            GPIO.output(18,False) #Turn off the light
    time.sleep(1/fop)

for i in range(0,5):
    GPIO.output(18,True) #Turn on the light
    time.sleep(0.2)
    GPIO.output(18,False) #Turn off the light
    time.sleep(0.2)import RPi.GPIO as GPIO
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import dht11
import sys

#create empty dataframe csv
#col_list = ['Timestamp','in_temp','out_temp']
#df = pd.DataFrame(columns = col_list)


#create a parameter to get GPIO reading
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(25,GPIO.IN) #data button
GPIO.setup(16,GPIO.IN) #stop button
GPIO.setup(18,GPIO.OUT) #led

#define function for each sensor
fop=4#Hz
Ts=5#s
fs = 1/Ts#Hz
n=fop/fs
#duration = 5 
#duration_adj = timedelta(days = 0, seconds = duration*1.35,microseconds = 0,milliseconds = 0,minutes = 0, hours = 0,weeks = 0)
begining =datetime.now()

instance_in = dht11.DHT11(pin = 14)
instance_out = dht11.DHT11(pin = 23)

Inifinite_run=True

while GPIO.input(16):
    if not GPIO.input(25):
        while not GPIO.input(25):
            GPIO.output(18,True) #Turn on the light
        count=n
        #create empty dataframe csv
        current_time =datetime.now()
        file = open("/home/pi/Documents/autonomous_setback/03 Measured data/"+str(current_time)+".csv", "a")
        if os.stat("/home/pi/Documents/autonomous_setback/03 Measured data/"+str(current_time)+".csv").st_size == 0:
                file.write("Date,Time,'in_temp','out_temp'\n")    
        while GPIO.input(25):
            if count==n:
                result = instance_in.read()
                temp_in  = result.temperature
                result = instance_out.read()
                temp_out  = result.temperature
                current_time =datetime.now()
                file.write(str(current_time)+","+str(temp_in)+","+str(temp_out)+"\n")
                count=0
            count+=1
            time.sleep(1/fop)
        GPIO.output(18,False) #Turn off the light
        file.close()
        while not GPIO.input(25):
            GPIO.output(18,False) #Turn off the light
    time.sleep(1/fop)

for i in range(0,5):
    GPIO.output(18,True) #Turn on the light
    time.sleep(0.2)
    GPIO.output(18,False) #Turn off the light
    time.sleep(0.2)
