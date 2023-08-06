.. _aredis: https://github.com/NoneGG/aredis

Changelog
=========

v4.2.1
------
Release Date: 2022-07-21

* Compatibility

  * Add support and test coverage for PyPy 3.8.

* Bug Fix

  * Ensure :meth:`coredis.RedisCluster.ensure_replication` can be used
    with :paramref:`~coredis.RedisCluster.ensure_replication.replicas` <
    total number of replicas

v4.2.0
------
Release Date: 2022-07-20

* Bug Fix

  * Fix routing of :meth:`coredis.Redis.script_kill` and
    :meth:`coredis.Redis.function_kill` to only route to primaries
  * Ensure all arguments expecting collections consistently
    use :data:`coredis.typing.Parameters`

* Chores

  * Fix ordering of keyword arguments of :meth:`coredis.Redis.set`
    to be consistent with command documentation
  * Improve documentation regarding request routing and repsonse
    merging for cluster multi node and multi shard commands
  * Sort all literal annotations

v4.1.1
------
Release Date: 2022-07-18

* Bug Fix

  * Ensure lua scripts for lock recipe are included in package

v4.1.0
------
Release Date: 2022-07-18

* Features

  * Reintroduce distributed lock implementation under
    `coredis.recipes.locks`

* Bug Fix

  * Allow initializing a LUA library without loading the code
    when it already exists if replace=False

* Performance

  * Reduce unnecessary calls to parser by using an async Event
    to signal that data is available for parsing

v4.0.2
------
Release Date: 2022-07-16

* Compatibility

  * Relax version checking to only warn if a server reports
    a non standard server version (for example with Redis-like
    databases)
  * Raise an exception when client tracking is not available
    and server assisted caching cannot be used (for example
    with upstash provisioned redis instances)

* Documentation

  * Add more detail about Sharded Pub/Sub

v4.0.1
------
Release Date: 2022-07-16

* Documentation

  * Added section about reliability in handbook
  * Improved cross referencing

v4.0.0
------
Release Date: 2022-07-15

* Features

  * Added support for using ``noreply`` when sending commands (see :ref:`handbook/noreply:no reply mode`)
  * Added support for ensuring replication to ``n`` replicas using :meth:`~coredis.Redis.ensure_replication`.
  * Moved :class:`~coredis.KeyDB` client out of experimental namespace

* Backward incompatible changes

  * Use RESP3 as default protocol version (see :ref:`handbook/response:redis response`)
  * :paramref:`~coredis.RedisCluster.non_atomic_cross_slot` is default behavior for cluster clients
  * Moved exceptions out of root namespace to ``coredis.exceptions``
  * Removed Lock implementations
  * Dropped support for hiredis (see :ref:`history:parsers`)
  * Removed ``StrictRedis`` & ``StrictRedisCluster`` aliases


v3.11.5
-------
Release Date: 2022-07-13

* Chore

  * Remove python 3.11 binary wheel builds

v3.11.4
-------
Release Date: 2022-07-09

* Bug Fix

  * Fix issue with sharded pubsub not handling multiple channel
    subscriptions

v3.11.3
-------
Release Date: 2022-07-07

* Bug Fix

  * Correct implementation of restore command when
    absttl argument is True.

v3.11.2
-------
Release Date: 2022-06-30

* Bug Fix

  * Ignore case when comparing error strings to map to
    exceptions

v3.11.1
-------
Release Date: 2022-06-29

* Bug Fix

  * Fix incorrect handling of :paramref:`~coredis.RedisCluster.non_atomic_cross_slot`
    commands when not all nodes are required for a command

v3.11.0
-------
Release Date: 2022-06-25

* Features

  * Added :paramref:`coredis.Redis.noreply` and :paramref:`coredis.RedisCluster.noreply` option
    to Redis & RedisCluster constructors to allow using the client without waiting for response from the
    server
  * Build wheels for all architectures supported by cibuildwheel


* Deprecations / Removals

  * Remove deprecated sentinel methods
  * Add warnings for :meth:`~coredis.Redis.client_setname`, :meth:`~coredis.Redis.client_reply`
    and :meth:`~coredis.Redis.auth` commands

* Bug Fixes

  * Fix missing :data:`protocol_version` in cluster pipeline code paths

