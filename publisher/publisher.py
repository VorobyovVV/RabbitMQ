import pika
import time
import json

params = pika.URLParameters('amqp://user:password@rabbitmq/')
connection = pika.BlockingConnection(params)
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)

try:
    while True:
        message = json.dumps({"operation": "sum", "data": [1, 2, 3]})
        channel.basic_publish(exchange='',
                              routing_key='task_queue',
                              body=message,
                              properties=pika.BasicProperties(
                                  delivery_mode=2,  # make message persistent
                              ))
        print(" [x] Sent %r" % message)
        time.sleep(1)
except KeyboardInterrupt:
    connection.close()
