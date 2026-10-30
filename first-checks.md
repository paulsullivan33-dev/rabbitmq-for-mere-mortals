# First Checks

**Outcome:** three independent proofs
that the node is up — its own status
report, its listeners on the expected
ports, and a diagnostics ping — each
runnable whenever you doubt it later.

**Check:** all three commands below
appear in transcript **t01** and
**t08** with their lab output. Run
them on your install and compare the
shape, not the numbers.

## 1. Ask the node about itself

```bash
rabbitmqctl await_startup
rabbitmqctl status
```

`await_startup` waits until the node
has finished booting (on a first boot
the lab's node answered "Still
booting" twice before it was ready —
that patience is built into the
command). The status report's first
block is the identity card:

```text
Status of node rabbit@localhost ...
RabbitMQ version: 3.12.1
Node name: rabbit@localhost
Erlang configuration: Erlang/OTP 25 [erts-13.2.2.5] ...
```

Three facts to read off it. The
**RabbitMQ version** (3.12.1 in the
lab) tells you which documentation
applies. The **node name** —
`rabbit@` plus a host name — is how
every command-line tool addresses it;
if your tools ever say they cannot
contact a node, this name is the first
suspect. And the **Erlang/OTP
version** (25 in the lab) matters
because RabbitMQ supports specific
OTP ranges per release; a mismatch
here is a classic cause of a node
that installs but will not start.

Further down, the same report lists
the enabled plugins — the lab's shows
`rabbitmq_management` and the helpers
it pulls in — and the data directory,
which is where the node's durable
state lives (chapter 11 leans on it).

## 2. Look at the listeners

```bash
ss -tlnp | grep -E '5672|15672'
```

The lab's node shows **5672** (AMQP,
the client protocol) listening on all
interfaces, and **15672** (management
HTTP) on `127.0.0.1` only, because the
lab configuration bound it there. On a
default install both listen on all
interfaces — which is one reason
chapter 10 insists on replacing the
default `guest` account's reach: by
design, `guest` can only log in from
localhost, whatever the listeners do.

## 3. Diagnostics

```bash
rabbitmq-diagnostics -q ping
rabbitmq-diagnostics check_running
```

The lab's answers: `Ping succeeded`
and "RabbitMQ on node rabbit@localhost
is fully booted and running"
(transcript **t08**). There is also
`rabbitmqctl report`, which bundles
status, listings and environment into
one long text — the thing to attach
when asking for help.

## The failure you will meet first

Run `rabbitmqctl status` against a
node that is stopped (or still
booting) and you get a long error
beginning:

```text
Error: unable to perform an operation on node 'rabbit@localhost'.
```

with a diagnostics section listing the
likely causes — node unreachable,
cookie mismatch, node not running.
The lab hit this verbatim on its first
attempt by asking too early
(transcript **t02**), and the fix was
unsexy: wait, then ask again. The
second classic is starting a second
copy of the server while one is
already up, which fails with
`could not bind to distribution port
25672, it is in use by another node` —
also in t02, also self-inflicted.
Chapter 15 returns to both.