v3.10.1
-------
Release Date: 2022-06-18

* Chores

  * Documentation tweaks

v3.10.0
-------
Release Date: 2022-06-18

* Features

  * Expose ssl parameters in :class:`coredis.RedisCluster` constructor
  * Expose :paramref:`~coredis.Redis.ssl_check_hostname` parameter in Redis/RedisCluster constructors
  * Separate opt-in cache behaviors into protocols leaving :class:`~coredis.cache.AbstractCache`
    as the minimal implementation required
  * Expose cache stats through the :data:`~coredis.cache.TrackingCache.stats` property, returning
    a :class:`~coredis.cache.CacheStats` dataclass.
  * Allow :paramref:`~coredis.cache.TrackingCache.dynamic_confidence` to increase cache confidence up to
    100% instead of capping it at the original :paramref:`~coredis.cache.TrackingCache.confidence` value provided

* Chores

  * Improve documentation for caching
  * Improve test coverage for ssl connections
  * Add test coverage for cluster ssl clients


v3.9.3
------
Release Date: 2022-06-15

* Features

  * Expose :paramref:`~coredis.sentinel.Sentinel.cache` parameter to Sentinel managed clients

* Bug Fix

  * Handle error parsing command not found exception

v3.9.2
------
Release Date: 2022-06-14

* Features

  * Add option to define confidence in cached entries

v3.9.1
------
Release Date: 2022-06-13

* Features

  * Extend coverage of cachable commands
  * Expose option to share TrackingCache between client

v3.9
----
Release Date: 2022-06-12

* Features

  * Add support for client side caching (:ref:`handbook/caching:caching`)

v3.8.12
-------
Release Date: 2022-06-10

* Features

  * Add support for sharded pubsub for redis 7.0.1 (:ref:`handbook/pubsub:cluster pub/sub`)
  * Expose :paramref:`~coredis.Redis.from_url.verify_version` parameter to :meth:`coredis.Redis.from_url`
    factory function

* Experiments

  * Extend CI coverage for keydb & dragonfly

v3.8.11
-------
Release Date: 2022-06-07

* Bug Fixes

  * Fix support for HELLO SETNAME
  * Fix routing of ACL SAVE in cluster mode

* Chores

  * Improved test coverage for server commands

v3.8.10
-------
Release Date: 2022-06-07

* Features

  * New ``nodenames`` parameter added to sentinel_info_cache

* Chores

  * Added redis 7.0 to sentinel test coverage matrix

v3.8.9
------
Release Date: 2022-06-05

* Bug Fix

  * Fix type annotation for hmget

* Experiments

  * Add CI coverage for dragonflydb


v3.8.7
------
Release Date: 2022-06-04

* Features

  * Add support for python 3.11 (b3) builds

* Performance

  * Extract python parser and optionally compile it to native
    code using mypyc

* Bug Fixes

  * Only route PING commands to primaries in cluster mode
  * Ensure connection errors for commands routed to multiple nodes
    are retried in case of cluster reconfiguration
  * Ensure re population of startup nodes is based off latest response
    from cluster


v3.8.6
------
Release Date: 2022-05-26

* Performance

  * Inline buffering of responses in python parser

v3.8.5
------
Release Date: 2022-05-25

* Features

  * Refactor python parser to remove recursion
  * Reduce number of async calls during response parsing
  * Extract command packer and use mypyc to compile it to native code


v3.8.0
------
Release Date: 2022-05-21

* Chores

  * Documentation reorg
  * Improved RESP error <-> exception mapping

* Bug fix

  * Ignore duplicate consumer group error due to groupconsumer
    initialization race condition

v3.7.57 ("Puffles")
------------------
Release Date: 2022-05-19

* Features

  * Stream consumer clients (:ref:`handbook/streams:simple consumer` and :ref:`handbook/streams:group consumer`)

* Experiments

  * Updated :class:`~coredis.experimental.KeyDB` command coverage
  * :class:`~coredis.experimental.KeyDBCluster` client

v3.6.0
------
Release Date: 2022-05-15

