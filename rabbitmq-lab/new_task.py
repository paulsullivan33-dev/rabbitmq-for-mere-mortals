#!/usr/bin/env python3
"""Publish job tickets to the durable 'task_queue' work queue.

Usage: new_task.py "JOB 2001 | banners x12 ........" "JOB 2002 | ..."
Each trailing dot is one second of simulated work for the worker, so a
reader can watch a long task outlive the worker that started it.
"""
import sys

import pika

conn = pika.BlockingConnection(pika.ConnectionParameters(
    host='127.0.0.1', port=5672, virtual_host='printshop',
    credentials=pika.PlainCredentials('pressop', 'presspass')))
ch = conn.channel()
ch.queue_declare(queue='task_queue', durable=True)
for body in sys.argv[1:]:
    ch.basic_publish(exchange='', routing_key='task_queue', body=body,
                     properties=pika.BasicProperties(delivery_mode=2))
    print(f"queued: {body}")
conn.close()
