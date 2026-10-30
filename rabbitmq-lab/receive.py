#!/usr/bin/env python3
"""Take one message off the 'intake' queue and acknowledge it."""
import pika

conn = pika.BlockingConnection(pika.ConnectionParameters(
    host='127.0.0.1', port=5672, virtual_host='printshop',
    credentials=pika.PlainCredentials('pressop', 'presspass')))
ch = conn.channel()
ch.queue_declare(queue='intake', durable=True)
method, props, body = ch.basic_get(queue='intake', auto_ack=False)
if method is None:
    print('queue empty')
else:
    print(f"received: {body.decode()} (redelivered={method.redelivered})")
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print('acknowledged')
conn.close()