* Features

  * Add option to enable non atomic splitting of commands in cluster
    mode when the commands only deal with keys (delete, exists, touch, unlink)
    (:paramref:`~coredis.RedisCluster.non_atomic_crossslot`)
  * Add support for sharded pub sub in cluster mode (:meth:`~coredis.RedisCluster.sharded_pubsub`)
  * Add support for readonly execution of LUA scripts and redis functions

* Bug Fix

  * Ensure :meth:`~coredis.RedisCluster.script_load` is routed to all nodes in cluster mode
  * Ensure :meth:`~coredis.RedisCluster.evalsha_ro`, :meth:`~coredis.RedisCluster.eval_ro`, :meth:`~coredis.RedisCluster.fcall_ro`
    are included in readonly commands for cluster readonly mode.
  * Change version related warnings to use :exc:`DeprecationWarning`

* Chores

  * General improvements in reliability and correctness of unit tests

v3.5.1
------
Release Date: 2022-05-12

* Bug Fix

  * Fix type annotation for :attr:`coredis.response.types.PubSubMessage.data` to include int
    for server responses to subscribe/unsubscribe/psubscribe/punsubscribe

v3.5.0
------
Release Date: 2022-05-10

* Features

  * Added :meth:`coredis.commands.Library.wraps` and :meth:`coredis.commands.Script.wraps` decorators
    for creating strict signature wrappers for lua scripts and
    functions.
  * Add :meth:`~coredis.commands.Script.__call__` method to :class:`coredis.commands.Script` so it can be called
    directly without having to go through :meth:`coredis.commands.Script.execute`
  * Improve type safety with regards to command methods accepting
    multiple keys or values. These were previously annotated as
    accepting either ``Iterable[KeyT]`` or ``Iterable[ValueT]`` which
    would allow strings or bytes to be passed. These are now changed to
    ``Parameters[KeyT]`` or ``Parameter[ValueT]`` respectively which only
    allow a restricted set of collections and reject strings and bytes.

* Breaking Changes

  * Removed custom client side implementations for cross slot cluster methods.
    These methods will now use the regular cluster implementation and raise
    and error if the keys don't map to the same shard.
  * :paramref:`coredis.Redis.verify_version` on both :class:`~coredis.Redis` &
    :class:`~coredis.RedisCluster` constructors will
    default to ``True`` resulting in warnings being emitted for using
    deprecated methods and preemptive exceptions being raised when calling
    methods against server versions that do not support them.
  * Dropped support for redis server versions less than 6.0
  * A large chunk of utility / private code has been moved into
    private namespaces

* Chores

  * Refactor response transformation to use inlined callbacks
    to improve type safety.

* Bug Fixes

  * Ensure protocol_version, decoding arguments are consistent
    across different construction methods.
  * Synchronize parameters for replacing library code between :class:`coredis.commands.Library`
    constructor and :meth:`coredis.Redis.register_library`

v3.4.7
------
Release Date: 2022-05-04

* Chores

  * Update CI to use official 7.0 release for redis
  * Update CI to use 7.0.0-RC4 image for redis-stack

* Bug Fix

  * Fix key spec extraction for commands using kw search

v3.4.6
------
Release Date: 2022-04-30

* Bug Fixes

  * Ensure protocol_version is captured for constructions with from_url
  * Fix command name for module_loadex method


v3.4.5
------
Release Date: 2022-04-22

* Chore

  * Fix incorrect type annotations for primitive callbacks
  * Update test matrix in CI with python 3.11 a7
  * Update documentation to provide a slightly more detailed
    background around the project diversion

* Experiments

  * Add basic support for KeyDB

v3.4.4
------
Release Date: 2022-04-21

* Chore

  * Fix github release workflow

v3.4.3
------
Release Date: 2022-04-21

* Chore

  * Fix github release workflow

v3.4.2
------
Release Date: 2022-04-21

* Bug fix

  * Fix error selecting database when ``decode_responses`` is ``True``
    (`Issue 46 <https://github.com/alisaifee/coredis/issues/46>`_)

v3.4.1
------
Release Date: 2022-04-12

* Chores

  * Remove unmaintained examples & benchmarks
  * Simplify setup/package info with respect to stubs
  * Cleanup documentation landing page

v3.4.0
------
Release Date: 2022-04-11

* Features

  * Updates for breaking changes with ``function_load`` in redis 7.0 rc3
  * Add ``module_loadex`` method

