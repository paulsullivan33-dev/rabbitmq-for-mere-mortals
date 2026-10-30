# Persistence and Restarts

**Outcome:** you can state exactly
what survives a broker restart — and
prove it — because you will have
stopped and started the node with
messages in it and read back what is
left.

**Check:** transcript **t07**: two
messages go in, the node is fully
stopped and started, and exactly one
message — the right one — comes out.

"Will my messages survive a restart?"
has a two-switch answer, and both
switches must be on:

- The **queue must be durable**.
  `durable=True` at declaration means
  the queue itself (and its bindings)
  is recreated after a restart.
- The **message must be persistent**.
  `delivery_mode=2` at publish means
  the broker writes it to disk and
  will restore it into the queue.

The four combinations behave as you
would now predict: a durable queue
full of transient messages restarts
*empty* (the queue survives, the
messages do not); persistent messages
in a transient queue are gone with
the queue. Exchanges, by the way,
have the same durable switch and no
message of their own to lose.

The lab's proof used a durable queue
called `archive` and two job tickets:

- `JOB 3001 | bound proofs x40 | keep
  until collected` — **delivery_mode
  2**.
- `JOB 3002 | scrap paper note` — the
  control, **delivery_mode 1**.

A depth check showed `messages: 2`.
Then the whole node was stopped —
`rabbitmqctl stop`, the Erlang VM
halted, not just the application —
and started again. After startup,
`rabbitmqctl list_queues -p printshop`
showed every durable queue back:
`task_queue`, `intake`, `press-a`,
`press-b`, `counter` — and `archive`
holding exactly **1** message.
Fetching it returned JOB 3001, word
for word, `delivery_mode: 2` still
attached. JOB 3002 was nowhere: the
control did its job by disappearing.

Three honest footnotes. First,
unacked messages are covered by the
same rule: a persistent message out
with a consumer at shutdown comes
back ready (and will be marked
redelivered on its next delivery).
Second, persistent means written to
disk *by the broker's schedule*, not
fsynced before every publish returns
— surviving a *broker restart* is
proven here; surviving the machine
losing power mid-write is a stronger
claim involving publisher confirms
and disk behaviour, and this guide
does not make it. Third, durability
is not backup: the node's data
directory (chapter 4 showed where it
lives) is the whole estate, and a
deleted directory loses durable
messages as finally as a deleted
database file.

What the node itself remembers across
the restart is also worth naming,
because the lab watched all of it
return: the vhost `printshop`, the
user `pressop` and its permissions,
the exchanges `tickets` and
`announce`, and every binding from
chapter 6 (compare t08's listings,
taken after the restart, with t04's
declarations). The broker's
*definitions* are durable by design —
which is why a RabbitMQ restart is
normally an anticlimax, and why the
interesting question is never "will
it come back" but "which of my
switches did I leave off".
