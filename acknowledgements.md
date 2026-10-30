# Acknowledgements and Not Losing Work

**Outcome:** you understand what an
acknowledgement really promises, what
happens to unacknowledged messages
when a consumer dies, and how to see
a redelivery happen with your own
eyes.

**Check:** transcript **t06** is this
chapter, run: a worker killed mid-job,
a second worker receiving the same
job marked `redelivered=True`, and
the queue ending empty.

An acknowledgement is a receipt the
consumer sends when it has *finished*
with a message. Until it arrives, the
message sits in the queue in a third
state — not waiting, not gone, but
**unacked**: delivered to a consumer,
still counted as the broker's
responsibility. You can see the three
states in the queue listings as
`messages_ready`, `messages_unack`
(or combined in `messages`).

The rule that makes the system
trustworthy is short: **if a
consumer's connection or channel
closes while it holds unacked
messages, the broker returns those
messages to the queue**, ahead of
undelivered ones, marked
**redelivered**. No timer, no
administrator, no recovery procedure.
The consumer that picks the message
up next sees the flag and knows it
may be looking at work someone else
started.

The lab proved it as rudely as
possible. Worker W1 took JOB 2001 —
eight seconds of simulated work — and
was sent `kill -9` after three
seconds: no cleanup, no final ack, the
rudest death a process can have. The
broker noticed the closed connection,
took the unacked message back, and
when worker W2 connected it received:

```text
[W2] received: JOB 2001 | banners x12 ........ (redelivered=True)
[W2] done: JOB 2001
```

then the two jobs behind it, each
`redelivered=False`, each acked, and
the queue ended empty. Nothing was
lost, and nothing had to be rescued
by hand. That transcript, t06, is the
centre of this guide: most of what a
broker is *for* is in those two lines.

The mirror-image mistake is
**auto-ack** (`auto_ack=True`, or the
API's `ack_requeue_true` habits):
the message is considered dealt with
the moment it is delivered, so a
crash a second later loses it for
good. Auto-ack has honest uses —
fire-and-forget metrics where a lost
sample costs nothing — but choosing
it should be a decision, not a
default you inherited from a tutorial.

Two refinements complete the picture.
A consumer can also **reject** a
message on purpose: `basic_nack` (or
`basic_reject`) with `requeue=False`
drops it — or, if the queue has a
**dead-letter exchange** configured,
sends it there for inspection, which
is how grown-up systems quarantine
poison messages instead of redelivering
them forever. And a message that keeps
being requeued by failing consumers
will loop; the redelivered flag, plus
a retry counter in the message
headers, is how applications notice
and stop. The lab demonstrated the
core mechanism only; dead-lettering
is described here, and chapter 14
says so.
