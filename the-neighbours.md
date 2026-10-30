# The Neighbours

**Outcome:** you can place RabbitMQ
among the tools that resemble it, and
name the job each neighbour does
better — so "should this be a queue?"
gets an honest answer.

**Check:** for each neighbour, say
which of this guide's chapters it
replaces or removes. If the answer is
"none, it is a different shape", that
is the correct answer for most of
this list.

**MQTT** (see the series' MQTT guide).
A protocol and broker family for
small devices: tiny clients, topics
instead of exchanges and queues, and
quality-of-service levels instead of
acks you manage. If your senders are
sensors and your messages are
readings, MQTT is the lighter tool.
RabbitMQ can even speak it, through a
plugin — but a dedicated MQTT broker
is simpler when telemetry is the
whole job. The overlap is real and
the centre of gravity differs: MQTT
moves *state*, RabbitMQ moves *work*.

**Redis** (see the Redis guide).
An in-memory data store whose lists
and streams can be pressed into
queue service, and often are, inside
projects already running it. As a
broker it is the apprentice: no
exchanges, no routing, ack semantics
you assemble yourself from streams'
consumer groups. If you already run
Redis and your queueing is modest, it
may be all you need; RabbitMQ is what
you reach for when the queueing *is*
the point.

**Kafka.** The other famous name, and
a different animal: a distributed
*log*. Messages are not deleted on
delivery; they stay, in order, for a
retention period, and consumers track
their own position and can re-read
history. For event streams at scale —
millions of records, replay,
analytics — Kafka's model wins. For
"hand this job to a worker and tell
me when it is done", its machinery is
heavier than the problem, and
per-message acknowledgement is not
its shape. RabbitMQ deletes on ack;
Kafka forgets on schedule.

**A plain database table.** The
neighbour nobody lists: an `jobs`
table, a `status` column, workers
polling for `status='new'`. It works,
it is transactional with the rest of
your data, and at small scale it may
be the right answer. What you give up
is everything chapters 6 to 8 got for
free — routing, fair dispatch,
redelivery on death — each of which
you will rebuild, slightly worse,
over the years. The honest comparison
is not "table or broker" but "which
of these mechanisms do I want to
maintain".

**Cloud queues (SQS and friends).**
The same work-queue idea as a rented
service: no node to run, per-message
pricing, someone else's 3 a.m.
problem. The concepts in this guide
transfer almost one-to-one — queues,
visibility timeouts instead of unacked
states, redelivery counts — which is
one reason to learn them on a broker
you can inspect.

**Celery, Sidekiq and friends.** Task
frameworks that sit *on top of* a
broker (very often RabbitMQ): they
add job serialisation, scheduling,
retries with backoff, and result
storage, in exchange for adopting
their model of a task. They are
RabbitMQ's customers, not its rivals —
when you outgrow hand-rolled workers,
they are where chapter 7's pattern
graduates to.
