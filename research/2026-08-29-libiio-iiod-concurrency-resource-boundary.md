# libiio iiod concurrency and resource boundaries

Date: 2026-08-29
Project: analogdevicesinc/libiio
Repository: https://github.com/analogdevicesinc/libiio
Evidence level: VERIFIED (source-level architecture)
Provisional Gold score: S / 27
Scope: Linux `iiod` TCP concurrency, thread lifecycle, listener backlog, stale-client handling, and operator resource assumptions

## Executive finding

The current Linux `iiod` network server uses a **thread-per-accepted-client model**, despite naming its helper subsystem a `thread_pool`. The inspected `thread-pool.c` is not a fixed-size worker pool and does not expose a maximum thread count, work queue, concurrency semaphore, or admission quota. Instead, it creates detached pthreads on demand and tracks how many remain active so shutdown can wait for cleanup.

This matters because the TCP listener's backlog of 16 is not an active-client limit. Once a connection is accepted, `network.c` allocates per-client state and asks `thread_pool_add_thread()` to create another detached client thread. The practical concurrent-client ceiling is therefore primarily determined by process/OS resource limits, socket behavior, memory/thread-stack cost, and any external deployment controls rather than by an explicit `iiod` application-level client cap in the inspected path.

This is recorded as an **operator/resource-boundary observation, not a vulnerability claim**. GitHub Gold did not load-test, fuzz, deploy, or attempt to exhaust `iiod`.

## Evidence inspected

Primary upstream files on current `main`:

- `iiod/network.c`
- `iiod/thread-pool.c`
- repository tree for related `iiod`, Zephyr, test, and stress-test surfaces

No third-party source code was copied into GitHub Gold.

## Connection lifecycle

Current `iiod/network.c` creates IPv4 and IPv6 TCP listener sockets, binds them to wildcard addresses, and calls `listen(fd, 16)`.

On an accepted connection, the server:

1. allocates a `client_data` structure;
2. configures socket options;
3. stores the accepted file descriptor and interpreter context;
4. calls `thread_pool_add_thread(..., client_thd, ..., "net_client_thd")`;
5. closes the connection if thread creation fails.

The resulting `client_thd` runs the IIO interpreter for that socket. When the interpreter returns, the thread closes the socket and frees its per-client allocation.

### Why backlog 16 is not a client quota

The `listen(..., 16)` value controls the kernel's pending-connection backlog behavior. It does not constrain the number of connections that have already been accepted and assigned threads.

Therefore it should not be documented as "iiod supports a maximum of 16 clients." The inspected application path contains no such active-client limit.

## What the `thread_pool` actually does

Current `iiod/thread-pool.c` defines a pool with:

- a mutex and condition variable;
- an unsigned `thread_count`;
- an `eventfd` used to signal stop;
- a boolean stop flag.

`thread_pool_add_thread()`:

- allocates a small wrapper object;
- initializes pthread attributes;
- explicitly sets `PTHREAD_CREATE_DETACHED`;
- increments `thread_count` before creation to avoid a race;
- invokes `pthread_create()` directly;
- decrements the count if creation fails;
- otherwise lets the detached worker run asynchronously.

There is no inspected field for `max_threads`, queue depth, worker count, per-client quota, or concurrency token budget.

The subsystem is therefore better understood as a **thread lifecycle/shutdown coordinator** than as the fixed-size worker-pool abstraction that its name might suggest.

## Shutdown behavior

The design has a useful cleanup property.

Each worker decrements `thread_count` immediately before it exits. `thread_pool_wait()` blocks on the condition variable until that count reaches zero. `thread_pool_stop_and_wait()` signals the stop event and then waits for all active threads to clean up before the surrounding IIO context is destroyed.

The source comments explicitly explain why detached threads are used: ordinary client threads may finish asynchronously, while daemon shutdown still needs a reliable way to wait for active threads to release resources and disable buffers before context destruction.

This is a reusable design pattern for daemons that want detached request workers but still need coordinated teardown.

## Stop signaling

The pool owns a nonblocking `eventfd`. `thread_pool_stop()` sets the stop flag and writes to that eventfd. Other daemon components can poll the pool's stop descriptor and unwind when shutdown is requested.

This is not a per-client resource-control mechanism; it is a process-lifecycle signal.

## TCP stale-peer handling

