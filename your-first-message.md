# Your First Message

**Outcome:** a small Python program
sends a job ticket into RabbitMQ and
a second program takes it out and
reads it back, word for word.

**Check:** transcript **t05** shows
the three runs: the send, the receive
(the payload identical), and a second
receive that finds the queue empty.

The lab's client library is **pika**,
the standard Python client for
RabbitMQ, installed into a private
virtual environment
(`pip install pika`; the lab got
pika 1.4.4). Both programs connect the
same way: to port 5672 on loopback, as
the lab's user `pressop`, into the
`printshop` virtual host — the user
and vhost are chapter 10's work,
created with `rabbitmqctl` before any
client connected.

`send.py` (kept in `rabbitmq-lab/`):

```python
conn = pika.BlockingConnection(pika.ConnectionParameters(
    host='127.0.0.1', port=5672, virtual_host='printshop',
    credentials=pika.PlainCredentials('pressop', 'presspass')))
ch = conn.channel()
ch.queue_declare(queue='intake', durable=True)
body = 'JOB 1050 | leaflets x300 | due Monday'
ch.basic_publish(exchange='', routing_key='intake', body=body,
                 properties=pika.BasicProperties(delivery_mode=2))
```

Three ideas are doing the work.
`queue_declare` makes sure the queue
exists (declaring an existing queue
with the same properties is harmless,
which is why both programs do it).
Publishing to `exchange=''` uses the
**default exchange**, the shortcut
from chapter 2: the routing key is the
queue's name, so this message lands in
`intake`. And `delivery_mode=2` marks
the message **persistent** — a promise
chapter 11 cashes in.

`receive.py` uses `basic_get` to pull
one message rather than subscribing:

```python
method, props, body = ch.basic_get(queue='intake', auto_ack=False)
```

and acknowledges it by hand with
`basic_ack`. The lab's output:

```text
$ python receive.py
received: JOB 1050 | leaflets x300 | due Monday (redelivered=False)
acknowledged
```

The payload is byte-for-byte what
`send.py` published — the broker
stored and forwarded it without
reading it. `redelivered=False` is the
broker saying "this is the first time
this message has been delivered to
anyone"; chapter 8 is about the day
it says `True`. Run `receive.py`
again and it prints `queue empty`:
the message is gone, because the ack
told the broker its job was done.

That is the whole loop — connect,
declare, publish, get, ack — and
everything after this chapter is
refinement: better sorting (chapter
6), fair sharing (chapter 7), and
proof that the loop survives rudeness
(chapters 8 and 11).
