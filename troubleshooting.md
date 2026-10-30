# Troubleshooting

**Outcome:** the failures this lab
actually met, in the order you are
likely to meet them, each with the
reading that fixed it.

**Check:** every error message quoted
here appears verbatim in a transcript;
find it there before trusting the
chapter.

## "unable to perform an operation on node"

`rabbitmqctl` cannot reach the node.
The diagnostics block under the error
lists the usual causes. In the lab
(t02) the cause was timing: the
command ran while the node was still
on its first boot. Fixes in order:
wait and `rabbitmqctl await_startup`;
confirm the node is running at all
(`rabbitmq-diagnostics -q ping`);
confirm both processes share a node
name and an Erlang cookie — a cookie
mismatch presents exactly like a dead
node, and the diagnostics print the
cookie hash of the *tool* for
comparison.

## "could not bind to distribution port 25672"

A second RabbitMQ is being started
while one is already running (t02).
There is one node per node name per
machine. Find it (`ps` for `beam.smp`,
or `rabbitmqctl status`), decide
which copy should live, and stop the
other with `rabbitmqctl stop` — not
by killing the VM, which leaves the
next start to recover from an unclean
shutdown.

## "Not management user" / "Not administrator user" / "User not authorised to access virtual host"

Three refusals, three layers (chapter
10, t03). *Not management user*: the
account has no tag — `rabbitmqctl
set_user_tags <user> management`.
*Not administrator user*: the endpoint
is admin-only and the account is not
an administrator. *User not authorised
to access virtual host*: no permission
row for that vhost — `rabbitmqctl
list_permissions -p <vhost>` shows
what exists. And `Not_Authorized`
with a 401 is the plainest of all:
the password is wrong.

## "My message vanished"

Work the contract in order. Did the
publish actually route? (The API
answers `"routed"`; AMQP publishers
need the `mandatory` flag to hear
about failures.) Does a binding exist
for that exchange, queue and key —
`rabbitmqctl list_bindings` prints
them all (t08). Was the consumer
running with **auto-ack** and crashed
(chapter 8)? Was the queue
**non-durable** and the broker
restarted, or the message
**non-persistent** in a durable queue
(chapter 11)? Vanishing is almost
always one of these five, and each
has a different fix.

## "The dashboard says 0 but messages exist"

Statistics lag (chapter 9, t04). The
management counters sample on an
interval. Ground truth is
`rabbitmqctl list_queues` or an API
`get`. Wait six seconds before
declaring a queue empty in either
direction.

## "The worker gets all the jobs" / "jobs pile up unacked"

The first is prefetch: without
`basic_qos(prefetch_count=1)` the
broker delivers round-robin regardless
of who is busy (chapter 7). The
second is the opposite side of the
same coin — consumers holding messages
they never ack: check
`messages_unacknowledged` in
`list_queues`, and `rabbitmqctl
list_consumers` for who is holding
them. Killing the stuck consumer is a
legitimate fix: chapter 8 guarantees
its unacked work comes back.

## "guest works locally but not from the other machine"

That is not a fault; it is
`loopback_users` doing its documented
job (chapter 10). Create a real user
with a real password for anything
off-box, and leave `guest` to
localhost.
