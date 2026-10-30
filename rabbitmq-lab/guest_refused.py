#!/usr/bin/env python3
"""Try to connect as guest/guest through the machine's non-loopback
address, the way a remote machine would. RabbitMQ's default rule
(loopback_users.guest = true) refuses guest from anywhere but
localhost; this script prints whatever the refusal looks like.

Usage: guest_refused.py HOST
"""
import sys

import pika

host = sys.argv[1]
params = pika.ConnectionParameters(
    host=host, port=5672, virtual_host='/',
    credentials=pika.PlainCredentials('guest', 'guest'),
    connection_attempts=1, socket_timeout=5, blocked_connection_timeout=5)
try:
    conn = pika.BlockingConnection(params)
    print('CONNECTED - the refusal did not happen')
    conn.close()
except Exception as exc:  # the refusal is the lesson; print it whole
    print(f"refused: {type(exc).__name__}: {exc}")
