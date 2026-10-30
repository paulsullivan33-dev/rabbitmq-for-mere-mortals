# Users and Permissions

**Outcome:** you can create a user,
give it exactly the access it needs
inside one virtual host, and read the
broker's refusals when something is
wrong — because you will have seen
each refusal once, on purpose.

**Check:** transcript **t03** is this
chapter end to end, including the
three different `not_authorised`
answers and what each one means.

RabbitMQ access control has three
layers, and most confusion comes from
treating them as one:

**1. Users and passwords.** A user is
a name with a password hash, created
with `rabbitmqctl`:

```bash
rabbitmqctl add_vhost printshop
rabbitmqctl add_user pressop presspass
```

A fresh broker has exactly one user,
`guest` (password `guest`), with
administrator rights — and one
deliberate restriction, below.

**2. Permissions per virtual host.**
For each vhost, a user gets three
regular expressions — **configure**,
**write**, **read** — matched against
the names of exchanges and queues it
may create, publish to, and consume
from:

```bash
rabbitmqctl set_permissions -p printshop pressop ".*" ".*" ".*"
```

`.*` means "any name" (the lab's lab
grant; a real system narrows these).
No row for a vhost means no access to
it at all: when the lab's `pressop`
asked the API for queues in the
default vhost `/`, the answer was
`User not authorised to access
virtual host`. And authentication is
checked before any of it — a wrong
password gets a flat
`401 {"error":"not_authorized",
"reason":"Not_Authorized"}`.

**3. Tags gate the management
plugin.** Permissions say what a user
may do over AMQP; **tags** say what
kind of operator it is. Before the
lab gave `pressop` a tag, the
management API answered its calls
with `Not management user` — even
with full permissions in its vhost.
After:

```bash
rabbitmqctl set_user_tags pressop management
```

its `whoami` answered normally, and
it could work in `printshop` through
the API — while single-object
endpoints reserved for administrators
(such as `GET /api/vhosts/printshop`)
still refused it with `Not
administrator user`. Three different
refusals, three different causes:
no tag, no admin, no vhost rights.
Reading them accurately is the whole
troubleshooting skill for this layer.

**The guest rule.** Since 2014 the
default has been
`loopback_users.guest = true`: the
built-in `guest` account may only
connect from the same machine. The
lab read the setting back from the
running node — `{ok, [<<"guest">>]}`
for `loopback_users` — and proved the
allowed side with both the API and an
AMQP connection as `guest` over
`127.0.0.1` (transcript **t05**).
Proving the refused side from inside
this sandbox defeated the lab: its
network intercepts connections to the
machine's own external address before
they reach the broker, so the attempt
is recorded verbatim as a timeout,
and the broker's actual refusal (it
closes the connection and logs that
`guest` can only connect via
localhost) is described here from the
documentation, not presented as a
lab result. The operational lesson
survives intact: on any real network,
`guest`/`guest` works only from the
broker's own machine — which is a
safety net, never a reason to leave
the account as your only admin. Make
your own administrator, set a real
password, and keep `guest` for the
day everything else is locked.
