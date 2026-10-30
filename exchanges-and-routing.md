# Exchanges and Routing

**Outcome:** you can declare exchanges
and queues, bind them together, and
predict — before publishing — exactly
which queues a message will reach.

**Check:** transcript **t04** declares
everything below through the
management API and then gets each
message back out. Cover the results
column and predict each one from the
bindings first; that prediction is
the skill this chapter teaches.

Chapter 5 used the default exchange,
which sorts by queue name and teaches
nothing about sorting. Real systems
declare their own exchanges so the
*sender* does not need to know the
queue names — only the routing rules.

The lab builds a small print-shop
layout in the `printshop` vhost, using
the management HTTP API (chapter 9
covers the API itself; here it is just
the tool for the job). Two exchanges:

- `tickets`, type **direct**: job
  tickets sorted by a routing key.
- `announce`, type **fanout**: shop
  notices copied to everyone.

Three durable queues: `press-a`,
`press-b`, and `counter`. Four
bindings wire them up:

| Exchange | Queue | Routing key |
|---|---|---|
| tickets | press-a | `urgent` |
| tickets | counter | `info` |
| announce | press-a | *(none — fanout ignores keys)* |
| announce | press-b | *(none)* |

Declaring through the API is a `PUT`
per object and a `POST` per binding;
each answered `201` in the lab. The
same declarations exist in every
client library (`exchange_declare`,
`queue_declare`, `queue_bind` in
pika), and in `rabbitmqctl`'s absence
they are the program's job at startup.

Now publish three messages and watch
the rules work:

1. To `tickets` with key `urgent`:
   `JOB 1042 | posters x200 | due
   Friday`. The API answers
   `{"routed": true}`.
2. To `tickets` with key `info`:
   `JOB 1043 | counter cards x500`.
3. To `announce`, no key:
   `SHOP NOTICE | press 2 down for
   cleaning at 18:00`.

Reading the queues back with the API's
`get` (chapter 9) shows the sorting
was exact:

- `press-a` held the **urgent job**
  (exchange `tickets`, routing key
  `urgent`, delivery mode 2 — every
  field survived) and then the **shop
  notice**.
- `press-b` held only the **notice** —
  fanout copied it to both presses,
  and no ticket reached it, because no
  binding connects `tickets` to it.
- `counter` held only the **info
  job**.

Two lessons hide in that small table.
The first is that an exchange never
guesses: a message to `tickets` with
a key nobody bound — say `routine` —
would be dropped, silently, unless
the publisher asked for it back (the
`mandatory` flag) or an alternate
exchange is configured. Routing is a
contract written in bindings, and
`rabbitmqctl list_bindings` (t08)
prints the whole contract whenever
you need to audit it. The second is
that fanout is not "send to many
queues" as a special feature — it is
the same machinery with the key check
switched off, which is why the notice
needed no key at all.

The lab did not declare a **topic**
exchange; its rule is the direct rule
with patterns — a binding key such as
`press.*` or `#.urgent` — and it is
the natural next step when two keys
stop being enough. Chapter 14 is
honest that it is described here, not
demonstrated.
