# The Moving Parts

**Outcome:** you can trace a message
from the program that sends it to the
program that processes it, naming each
part it passes through.

**Check:** trace `JOB 1042` on paper:
producer → exchange → binding → queue
→ consumer → acknowledgement. If any
arrow is missing in your trace, that
is the part to re-read.

A message crosses five named things on
its way through RabbitMQ. None of them
is complicated; the discipline is in
not muddling them up.

**Producer.** The program that creates
a message and sends it to RabbitMQ. A
producer never sends to a queue
directly (with one shortcut, below);
it sends to an **exchange**, naming a
**routing key**.

**Exchange.** A sorting office. An
exchange receives a message, looks at
its type and the message's routing
key, and copies the message into zero
or more queues according to its
**bindings**. The exchange types are
the sorting rules:

- **direct** — deliver to queues bound
  with a routing key that matches the
  message's key exactly.
- **fanout** — deliver to every bound
  queue, ignoring keys entirely.
- **topic** — deliver by pattern:
  binding keys may contain wildcards
  (`press.*.urgent` and the like).
- **headers** — deliver by matching
  message headers instead of the key;
  rare in practice.

**Binding.** The rule that connects an
exchange to a queue, with a key where
the exchange type uses one. No
binding, no delivery: a message whose
key matches no binding is dropped by
the exchange (the publisher can ask to
be told, but by default it vanishes —
chapter 6 shows a publish report
`"routed": true`, which is the API
confirming at least one queue took
it).

**Queue.** A first-in, first-out
buffer inside the broker that holds
messages until a consumer takes them.
Queues live inside a **virtual host**
(see below). A queue may be **durable**
(its declaration survives a broker
restart) or transient. Messages in it
may individually be **persistent**
(marked to be written to disk) or not —
durability and persistence are two
separate switches, and chapter 11
shows you need both.

**Consumer.** A program connected to
the broker, subscribed to a queue.
RabbitMQ pushes messages to it (or it
pulls them one at a time). With
**prefetch** set, the broker limits
how many unacknowledged messages a
consumer may hold at once — the fair-
dispatch knob for chapter 7's work
queues.

**Acknowledgement (ack).** The
consumer's receipt: "done, you may
delete it." Until the ack arrives, the
message is **unacked** — delivered but
still the broker's responsibility. If
the consumer's connection drops with
unacked messages outstanding, the
broker puts them back at the front of
the queue, marked **redelivered**, and
hands them to the next consumer. This
single mechanism is most of why people
trust a broker with real work.

**Virtual host (vhost).** A separate
tenancy inside one broker: its own
exchanges, queues and permissions,
invisible to other vhosts. The broker
starts with one vhost, `/`. The lab
creates one called `printshop` and
does everything inside it.

**The shortcut.** Every queue is
automatically bound to the built-in
**default exchange** (its name is the
empty string) with the queue's own
name as the key. Publishing to the
default exchange with
`routing_key='intake'` therefore
delivers straight to the queue called
`intake` — which is why the first
programs in chapter 5 can skip the
sorting office entirely, and why
`rabbitmqctl list_bindings` shows a
row for every queue with an empty
source name (transcript t08).

Who runs all this? One Erlang program
— the **node** — plus two small
neighbours on the same machine: the
command-line tool **rabbitmqctl**,
which talks to the node over the same
Erlang machinery, and (in this guide)
the **management plugin**, which adds
an HTTP API and a web interface on
port 15672. The node listens for AMQP
clients on port **5672**. Those two
numbers are RabbitMQ's own defaults,
used throughout the lab.
