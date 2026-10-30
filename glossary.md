# Glossary

The terms of this guide, in the order
you met them rather than the alphabet's.

**Message broker** — A program that
accepts messages from producers, holds
them, and delivers them to consumers,
so the two never have to meet.

**Message** — The unit that travels:
a body of bytes plus properties (such
as delivery mode) and a routing key.
The broker does not read the body.

**Producer** — A program that creates
messages and publishes them to an
exchange.

**Consumer** — A program subscribed to
a queue, receiving messages from it
and (usually) acknowledging them.

**AMQP** — Advanced Message Queuing
Protocol, the wire protocol RabbitMQ
speaks with clients; this guide uses
AMQP 0-9-1.

**Exchange** — The sorting office: it
receives published messages and copies
them into queues according to its type
and its bindings.

**Direct exchange** — Routes to queues
whose binding key exactly matches the
message's routing key.

**Fanout exchange** — Routes to every
bound queue, ignoring routing keys.

**Topic exchange** — Routes by pattern
matching on the routing key, with `*`
(one word) and `#` (any words)
wildcards.

**Routing key** — The label a producer
puts on a message for the exchange to
sort by; on the default exchange it
is simply the queue's name.

**Binding** — A rule connecting an
exchange to a queue, carrying a key
where the exchange type uses one.

**Default exchange** — The built-in
exchange named `""`, to which every
queue is automatically bound under its
own name.

**Queue** — A first-in, first-out
buffer inside a vhost that holds
messages until a consumer takes them.

**Durable** — A property of queues and
exchanges: the declaration survives a
broker restart. Says nothing about the
messages by itself.

**Persistent message** — A message
published with `delivery_mode=2`,
written to disk so it can be restored
after a restart — into a durable
queue.

**Virtual host (vhost)** — A separate
tenancy inside one broker, with its
own exchanges, queues and permissions.
The broker starts with one, `/`.

**Acknowledgement (ack)** — The
consumer's receipt: work finished, the
broker may delete the message.

**Unacked** — The state of a message
delivered to a consumer but not yet
acknowledged; still the broker's
responsibility.

**Redelivered** — The flag on a message
being delivered again after a previous
consumer failed to ack it.

**Prefetch** — The limit on how many
unacked messages a consumer may hold
at once; `prefetch_count=1` is the
fair-dispatch setting for work queues.

**Dead-letter exchange** — An exchange
that receives messages rejected or
expired in a queue, for inspection
instead of silent loss. (Named, not
configured, in this guide.)

**Node** — One running RabbitMQ broker
— an Erlang VM — addressed by a name
such as `rabbit@localhost`.

**rabbitmqctl** — The command-line
administration tool that talks to the
node: status, users, permissions,
listings.

**Management plugin** — The optional
component adding the HTTP API and web
interface on port 15672.

**Tag** — A label on a user
(`management`, `administrator`, and
others) that gates operator surfaces
such as the management API, separately
from vhost permissions.

**pika** — The standard Python client
library for RabbitMQ, used by this
guide's programs.
