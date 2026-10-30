# What RabbitMQ Is

**Outcome:** you can say what problem a
message broker solves, and why handing
work to a queue is different from
calling a program directly.

**Check:** by the end, explain in one
sentence what happens to a job ticket
if the program that would process it
is switched off when the ticket
arrives. (Answer, in advance: nothing
bad — the ticket waits in the queue.)

Two programs need to cooperate. A web
shop takes an order; something must
charge the card, email the customer,
tell the warehouse. The obvious way is
for the shop program to call each of
those programs directly and wait for
each answer. That works until it
doesn't: if the email program is down
for an hour, does the shop refuse
orders for an hour? If a sale makes
orders arrive ten times faster than
the warehouse program can read them,
does the shop fall over, or does the
work pile up somewhere safe?

**RabbitMQ is the somewhere safe.** It
is a **message broker** — a program
whose whole job is to accept
**messages**, hold them in **queues**,
and deliver them to other programs
when those programs are ready. The
program sending work (the **producer**)
hands RabbitMQ a message and walks
away; it does not wait, and it does
not need to know who will do the work.
The program doing the work (the
**consumer**) takes messages off the
queue at its own pace. If the consumer
is switched off, the messages wait. If
ten consumers are running, the work
spreads across them. If a consumer
dies halfway through a job, RabbitMQ
can hand that job to another one —
chapter 8 proves this with a worker
that is killed on purpose.

A message is just bytes with a small
label. RabbitMQ does not read it, does
not care whether it is JSON, a job
ticket, or a compressed image. In this
guide's lab the messages are plain
text job tickets from a fictional
print shop — `JOB 1042 | posters x200 |
due Friday` — because text lets you
see with your own eyes that what comes
out of the queue is exactly what went
in.

RabbitMQ speaks a protocol called
**AMQP** (Advanced Message Queuing
Protocol), most often version 0-9-1.
The protocol is why the moving parts
in chapter 2 have the names they do —
exchanges, routing keys, bindings —
and why client libraries exist for
nearly every programming language: the
broker and the clients only have to
agree on the wire protocol, not on
anything else. RabbitMQ itself is
written in **Erlang**, a language built
for telephone switches — systems that
must not stop — which is why the
install in chapter 3 brings an Erlang
runtime along with it.

One honest boundary before we start:
a broker is not a database. Messages
are meant to *move* — to be delivered,
processed, and acknowledged away.
RabbitMQ can hold a message safely
through a restart when you ask it to
(chapter 11 proves it), but a queue
used as permanent storage becomes a
liability: it grows, it slows, and the
messages in it are the ones nobody
processed. Use RabbitMQ to hand work
over, not to file it.

The print shop in this guide is a
stand-in for every system of that
shape: orders arriving at one counter,
presses doing work at their own pace,
a noticeboard everyone needs to see.
Wherever your own system has a counter
and a press, the same map applies.