* Bug fix

  * Fix installation error when building from source

v3.3.0
------
Release Date: 2022-04-04

* Features

  * Add explicit key extraction based on key spec for cluster clients

v3.2.0
------
Release Date: 2022-04-02

* Features

  * New APIs:

    * Server:

      * ``Redis.latency_histogram``
      * ``Redis.module_list``
      * ``Redis.module_load``
      * ``Redis.module_unload``

    * Connection:

      * ``Redis.client_no_evict``

    * Cluster:

      * ``Redis.cluster_shards``
      * ``Redis.readonly``
      * ``Redis.readwrite``

  * Micro optimization to use bytestrings for all hardcoded tokens
  * Add type hints for pipeline classes
  * Remove hardcoded pipeline blocked commands

* Bug Fix

  * Disable version checking by default
  * Fix incorrect key names for server commands

* Chores

  * Move publishing steps to CI
  * More typing related cleanups
  * Refactor parsers into a separate module
  * Improve test coverage to cover non decoding clients

v3.1.1
------
Release Date: 2022-03-24

* Bug Fix

  * Fix extracting version/protocol with binary clients

* Features

  * New APIs:

    * ``Redis.cluster_addslotsrange``
    * ``Redis.cluster_delslotsrange``
    * ``Redis.cluster_links``
    * ``Redis.cluster_myid``

v3.1.0
------
Release Date: 2022-03-23

* Features

  * Added support for functions
  * Added runtime checks to bail out early if server version doesn't support the command
  * Deprecate custom cluster methods
  * Issue warning when a deprecated redis command is used
  * Add support for ``RESP3`` protocol

* New APIs:

  * Scripting:

    * ``Redis.fcall``
    * ``Redis.fcall_ro``
    * ``Redis.function_delete``
    * ``Redis.function_dump``
    * ``Redis.function_flush``
    * ``Redis.function_kill``
    * ``Redis.function_list``
    * ``Redis.function_load``
    * ``Redis.function_restore``
    * ``Redis.function_stats``

  * Server:

    * ``Redis.command_docs``
    * ``Redis.command_getkeysandflags``
    * ``Redis.command_list``


v3.0.3
------
Release Date: 2022-03-21

* Bug Fix

  * Fix autoselection of hiredis when available

v3.0.2
------
Release Date: 2022-03-21

* Bug Fix

  * Fix incorrect response type for :meth:`coredis.Redis.exists` (:issue:`24`)

v3.0.1
------
Release Date: 2022-03-21

* Bug Fix

  * Ensure all submodules are included in package (:issue:`23`)
  * Fix conversation of datetime object to pxat value for set command

* Chores

  * Re-add examples folder
  * Tweak type hints
  * Make ``scan_iter`` arguments consistent with ``scan``

v3.0.0
---------
Release Date: 2022-03-20

* Features:

  * Added type hints to all redis commands
  * Added support for experimental runtime type checking
  * Updated APIs upto redis 6.2.0
  * Added experimental features for redis 7.0.0

