#!/usr/bin/python

import os
import glob
import time
import csv

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28-*')[0]
device_file = device_folder + '/w1_slave'

def get_time():
   return time.strftime("%Y-%m-%d %H:%M")

def read_temp_raw():
   f = open(device_file, 'r')
   lines = f.readlines()
   f.close()
   return lines

def read_temp():
   lines = read_temp_raw() # read temp
   # continue reading until temp is available
   while lines[0].strip()[-3:] != 'YES':
      time.sleep(0.2)
      lines = read_temp_raw()
   equals_pos = lines[1].find('t=')
   if equals_pos != -1:
      temp_string = lines[1][equals_pos+2:]
      temp_c = float(temp_string) / 1000.0
      temp_f = temp_c + 9.0 / 5.0 + 32.0
      return temp_c

temp_c = read_temp()
temp_f = temp_c * 9.0 / 5.0 + 32.0

# append to temp list
fd = open('temp.csv', 'a')
fd.write(get_time()+","+str(temp_c)+","+str(temp_f)+"\n")
fd.close()

# write to latest temp file
fd = open('latestTemp.csv', 'w')
fd.write(get_time()+","+str(temp_c)+","+str(temp_f))
fd.close()
