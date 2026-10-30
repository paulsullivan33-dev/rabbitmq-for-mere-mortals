#!/usr/bin/env python3
"""Send one job ticket to the 'intake' queue through the default exchange.

The default exchange routes by queue name: routing_key='intake' delivers
to the queue called 'intake'. delivery_mode=2 asks for the message to be
written to disk (it still needs a durable queue to survive a restart).
"""
import pika

conn = pika.BlockingConnection(pika.ConnectionParameters(
    host='127.0.0.1', port=5672, virtual_host='printshop',
    credentials=pika.PlainCredentials('pressop', 'presspass')))
ch = conn.channel()
ch.queue_declare(queue='intake', durable=True)
body = 'JOB 1050 | leaflets x300 | due Monday'
ch.basic_publish(exchange='', routing_key='intake', body=body,
                 properties=pika.BasicProperties(delivery_mode=2))
print(f"sent: {body}")
conn.close()
