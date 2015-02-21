#!/usr/bin/python

import os
import glob
import time
import sqlite3 as db

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28-*')[0]
device_file = device_folder + '/w1_slave'

con = None

# return current time
def get_time():
   return time.strftime("%Y-%m-%d %H:%M")

# read raw temp data
def read_temp_raw():
   f = open(device_file, 'r')
   lines = f.readlines()
   f.close()
   return lines

# gets temperature C from raw temp data
def read_temp():
   lines = read_temp_raw() # read raw temp data
   # continue reading until temp is available
   while lines[0].strip()[-3:] != 'YES':
      time.sleep(0.2)
      lines = read_temp_raw()
   # find temperature
   equals_pos = lines[1].find('t=')
   if equals_pos != -1: # check if valid reading
      temp_string = lines[1][equals_pos+2:] # get temp from string
      temp_c = float(temp_string) / 1000.0 # convert to tempC
      return temp_c

temp_c = read_temp();
temp_f = temp_c * 9.0 / 5.0 + 32.0
time = get_time()

# write to sqlite database
try:
   con = db.connect('/home/pi/dev/git/ELSpring2015/code/temp/data/temp.db')
   cur = con.cursor()
   cur.execute("INSERT INTO temps values(?,?,?)", (time, temp_c, temp_f))
   con.commit()
   con.close()
except db.Error, e:
   print "Error %s:" % e.args[0]
   sys.exit(1)
finally:
   if con:
      con.close()

# append to temp list
fd = open('/home/pi/dev/git/ELSpring2015/code/temp/data/temp.csv','a')
fd.write(time+","+str(temp_c)+","+str(temp_f)+"\n")
fd.close()

# write to latest temp file
fd = open('/home/pi/dev/git/ELSpring2015/code/temp/data/latest_temp.csv','w')
fd.write(time+","+str(temp_c)+","+str(temp_f))
fd.close()
