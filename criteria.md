# Writing criteria for this guide

Every "for Mere Mortals" guide is written to the same nine-point
standard, so a reader who trusts one can trust the rest. Here it
is, with the verification notes for this particular guide below.

1. **Fix it first.** Reader outcomes lead, not action items: each
   chapter opens by naming the outcome it delivers, shows a check
   the reader can run to confirm they got it, and a reasonable
   reader finishes able to state what was done, what it means,
   and what to try next.
2. **Plain language.** Short sentences, everyday vocabulary,
   technical terms defined on first use. No slang, and no
   idioms that only make sense in one country — the reader may
   be translating as they go.
3. **No dead ends.** A guide never tells the reader to do
   something it cannot show them how to verify. Every claim a
   reader relies on — an install, a command, an output — is
   something this guide demonstrates or clearly labels
   documented-only below.
4. **Live-verified where it matters.** Procedures are run for
   real in the guide's lab wherever the build machine allows it,
   and the transcripts kept in the repository are the evidence.
   What could not be run is listed honestly below, never
   presented as if it had been.
5. **General audiences.** Nothing in this guide — examples,
   fixtures, names, addresses — is modelled on any particular
   reader or author's real life, network, or organisations.
   The lab's print shop, its job tickets and its passwords are
   all invented.
6. **Standalone.** A reader needs this guide, its lab, and
   nothing else. Where another guide would genuinely help, it
   is pointed to once, by name, and the chapter still completes
   without it.
7. **Honest about limits.** Chapter 14 names what the tool
   cannot do and what the lab did not run: one node only, no
   TLS, classic queues only, sampled statistics, duplicates as
   a fact of life, and a guest-refusal the sandbox network
   would not let the broker demonstrate.
8. **The ethics rule is in the text, early.** A broker moves
   other programs' data without reading it, which makes access
   control the moral centre of the tool: chapter 10 builds a
   named user with scoped permissions before any client
   connects, states the guest account's loopback restriction
   and the reason for it, and no chapter uses anyone's real
   messages — every payload is an invented job ticket.
9. **Builds clean.** The site builds with MkDocs in strict mode
   with no warnings, and a fresh reader following the chapters
   in order reaches the stated outcome of each.

## Verification notes for this guide

The build machine is a 2-CPU, 7.9 GB Ubuntu 24.04 sandbox,
shared with other work while the lab ran (the node idled at
roughly 150 MB of memory; timings are therefore ranges, and
the guide says so). RabbitMQ **3.12.1** — the Ubuntu noble
package `rabbitmq-server 3.12.1-1ubuntu1.7` — and its
**Erlang/OTP 25** runtime were fetched as eighteen download-only
`.deb` files (36.1 MB) using a lab-private apt state and
unpacked unmodified with `dpkg -x` into the lab tree; the
system package state was never touched. One adaptation was
needed and is disclosed in chapter 3: Debian's `erl` launcher
hardcodes `/usr/lib/erlang`, so a five-line shim set `ROOTDIR`
and `BINDIR` for the extracted tree and called `erlexec`
directly. The node ran with `RABBITMQ_BASE` and friends pointed
into the lab directory, the management listener bound to
loopback, and `total_memory_available_override_value` set to
1 GB so the shared machine's memory would not trip its alarms.
Ports were RabbitMQ's own: AMQP **5672**, management **15672**.
All transcripts live in `rabbitmq-lab/`; the client programs
are `rabbitmq-lab/send.py`, `receive.py`, `new_task.py`,
`worker.py` and `guest_refused.py`.

Run for real, with transcripts as evidence:

- Download and extraction of the packages, the Erlang shim,
  and OTP 25 answering (t00).
- Plugin enablement, node startup with `await_startup`
  patience, the full `rabbitmqctl status` (RabbitMQ 3.12.1,
  Erlang/OTP 25 [erts-13.2.2.5]), and the two listeners on
  5672 and 127.0.0.1:15672 (t01).
- Vhost `printshop` and user `pressop` created with
  `rabbitmqctl`, permissions granted and listed; the three
  management refusals in sequence — `Not management user`
  before the tag, a 401 `Not_Authorized` for a wrong password,
  `User not authorised to access virtual host` for the
  default vhost — and `Not administrator user` for an
  admin-only endpoint after the `management` tag was set
  (t03).
- The whole routing layout declared through the management
  API (two exchanges, three queues, four bindings, all
  `201`s), three publishes each answered `{"routed": true}`,
  and every message fetched back with payload, exchange,
  routing key and delivery mode intact: direct `urgent`
  reached only `press-a`, direct `info` only `counter`, the
  fanout notice reached both presses (t04). The same
  transcript records the statistics lag honestly: queue
  counters read 0 immediately after publishing, and exactly
  right after six seconds.
- pika 1.4.4 (installed from PyPI into a lab venv): `send.py`
  published `JOB 1050` through the default exchange and
  `receive.py` returned it byte-identical with
  `redelivered=False`, then found the queue empty (t05).
- The work queue end to end: three tasks queued, worker W1
  killed with `kill -9` three seconds into the eight-second
  task, worker W2 receiving that task with
  `redelivered=True`, finishing it, and finishing the two
  behind it in order (t06).
- Persistence: a durable `archive` queue holding two
  messages was taken through a full node stop and start;
  the delivery_mode 2 ticket survived word for word and the
  delivery_mode 1 control was gone; every durable queue,
  the vhost, the user, the exchanges and the bindings all
  returned (t07, and the post-restart listings in t08).
- Diagnostics and listings: `rabbitmq-diagnostics -q ping`
  ("Ping succeeded"), `check_running`, the exchange and
  binding tables including the default exchange's implicit
  per-queue bindings (t08).
- The guest rule from the allowed side: `loopback_users`
  read back from the running node as `[<<"guest">>]`, the
  guest `whoami` over loopback, and an AMQP connection as
  guest over 127.0.0.1 accepted (t03, t05).

Documented only — described from the project's documentation,
not run, and the text does not claim otherwise:

- Clustering, quorum queues and high availability; the lab
  ran a single node with classic queues.
- TLS for AMQP and the management API, and client certificate
  verification.
- Federation and the shovel plugin.
- The management web interface as a clicked, visual
  experience; its API is the proven surface.
- Topic and headers exchanges (direct and fanout are the
  demonstrated types), dead-letter exchanges, message TTL
  and queue-length limits.
- The guest refusal from a non-loopback address: the
  sandbox's network intercepts connections to the machine's
  own external address before they reach the broker, so the
  attempt is recorded verbatim as a client timeout
  (t05) and the broker's refusal behaviour is described
  from the documentation in chapter 10.
- Production sizing, memory/disk alarm tuning, and publisher
  confirms as a power-loss guarantee.
- Client libraries other than pika, and the neighbour tools
  of chapter 13 (MQTT brokers, Redis, Kafka, cloud queues,
  task frameworks) — characterised, not run.

Failures kept verbatim, because they teach: `rabbitmqctl`
run before the first boot finished ("unable to perform an
operation on node 'rabbit@localhost'"), and a second server
started over a running one ("could not bind to distribution
port 25672, it is in use by another node") — both in t02 and
both in chapter 15. The node was stopped cleanly at the end
of the lab (t09).

Fixtures are this guide's own and deliberately generic: a
fictional print shop ("printshop", presses A and B, a counter)
and job tickets with invented numbers, products and due days —
no real customer, order or organisation appears anywhere.
