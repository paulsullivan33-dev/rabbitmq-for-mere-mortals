# The Management API and UI

**Outcome:** you can drive the broker
through its HTTP API — declare
objects, publish, fetch, inspect —
and you know what the web interface
is (and is not) adding on top.

**Check:** chapter 6's whole layout
was built with this API (transcript
**t04**); every call below appears
there with a real reply.

Enabling the `rabbitmq_management`
plugin (chapter 3) gives the node an
HTTP API on port **15672** and, at the
same address, a web interface. The
interface is a client of the API —
anything it shows, the API can be
asked for directly, which is why this
guide proves the API and treats the
clicking as documented-only: there
was no browser in the lab, and the
API is the surface scripts and
monitoring actually use.

Every call is ordinary HTTP with
basic authentication. The workhorse
endpoints, all under `/api`:

- `PUT /api/exchanges/{vhost}/{name}` —
  declare an exchange (a `type` and
  `durable` in the body). `PUT` both
  creates and updates, and answers
  `201` when it creates.
- `PUT /api/queues/{vhost}/{name}` —
  declare a queue, the same way.
- `POST /api/bindings/{vhost}/e/{exchange}/q/{queue}` —
  bind, with the routing key in the
  body.
- `POST /api/exchanges/{vhost}/{name}/publish` —
  publish a message; the reply
  `{"routed": true}` tells you at
  least one queue accepted it.
- `POST /api/queues/{vhost}/{name}/get` —
  fetch messages, choosing an
  `ackmode`: `ack_requeue_false`
  (take and acknowledge),
  `ack_requeue_true` (peek and put
  back), and their `reject` cousins.
  Chapter 6's payloads came back with
  every field intact — payload,
  exchange, routing key, delivery
  mode, redelivered flag.
- `GET /api/queues/{vhost}/{name}` —
  the queue object: depth, consumers,
  rates, state.
- `GET /api/overview`, `/api/nodes`,
  `/api/connections`, `/api/channels` —
  the health-and-plumbing views.

Virtual host names are URL-escaped in
paths: the default vhost `/` appears
as `%2F`. The lab's `printshop` needs
no escaping, which is one more reason
to name your own vhosts plainly.

**The counters lie politely.** Right
after the lab published three
messages, the queue objects still
reported `messages: 0` — the
management database samples statistics
on an interval rather than counting
live, and the `get` calls proved the
messages were sitting there all
along. Wait a few seconds (the lab
waited six, in t04's addendum, and
the counter then read exactly 1) or
trust `get` and `rabbitmqctl
list_queues` over the dashboard
numbers when they disagree. Anyone
who has watched a monitoring screen
"catch up" after an incident has met
the same behaviour; here it is in
miniature, with the ground truth
available to check.

One boundary the lab ran into and
chapter 10 explains: the API is
gated by **tags** as well as
permissions. The lab's user could do
everything in its own vhost once it
held the `management` tag — and
nothing at all before. Point a
browser at `http://localhost:15672/`
on a machine with one, and the same
login opens the web interface: tabs
for overview, connections, channels,
exchanges, queues, users and
policies, all reading and writing the
same API this chapter drove with
`curl`.
