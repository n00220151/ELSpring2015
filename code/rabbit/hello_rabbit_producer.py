import pika, sys

#establish connection to broker
#using default vhost '/' because none specified
credentials = pika.PlainCredentials("guest", "guest")
conn_params = pika.ConnectionParameters("137.140.8.122", credentials = credentials)
conn_broker = pika.BlockingConnection(conn_params)

#obtain channel
channel = conn_broker.channel()

#declare exchange
channel.exchange_declare(exchange = "hello-exchange",
                         type = "direct",
                         passive = False, #True if only obtaining information
                         durable = True, 
                         auto_delete = False)

#create plaintext message
msg = sys.argv[1]
msg_props = pika.BasicProperties()
msg_props.content_type = "text/plain"

#publish message
channel.basic_publish(body = msg, 
                      exchange = "hello-exchange", 
                      properties = msg_props, 
                      routing_key = "hola")
