# Limits

**Outcome:** a plain list of what this
guide did not do, what RabbitMQ itself
will not do for you, and where the
edges of both are — stated before you
meet them in production.

**Check:** every item below is either
a sentence containing "described, not
run" or a behaviour a chapter proved.
If you find a third kind of claim in
this guide, it does not belong there.

## What the lab did not run

- **Clustering and high
  availability.** One node only.
  Clusters, quorum queues (the modern
  replicated queue type; this guide
  used classic queues throughout),
  and failover are described from the
  documentation, not demonstrated.
- **TLS.** Clients and the API spoke
  plain HTTP/AMQP on loopback.
  Certificate setup, and clients
  verifying them, are not covered by
  any transcript.
- **Federation and shovel.** Moving
  messages between brokers — described
  in one paragraph here, never
  configured.
- **The management UI as a visual
  experience.** Chapter 9 drove the
  API the UI is built on; nobody
  clicked anything.
- **Topic and headers exchanges.**
  Declared types are characterised in
  chapters 2 and 6; only direct and
  fanout were exercised.
- **Dead-letter exchanges, message
  TTL, queue length limits.** Named
  where they belong (chapters 8 and
  12) as the next mechanisms to learn;
  not configured in the lab.
- **Other client languages.** Python
  with pika, and `curl`. The concepts
  transfer; no Java, Go, or .NET
  client was compiled or run.
- **The guest refusal from a remote
  address.** Chapter 10 tells this
  story in full: the setting is
  proven, the loopback success is
  proven, the sandbox's network
  intercepted the remote-side attempt
  before the broker could refuse it.

## What RabbitMQ will not do

- **It is not storage.** Queues are
  for messages in motion. Chapter 1
  said it and it bears repeating at
  the end: a queue of unprocessed
  messages is a backlog, not an
  archive.
- **It does not make work
  exactly-once.** Chapter 7:
  redelivery means duplicates are a
  fact of life; idempotent consumers
  are your responsibility.
- **It will not save you from a full
  disk or a memory alarm.** When the
  node crosses its memory watermark
  or runs low on disk, it *blocks
  publishers* rather than lose
  messages — correct behaviour that
  looks, from the outside, like the
  broker freezing. The alarms are in
  the status report; watch them.
- **Ordering is narrower than it
  looks.** A single queue delivers in
  order to a single consumer; add
  consumers, priorities, or
  redeliveries and the order becomes
  "roughly, with exceptions". Designs
  that need strict order must say so
  early and pay for it.
- **The statistics are sampled.**
  Chapter 9's polite lie is a design
  property, not a bug: management
  numbers trail the truth by seconds.