For accepted TCP clients, current `network.c` enables `SO_KEEPALIVE` and configures:

- TCP keepalive idle time: 10 seconds;
- keepalive interval: 10 seconds;
- keepalive probe count: 6.

The upstream source comment describes the intent as sending keep-alives every 10 seconds and disconnecting when there has been no reply for roughly one minute.

This helps reclaim sockets/threads associated with dead or unreachable peers. It should not be confused with an application-level idle-session timeout: a live peer that keeps its TCP connection viable is a different case, and this pass did not establish a separate maximum session age or command-idle deadline in `iiod`.

## Resource-control interpretation

### Explicit controls found in this path

- kernel listen backlog of 16 pending connections;
- OS failure of allocation or `pthread_create()` causes that new client to be rejected/closed;
- TCP keepalive helps detect stale/dead peers;
- coordinated daemon stop waits for active client workers to clean up.

### Explicit controls not found in the inspected path

The inspected Linux TCP/thread-pool source does not expose an obvious:

- maximum active client count;
- fixed worker-thread count;
- admission semaphore;
- per-source-IP connection quota;
- application-level connection rate limiter;
- bounded worker queue;
- per-client CPU budget;
- per-client memory budget;
- maximum session lifetime.

This statement is intentionally limited to the files and path inspected. External supervisors, containers, systemd settings, firewalls, namespaces, kernel limits, distribution packaging, or downstream patches can impose additional boundaries.

## Deployment consequence

Because `iiod` exposes meaningful hardware-control operations over its protocol, the resource boundary is operationally important even when the daemon is correctly deployed only on trusted networks.

A production deployment should treat process resource limits and network admission policy as part of the service design rather than assuming the daemon's internal `thread_pool` provides bounded concurrency.

Examples of external controls that can complement the application include:

- network segmentation/firewall policy;
- authenticated overlay or tunnel access;
- service-manager task/process/file-descriptor/memory limits;
- container or cgroup limits;
- connection-rate controls at a trusted proxy/firewall layer;
- monitoring of thread, socket, memory, and I/O pressure.

These are deployment considerations, not claims about required upstream configuration.

## Reusable component assessment

`iiod/thread-pool.c` is technically interesting but should be described accurately.

Useful ideas include:

- detached worker creation with race-safe active-thread accounting;
- condition-variable shutdown synchronization;
- eventfd-based cooperative stop signaling;
- cleanup before shared context destruction.

It is **not** a reusable bounded worker-pool implementation without additional concurrency controls.

The file carries `LGPL-2.1-or-later`; any source reuse would require license/notice review. GitHub Gold only catalogs the design and does not copy the implementation.

## Verification boundary

VERIFIED here means GitHub Gold confirmed from current upstream source that:

- accepted TCP clients are dispatched through `thread_pool_add_thread()`;
- each call creates a detached pthread rather than enqueueing work into a fixed worker set;
- the helper tracks active thread count for shutdown;
- no maximum-thread field or concurrency semaphore is present in the inspected implementation;
- the TCP listener uses backlog 16;
- accepted sockets receive TCP keepalive configuration with the values described above.

It does **not** mean GitHub Gold independently measured maximum clients, thread-stack memory, kernel backlog behavior under load, throughput, denial-of-service resistance, or real-world deployment defaults.

## Promotion impact

libiio remains **VERIFIED — provisional S / 27**.

This follow-up does not justify a score change. It improves the candidate record by distinguishing architectural capability from deployment/resource assumptions and by identifying `iiod/thread-pool.c` as a useful lifecycle primitive rather than misclassifying it as a bounded executor.

## Strong next leads

1. Inspect `utils/iio_stresstest.c` to determine what concurrency/load behavior upstream actually exercises and what it does not test.
2. Compare Linux `iiod` against `zephyr/iiod/network.c` and Zephyr Kconfig for explicit thread/stack/connection limits.
3. Trace whether the interpreter or responder layers impose command/read deadlines independent of TCP keepalive.
4. Map SoapySDR ↔ libiio integration to see how a broader SDR abstraction consumes IIO contexts and streaming.
5. Inspect pyadi-iio and libad9361 as higher-level reusable control layers above libiio.
6. Compare distribution/service hardening with the upstream systemd template before making claims about deployed privilege or cgroup limits.