* New APIs:

  * Generic:

    * ``Redis.copy``
    * ``Redis.migrate``

  * String:

    * ``Redis.lcs``

  * List:

    * ``Redis.blmpop``
    * ``Redis.lmpop``

  * Set:

    * ``Redis.sintercard``

  * Sorted-Set:

    * ``Redis.bzmpop``
    * ``Redis.zintercard``
    * ``Redis.zmpop``

  * Scripting:

    * ``Redis.eval_ro``
    * ``Redis.evalsha_ro``
    * ``Redis.script_debug``

  * Stream:

    * ``Redis.xautoclaim``
    * ``Redis.xgroup_createconsumer``
    * ``Redis.xgroup_delconsumer``
    * ``Redis.xgroup_setid``

  * Server:

    * ``Redis.acl_cat``
    * ``Redis.acl_deluser``
    * ``Redis.acl_dryrun``
    * ``Redis.acl_genpass``
    * ``Redis.acl_getuser``
    * ``Redis.acl_list``
    * ``Redis.acl_load``
    * ``Redis.acl_log``
    * ``Redis.acl_save``
    * ``Redis.acl_setuser``
    * ``Redis.acl_users``
    * ``Redis.acl_whoami``
    * ``Redis.command``
    * ``Redis.command_count``
    * ``Redis.command_getkeys``
    * ``Redis.command_info``
    * ``Redis.failover``
    * ``Redis.latency_doctor``
    * ``Redis.latency_graph``
    * ``Redis.latency_history``
    * ``Redis.latency_latest``
    * ``Redis.latency_reset``
    * ``Redis.memory_doctor``
    * ``Redis.memory_malloc_stats``
    * ``Redis.memory_purge``
    * ``Redis.memory_stats``
    * ``Redis.memory_usage``
    * ``Redis.replicaof``
    * ``Redis.swapdb``

  * Connection:

    * ``Redis.auth``
    * ``Redis.client_caching``
    * ``Redis.client_getredir``
    * ``Redis.client_id``
    * ``Redis.client_info``
    * ``Redis.client_reply``
    * ``Redis.client_tracking``
    * ``Redis.client_trackinginfo``
    * ``Redis.client_unblock``
    * ``Redis.client_unpause``
    * ``Redis.hello``
    * ``Redis.reset``
    * ``Redis.select``

  * Cluster:

    * ``Redis.asking``
    * ``Redis.cluster_bumpepoch``
    * ``Redis.cluster_flushslots``
    * ``Redis.cluster_getkeysinslot``


