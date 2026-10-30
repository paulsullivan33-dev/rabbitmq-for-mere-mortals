# Work Queues

**Outcome:** several workers share one
queue of jobs so that work spreads
across them, no job is given to two
workers at once, and a slow job does
not block the fast ones behind it.

**Check:** transcript **t06** queues
three jobs and runs two workers in
sequence. Even without starting a
second worker yourself, the shape to
recognise is: one queue, many
consumers, the broker keeping count.

The print shop's counter keeps taking
job tickets; the presses work at
different speeds. The pattern for this
is the **work queue**: one durable
queue (`task_queue`), one producer
adding jobs, and any number of
consumers taking them off. RabbitMQ
hands the messages out in turn —
round-robin — to whichever consumers
are connected.

The lab's producer, `new_task.py`,
publishes tickets whose trailing dots
stand for seconds of work, so the
timing is visible without any real
printing:

```bash
python new_task.py "JOB 2001 | banners x12 ........" \
                   "JOB 2002 | stickers x50 ." \
                   "JOB 2003 | posters x20 .."
```

and the worker, `worker.py`, sleeps
one second per dot before acking. Two
details in the worker matter more
than everything else in this chapter:

**Prefetch of one.** The worker sets
`basic_qos(prefetch_count=1)`: the
broker may not give it a second
message while it holds an
unacknowledged one. Without this, the
broker happily pushes every job to
whichever worker connected first —
round-robin by *delivery*, not by
*availability* — and a worker can sit
on a pile of jobs it has not started
while another idles. With prefetch 1,
a busy worker is skipped until it
acks, which is what "spread the work
fairly" actually requires.

**Ack after the work, not before.**
The worker acknowledges only when the
sleep finishes — when, in a real
system, the printing is done and
committed. Chapter 8 shows what that
buys; here just note the cost of the
opposite habit: ack on receipt and a
crash loses the job exactly as if
there were no broker at all.

In the lab's run (t06), worker **W1**
takes the eight-second JOB 2001 —
and is killed three seconds in,
before chapter 8 picks the story up.
Worker **W2** then receives all three
jobs in order and finishes them:
eight seconds for the banners again
(redelivery restarts the work, it does
not resume it), one for the stickers,
two for the posters.

That restart-from-scratch is worth
underlining, because it decides how
you design jobs. A consumer can be
given the same message twice — once
before dying, once after — so work
that must not happen twice (charging
a card) has to be made safe against
duplicates by the application, for
example by recording job numbers it
has already completed. The broker
guarantees delivery; *exactly-once*
effect is your problem, and every
honest messaging system will tell you
the same.
