import pika
import json

def callback(ch, method, properties, body):
    message = json.loads(body)
    print(" [x] Received %r" % message)
    try:
        if message["operation"] == "sum":
            result = sum(message["data"])
            print(f"Result: {result}")
        else:
            raise Exception("Unknown operation")
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f"Error processing message: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

params = pika.URLParameters('amqp://user:password@rabbitmq/')
connection = pika.BlockingConnection(params)
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)

channel.basic_consume(queue='task_queue', on_message_callback=callback, auto_ack=False)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
