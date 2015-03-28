import pika

#establish connection broker
credentials = pika.PlainCredentials("forcel","forcel")
conn_params = pika.ConnectionParameters("137.140.8.122",credentials=credentials)
conn_broker = pika.BlockingConnection(conn_params)

#obtain channel
channel = conn_broker.channel()

#declare exchange
channel.exchange_declare(exchange = "hello-exchange", 
                         type = "direct", 
                         passive = False, 
                         durable = True, 
                         auto_delete = False)

#declare queue
channel.queue_declare(queue = "hello-queue")

#bind queue and exchange on "hola"
channel.queue_bind(queue = "hello-queue", 
                   exchange = "hello-exchange", 
                   routing_key = "hola")

#function to process incoming messages
def msg_consumer(channel, method, header, body):
   channel.basic_ack(delivery_tag = method.delivery_tag)    #msg ack
   if body == "quit":
      channel.basic_cancel(consumer_tag = "hello-consumer")
      channel.stop_consuming()                              #stop consuming
   else:
      print body
   return

#subscribe consumer
channel.basic_consume(msg_consumer, 
                      queue = "hello-queue", 
                      consumer_tag = "hello-consumer")

#start consuming
channel.start_consuming()
