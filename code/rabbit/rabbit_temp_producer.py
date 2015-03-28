import pika, sys, os, glob

# initialize temp probe
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28-*')[0]
device_file = device_folder + '/w1_slave'

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
      return str(temp_c)

# establish connection to broker
# using default vhost '/' because none specified
credentials = pika.PlainCredentials("forcel", "forcel")
conn_params = pika.ConnectionParameters("137.140.8.121", credentials = credentials)
conn_broker = pika.BlockingConnection(conn_params)

# obtain channel
channel = conn_broker.channel()

# declare exchange
channel.exchange_declare(exchange = "hello-exchange",
                         type = "direct",
                         passive = False, #True if only obtaining information
                         durable = True, 
                         auto_delete = False)

# create temp message
msg = read_temp()
msg_props = pika.BasicProperties()
msg_props.content_type = "text/plain"

# publish message
channel.basic_publish(body = msg, 
                      exchange = "hello-exchange", 
                      properties = msg_props, 
                      routing_key = "hola")
