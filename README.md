# RabbitMQ for Mere Mortals

Two programs that need to cooperate
usually meet in one of two ways: one
calls the other directly and waits, or
one leaves the work somewhere both can
reach. **RabbitMQ is the somewhere.** It
is a **message broker**: a program that
accepts messages from **producers**,
holds them in **queues**, and hands them
to **consumers** when they are ready.
The producer does not wait for the work
to happen, and the consumer does not
care who produced the message or when.
That loosening — hand the job over and
walk away — is the whole idea, and it
is why brokers sit underneath order
systems, print pipelines, notification
services and a great deal of plumbing
you never see.

This guide explains how RabbitMQ moves
a message from one program to another,
how to install it and check that it is
really running, and how to put it to
work: a first message sent and received
by small Python programs, an exchange
that routes job tickets to the right
queue, a work queue shared between
workers, and the acknowledgement that
makes "the worker died" a nuisance
instead of a lost job. Then it proves
the promise the whole design rests on:
stop the broker, start it again, and
the durable work is still there.

The lab that wrote this guide ran the
real thing: **RabbitMQ 3.12.1** (the
Ubuntu 24.04 package) on
**Erlang/OTP 25**, on one small Linux
machine, with everything on loopback.
Against it the lab created a fictional
print shop's world — a virtual host, a
user, queues named for presses — and
moved invented job tickets through it:
routed by a direct exchange, broadcast
by a fanout one, pulled back out with
the words intact, worked on by a
consumer that was **killed in the
middle of a job** so the broker had to
hand that job to a second consumer,
and finally frozen into a restart to
see which messages survived. Every one
of those runs is kept in
`rabbitmq-lab/` as a transcript, and
the small Python programs are there
too.

What the lab could not do, it did not
fake. It ran **one node**, so clusters
and high availability are described,
not demonstrated. It drove the
management **API** with `curl` — the
same API the web interface uses — but
never clicked through the interface
itself. It sent no message over TLS
and federated with no other broker.
Chapter 14 lists every such limit
plainly, and `criteria.md` keeps the
ledger of what was run and what was
only read about.

## What it doesn't cover

Running a RabbitMQ **cluster** in
production, sizing one for heavy load,
or tuning Erlang for throughput — this
guide's node is a teaching node on a
small shared machine. Other client
languages: the worked examples are
Python (with the **pika** library) and
`curl`; the ideas transfer, the code
does not. And the print shop is
invented — its job tickets are
fixtures, chosen so every number in
the guide can be checked by hand.

## How to use this guide

Read chapter 1 for the model and
chapter 2 before installing anything —
knowing which part holds a message at
each moment turns later confusion into
a named problem. Chapters 3 and 4 get
you a running broker and the checks
that prove it. Chapter 5 sends your
first message in the same sitting.
Chapters 6 to 8 are the working core:
routing, work queues, and the
acknowledgement habit that keeps work
from vanishing. The lab's transcripts
live in `rabbitmq-lab/` (t00 to t09),
and its programs — `send.py`,
`receive.py`, `new_task.py`,
`worker.py`, `guest_refused.py` — are
in the same folder.

---

## Part of the series

This guide is one of the [For Mere Mortals](https://paulsullivan33-dev.github.io/mere-mortals/) guides: plain-language guides to the tools programmers and makers use.

Related guides:

- [MQTT for Mere Mortals](https://paulsullivan33-dev.github.io/mqtt-for-mere-mortals/)
- [APIs for Mere Mortals](https://paulsullivan33-dev.github.io/api-for-mere-mortals/)
- [Redis for Mere Mortals](https://paulsullivan33-dev.github.io/redis-for-mere-mortals/)
- [Docker for Mere Mortals](https://paulsullivan33-dev.github.io/docker-for-mere-mortals/)

## License

The writing in this guide is licensed under [CC BY 4.0](https://github.com/paulsullivan33-dev/rabbitmq-for-mere-mortals/blob/main/LICENSE). Code examples and lab scripts are licensed under the [MIT License](https://github.com/paulsullivan33-dev/rabbitmq-for-mere-mortals/blob/main/LICENSE-CODE).
