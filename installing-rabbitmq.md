# Installing RabbitMQ

**Outcome:** a RabbitMQ node installed
and started on your machine, with the
management plugin enabled, ready for
the checks in chapter 4.

**Check:** `rabbitmqctl status` prints
a block beginning "Status of node" and
names a RabbitMQ version. Chapter 4
reads that block properly; if the
command errors instead, chapter 15
starts with exactly that error.

On an ordinary Ubuntu or Debian
machine, installing RabbitMQ is two
commands, because the distribution
packages both RabbitMQ and the Erlang
runtime it needs:

```bash
sudo apt update
sudo apt install rabbitmq-server
sudo systemctl enable --now rabbitmq-server
sudo rabbitmq-plugins enable rabbitmq_management
```

The third line starts the node and
arranges for it to start at boot; the
fourth turns on the management plugin
(the HTTP API and web interface used
from chapter 9 onward). On other
systems the shape is the same — the
RabbitMQ project publishes packages
for the major distributions and a
generic Unix archive — but the exact
commands belong to the project's
install pages, and this guide does not
pretend to have tested them.

## How the lab installed it instead

The machine that produced this guide
is a shared sandbox where the system
package state could not be touched, so
the lab did the same install with the
moving parts showing — worth reading
even if you never need it, because it
shows what a package manager does for
you. The full run is transcript
**t00** in `rabbitmq-lab/`:

1. The package lists and the eighteen
   `.deb` files (RabbitMQ 3.12.1 plus
   its Erlang dependencies, 36.1 MB in
   all) were downloaded with a private
   `apt` state directory — downloaded,
   not installed.
2. Each `.deb` was unpacked with
   `dpkg -x` into a private tree.
3. One wrinkle: Debian's `erl` launcher
   script has the system path
   `/usr/lib/erlang` written into it, so
   it cannot see an Erlang that lives
   elsewhere. The underlying program,
   `erlexec`, takes its paths from the
   `ROOTDIR` and `BINDIR` environment
   variables, so the lab used a
   five-line shell script that sets
   those and calls `erlexec` — exactly
   what the real `erl` does on a normal
   install.
4. Everything the node writes was
   pointed into the lab directory with
   the standard variables RabbitMQ
   honours on any install:
   `RABBITMQ_BASE` (data and logs),
   `RABBITMQ_MNESIA_BASE`,
   `RABBITMQ_LOG_BASE`,
   `RABBITMQ_PLUGINS_DIR`,
   `RABBITMQ_ENABLED_PLUGINS_FILE`,
   `RABBITMQ_CONFIG_FILE`. A small
   `rabbitmq.conf` bound the management
   listener to loopback and left AMQP
   on its own port, **5672** (the
   management port is **15672**; both
   are RabbitMQ's defaults, not choices
   of this guide).

The result is the same software the
`apt` route installs — the version
strings in chapter 4 are the Ubuntu
package's own. The lab then enabled
the management plugin offline, the way
the package route does it:

```bash
rabbitmq-plugins enable rabbitmq_management
```

which writes one line —
`[rabbitmq_management].` — into the
enabled-plugins file, and started the
node detached:

```bash
rabbitmq-server -detached
```

Two honest notes. First, a freshly
started node takes a little while to
be ready; chapter 4's checks wait for
it rather than assuming. Second, the
lab's node was told to assume 1 GB of
memory was available
(`total_memory_available_override_value`)
because the sandbox is shared with
other work. On your own machine you
should not set that: the node reads
the machine's real memory and manages
its own limits from it.