* Breaking changes:

  * Most redis command API arguments and return types have been
    refactored to be in sync with the official docs.

  * Updated all commands accepting multiple values for an argument
    to use positional var args **only** if the argument is optional.
    For all other cases, use a positional argument accepting an
    ``Iterable``. Affected methods:

    * ``bitop`` -> ``*keys`` -> ``keys: Iterable[KeyT]``
    * ``delete`` -> ``*keys`` -> ``keys: Iterable[KeyT]``
    * ``exists`` -> ``*keys`` -> ``keys: Iterable[KeyT]``
    * ``touch`` -> ``*keys`` -> ``keys: Iterable[KeyT]``
    * ``unlink`` -> ``*keys`` -> ``keys: Iterable[KeyT]``
    * ``blpop`` -> ``*keys`` -> ``keys: Iterable[KeyT]``
    * ``brpop`` -> ``*keys`` -> ``keys: Iterable[KeyT]``
    * ``lpush`` -> ``*elements`` -> ``elements: Iterable[ValueT]``
    * ``lpushx`` -> ``*elements`` -> ``elements: Iterable[ValueT]``
    * ``rpush`` -> ``*elements`` -> ``elements: Iterable[ValueT]``
    * ``rpushx`` -> ``*elements`` -> ``elements: Iterable[ValueT]``
    * ``mget`` -> ``*keys`` -> ``keys: Iterable[KeyT]``
    * ``sadd`` -> ``*members`` -> ``members: Iterable[ValueT]``
    * ``sdiff`` -> ``*keys`` -> ``keys: Iterable[KeyT]``
    * ``sdiffstore`` -> ``*keys`` -> ``keys: Iterable[KeyT]``
    * ``sinter`` -> ``*keys`` -> ``keys: Iterable[KeyT]``
    * ``sinterstore`` -> ``*keys`` -> ``keys: Iterable[KeyT]``
    * ``smismember`` -> ``*members`` -> ``members: Iterable[ValueT]``
    * ``srem`` -> ``*members` -> ``members: Iterable[ValueT]``
    * ``sunion`` -> ``*keys`` -> ``keys: Iterable[KeyT]``
    * ``sunionstore`` -> ``*keys`` -> ``keys: Iterable[KeyT]``
    * ``geohash`` -> ``*members`` -> ``members: Iterable[ValueT]``
    * ``hdel`` -> ``*fields`` -> ``fields: Iterable[ValueT]``
    * ``hmet`` -> ``*fields`` -> ``fields: Iterable[ValueT]``
    * ``pfcount`` -> ``*keys`` -> ``keys: Iterable[KeyT]``
    * ``pfmerge`` -> ``*sourcekeys`` -> ``sourcekeys: Iterable[KeyT]``
    * ``zdiff`` -> ``*keys`` -> ``keys: Iterable[KeyT]``
    * ``zdiffstore`` -> ``*keys`` -> ``keys: Iterable[KeyT]``
    * ``zinter`` -> ``*keys`` -> ``keys: Iterable[KeyT]``
    * ``zinterstore`` -> ``*keys`` -> ``keys: Iterable[KeyT]``
    * ``zmscore`` -> ``*members`` -> ``members: Iterable[ValueT]``
    * ``zrem`` -> ``*members`` -> ``members: Iterable[ValueT]``
    * ``zunion`` -> ``*keys`` -> ``keys: Iterable[KeyT]``
    * ``zunionstore`` -> ``*keys`` -> ``keys: Iterable[KeyT]``
    * ``xack`` -> ``*identifiers`` -> ``identifiers: Iterable[ValueT]``
    * ``xdel`` -> ``*identifiers`` -> ``identifiers: Iterable[ValueT]``
    * ``xclaim`` -> ``*identifiers`` -> ``identifiers: Iterable[ValueT]``
    * ``script_exists`` -> ``*sha1s`` - > ``sha1s: Iterable[ValueT]``
    * ``client_tracking`` -> ``*prefixes`` - > ``prefixes: Iterable[ValueT]``
    * ``info`` -> ``*sections`` - > ``sections: Iterable[ValueT]``

v2.3.1
------
Release Date: 2022-01-30

* Chore:

  * Standardize doc themes
  * Boo doc themes

v2.3.0
------
Release Date: 2022-01-23

Final release maintaining backward compatibility with `aredis`_

* Chore:

  * Add test coverage for uvloop
  * Add test coverage for hiredis
  * Extract tests to use docker-compose
  * Add tests for basic authentication


v2.2.3
------
Release Date: 2022-01-22

* Bug fix:

  * Fix stalled connection when only username is provided

v2.2.2
------
Release Date: 2022-01-22

* Bug fix:

  * Fix failure to authenticate when just using password

v2.2.1
------
Release Date: 2022-01-21


This release brings in pending pull requests from
the original `aredis`_ repository and updates the signatures
of all implemented methods to be synchronized (as much as possible)
with the official redis documentation.

* Feature (extracted from pull requests in `aredis`_):
  * Add option to provide ``client_name``
  * Add support for username/password authentication
  * Add BlockingConnectionPool

v2.1.0
------
Release Date: 2022-01-15

This release attempts to update missing command
coverage for common datastructures and gets closer
to :pypi:`redis-py` version ``4.1.0``

* Feature:

  * Added string commands ``decrby``, ``getdel`` & ``getex``
  * Added list commands ``lmove``, ``blmove`` & ``lpos``
  * Added set command ``smismember``
  * Added sorted set commands ``zdiff``, ``zdiffstore``, ``zinter``, ``zmscore``,
      ``zpopmin``, ``zpopmax``, ``bzpopmin``, ``bzpopmax`` & ``zrandmember``
  * Added geo commands ``geosearch``, ``geosearchstore``
  * Added hash command ``hrandfield``
  * Added support for object inspection commands ``object_encoding``, ``object_freq``, ``object_idletime`` & ``object_refcount``
  * Added ``lolwut``

* Chore:
  * Standardize linting against black
  * Add API documentation
  * Add compatibility documentation
  * Add CI coverage for redis 6.0


v2.0.1
------
Release Date: 2022-01-15

* Bug Fix:

  * Ensure installation succeeds without gcc


v2.0.0
------
Release Date: 2022-01-05

* Initial import from `aredis`_
* Add support for python 3.10

------

Imported from fork
------------------

The changelog below is imported from `aredis`_


------
v1.1.8
------
* Fixbug: connection is disconnected before idel check, valueError will be raised if a connection(not exist) is removed from connection list
* Fixbug: abstract compat.py to handle import problem of asyncio.future
* Fixbug: When cancelling a task, CancelledError exception is not propagated to client
* Fixbug: XREAD command should accept 0 as a block argument
* Fixbug: In redis cluster mode, XREAD command does not function properly
* Fixbug: slave connection params when there are no slaves

------
v1.1.7
------
* Fixbug: ModuleNotFoundError raised when install aredis 1.1.6 with Python3.6

------
v1.1.6
------
* Fixbug: parsing stream messgae with empty payload will cause error(#116)
* Fixbug: Let ClusterConnectionPool handle skip_full_coverage_check (#118)
* New: threading local issue in coroutine, use contextvars instead of threading local in case of the safety of thread local mechanism being broken by coroutine (#120)
* New: support Python 3.8

------
v1.1.5
------
* new: Dev conn pool max idle time (#111) release connection if max-idle-time exceeded
* update: discard travis-CI
* Fix bug: new stream id used for test_streams

------
v1.1.4
------
* fix bug: fix cluster port parsing for redis 4+(node info)
* fix bug: wrong parse method of scan_iter in cluster mode
* fix bug: When using "zrange" with "desc=True" parameter, it returns a coroutine without "await"
* fix bug: do not use stream_timeout in the PubSubWorkerThread
* opt: add socket_keepalive options
* new: add ssl param in get_redis_link to support ssl mode
* new: add ssl_context to StrictRedis constructor and make it higher priority than ssl parameter

------
v1.1.3
------
* allow use of zadd options for zadd in sorted sets
* fix bug: use inspect.isawaitable instead of typing.Awaitable to judge if an object is awaitable
* fix bug: implicitly disconnection on cancelled error (#84)
* new: add support for `streams`(including commands not officially released, see `streams <http://aredis.readthedocs.io/en/latest/streams.html>`_ )

