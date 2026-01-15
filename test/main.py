import pika
import struct

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost')) # Connect to the local broker
channel = connection.channel()

# Declare a queue named 'hello'
channel.queue_declare(queue='sendQueue',durable=True)

# Publish a message to the default exchange with the 'hello' routing key
channel.basic_publish(exchange='',
                      routing_key='sendQueue',
                      body=struct.pack("<BB",15,0))
print(" [x] Sent")

connection.close()
