#!/usr/bin/env python3
"""A work-queue consumer with manual acknowledgements.

Usage: worker.py NAME

prefetch_count=1 means the broker will not hand this worker a second
message while one is unacknowledged. The ack is sent only after the
(simulated) work finishes, so if this process dies mid-task the broker
still holds the message as unacked and will redeliver it elsewhere.
"""
import sys
import time

import pika

name = sys.argv[1] if len(sys.argv) > 1 else 'worker'
conn = pika.BlockingConnection(pika.ConnectionParameters(
    host='127.0.0.1', port=5672, virtual_host='printshop',
    credentials=pika.PlainCredentials('pressop', 'presspass')))
ch = conn.channel()
ch.queue_declare(queue='task_queue', durable=True)
ch.basic_qos(prefetch_count=1)


def on_message(channel, method, properties, body):
    text = body.decode()
    job = text.split('|')[0].strip()
    print(f"[{name}] received: {text} (redelivered={method.redelivered})",
          flush=True)
    time.sleep(text.count('.'))  # one dot = one second of "work"
    print(f"[{name}] done: {job}", flush=True)
    channel.basic_ack(delivery_tag=method.delivery_tag)


ch.basic_consume(queue='task_queue', on_message_callback=on_message)
print(f"[{name}] waiting for tasks", flush=True)
ch.start_consuming()