------
v1.1.2
------
* fix bug: redis command encoding bug
* optimization: sync change on acquring lock from redis-py
* fix bug: decrement connection count on connection disconnected
* fix bug: optimize code proceed single node slots
* fix bug: initiation error of aws cluster client caused by not appropiate function list used
* fix bug: use `ssl_context` instead of ssl_keyfile,ssl_certfile,ssl_cert_reqs,ssl_ca_certs in intialization of connection_pool

------
v1.1.1
------
* fix bug: connection with unread response being released to connection pool will lead to parse error, now this kind of connection will be destructed directly. `#52 <https://github.com/NoneGG/aredis/issues/52>`_
* fix bug: remove Connection.can_read check which may lead to block in awaiting pubsub message. Connection.can_read api will be deprecated in next release. `#56 <https://github.com/NoneGG/aredis/issues/56>`_
* add c extension to speedup crc16, which will speedup cluster slot hashing
* add error handling for asyncio.futures.Cancelled error, which may cause error in response parsing.
* sync optimization of client list made by swilly22 from redis-py
* add support for distributed lock using redis cluster

------
v1.1.0
------
* sync optimization of scripting from redis-py made by `bgreenberg <https://github.com/bgreenberg-eb>`_ `redis-py#867 <https://github.com/andymccurdy/redis-py/pull/867>`_
* sync bug fixed of `geopos` from redis-py made by `categulario <https://github.com/categulario>`_ `redis-py#888 <https://github.com/andymccurdy/redis-py/pull/888>`_
* fix bug which makes pipeline callback function not executed
* fix error caused by byte decode issues in sentinel
* add basic transaction support for single node in cluster
* fix bug of get_random_connection reported by myrfy001

------
v1.0.9
------
* fix bug of pubsub, in some env AssertionError is raised because connection is used again after reader stream being fed eof
* add reponse decoding related options(`encoding` & `decode_responses`), make client easier to use
* add support for command `cluster forget`
* add support for command option `spop count`

------
v1.0.8
------
* fix initialization bug of redis cluster client
* add example to explain how to use `client reply on | off | skip`

------
v1.0.7
------
* introduce loop argument to aredis
* add support for command `cluster slots`
* add support for redis cluster

------
v1.0.6
------
* bitfield set/get/incrby/overflow supported
* new command `hstrlen` supported
* new command `unlink` supported
* new command `touch` supported

------
v1.0.5
------
* fix bug in setup.py when using pip to install aredis

------
v1.0.4
------
* add support for command `pubsub channel`, `pubsub numpat` and `pubsub numsub`
* add support for command `client pause`
* reconsitution of commands to make develop easier(which is transparent to user)

------
v1.0.2
------
* add support for cache (Cache and HerdCache class)
* fix bug of `PubSub.run_in_thread`

------
v1.0.1
------

* add scan_iter, sscan_iter, hscan_iter, zscan_iter and corresponding unit tests
* fix bug of `PubSub.run_in_thread`
* add more examples
* change `Script.register` to `Script.execute`


























































