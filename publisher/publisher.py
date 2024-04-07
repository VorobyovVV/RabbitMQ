import pika
import time
import json

params = pika.URLParameters('amqp://user:password@rabbitmq/')
connection = pika.BlockingConnection(params)
channel = connection.channel()

# Создание DLQ
dlq_name = 'dlq_task_queue'
channel.queue_declare(queue=dlq_name, durable=True)

# Создание основной очереди с указанием DLQ
args = {
    'x-dead-letter-exchange': '',  # Используем default exchange
    'x-dead-letter-routing-key': dlq_name  # Направляем сообщения в DLQ
}
channel.queue_declare(queue='task_queue', durable=True, arguments=args)

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
