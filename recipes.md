# Recipes

**Outcome:** five small, complete jobs
done the way the preceding chapters
teach — each names the chapter it
stands on, so a recipe never has to
re-teach its parts.

**Check:** every recipe here was run
in the lab except where it says
otherwise; the transcripts are the
same ones the chapters cite.

## 1. A noticeboard in four calls

Declare a fanout exchange, bind two
queues, publish once, and both queues
hold the notice (chapter 6, t04):

```bash
curl -u pressop:presspass -XPUT \
  -d '{"type":"fanout","durable":true}' \
  http://127.0.0.1:15672/api/exchanges/printshop/announce
```

The pattern generalises: fanout plus
one queue per audience is the simplest
publish/subscribe there is.

## 2. Add a worker without touching the producer

Start a second copy of chapter 7's
worker with a different name:

```bash
python worker.py W3
```

Nothing is reconfigured anywhere —
that is the point of the work-queue
pattern. The broker shares the queue
between W2 and W3 from the next job
on, each worker protected by its
prefetch of 1.

## 3. Peek at a queue without consuming it

Use the API's `get` with
`"ackmode":"ack_requeue_true"`:
the messages come back *and* go back,
unacked count unchanged. It is the
safe inspection hatch for "what is
actually stuck in there" — far better
than pointing a real consumer at a
production queue to find out.

## 4. Drain a queue before decommissioning it

Read its depth with `GET
/api/queues/{vhost}/{name}` until
`messages` reaches 0 (remember the
statistics lag from chapter 9 — wait
a few seconds before declaring it
empty), let consumers finish, then
delete it with `DELETE` on the same
path. A queue deleted with messages
in it takes them with it.

## 5. The pre-flight trio

Before blaming a client, run chapter
4's checks in their short form:

```bash
rabbitmq-diagnostics -q ping
rabbitmqctl list_queues -p printshop name messages messages_unacknowledged
rabbitmqctl list_permissions -p printshop
```

Node alive, depths and unacked counts
visible, permissions as expected —
most "RabbitMQ ate my message"
reports die at one of these three.

## 6. Rotate the lab user's password

```bash
rabbitmqctl change_password pressop newpass
```

and update the clients' credentials
to match. (Described, not run: the
lab's transcripts are written against
the original password, and rotating
it mid-lab would invalidate the
evidence chain — on a real system,
rotate first and write second.)
