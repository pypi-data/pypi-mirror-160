## 4.3.8 (2022-07-21)

Annotate some `redis.backoff` items (#8352)

## 4.3.7 (2022-07-20)

Improve types of `redis.connection` module (#8342)

Co-authored-by: pre-commit-ci[bot] <66853113+pre-commit-ci[bot]@users.noreply.github.com>
Co-authored-by: Alex Waygood <Alex.Waygood@Gmail.com>

## 4.3.6 (2022-07-19)

Type async Pipeline commands explicitly (#8325)

## 4.3.5 (2022-07-19)

Improve `redis.sentinel` types (#8331)

## 4.3.4 (2022-07-12)

Import `Match` and `Pattern` from `re`, not `typing` (#8277)

## 4.3.3 (2022-06-28)

Update redis stubs to 4.3.4 (#8199)

Fixes #8196

## 4.3.2 (2022-06-23)

Improve `redis/asyncio/client.pyi` (#8141)

## 4.3.1 (2022-06-21)

Rename some confusingly named type aliases (#8129)

## 4.3.0 (2022-06-20)

Update redis stubs to 4.3 (#8108)

## 4.2.8 (2022-06-18)

redis: remove duplicate allowlist entries (#8097)

Co-authored-by: hauntsaninja <>

## 4.2.7 (2022-06-15)

`redis`: fix more unconstrained `TypeVar`s (#8084)

## 4.2.6 (2022-05-26)

redis: Fix unconstrained TypeVars in a few redis commands (#7942)

Part of #7928

## 4.2.5 (2022-05-21)

Simplify and correct many numeric unions (#7906)

Unblocks PyCQA/flake8-pyi#222

## 4.2.4 (2022-05-19)

reds: commands from asyncio module must be async (#7820)

redis-py has introduced an asyncio module since 4.2 and almost all
commands should be async if the redis.asyncio.Redis is used instead of
redis.Redis.

This changes adds the types for all core commands.

Related to #7597

## 4.2.3 (2022-05-15)

Add `__version__`/`VERSION` to redis (#7838)

## 4.2.2 (2022-05-07)

Import generics from standard modules in all third-party stubs (#7791)

## 4.2.1 (2022-05-04)

Add missing redis modules and classes (#7676)

This adds asyncio support and support for redis.typing.

## 4.2.0 (2022-04-24)

Update redis stubs to 4.2 (#7675)

Closes #7597

## 4.1.22 (2022-04-20)

Use `TypeAlias` for type aliases where possible, part II (#7667)

## 4.1.21 (2022-04-16)

Third-party stubs: import from `collections.abc` where possible (#7637)

## 4.1.20 (2022-04-16)

Use `TypeAlias` where possible for type aliases (#7630)

## 4.1.19 (2022-04-01)

Third-party stubs: Improve several `__exit__` methods (#7575)

## 4.1.18 (2022-03-16)

Use PEP 604 syntax wherever possible (#7493)

## 4.1.17 (2022-02-23)

Re-export RedisCluster from redis (#7371)

## 4.1.16 (2022-02-17)

Update to redis 4.1.4 (#7247)

Closes: #7245

## 4.1.15 (2022-02-03)

Improve `__enter__` & constructor methods (#7114)

## 4.1.14 (2022-02-02)

Redis: Annotate .lolwut() (#7104)

## 4.1.13 (2022-01-31)

Redis: Annotate .pttl(), .dump(), and .getdel() (#7091)

## 4.1.12 (2022-01-31)

Upgrade black version (#7089)

## 4.1.11 (2022-01-28)

Update redis stubs for 4.1.2 (#7064)

## 4.1.10 (2022-01-19)

Update redis stubs to 4.1.1 (#6960)

Closes: #6951

## 4.1.9 (2022-01-19)

Revert "Temporarily fix redis version to 4.1.0" (#6957)

This reverts commit 7d2de33bba2808e98b3caa46904418ad9a1b07f5.

Temporarily fix redis version to 4.1.0 (#6952)

Quick fix for #6951

## 4.1.8 (2022-01-13)

Annotate command kwargs arguments (#6721)

## 4.1.7 (2022-01-10)

Always use `_typeshed.Self`, where applicable (#6880)

* Always use `_typeshed.Self`, where applicable

* Revert changes to `google-cloud-ndb` (ambiguous)

* Remove empty line added by script

* Revert changes to `stubs/python-dateutil/dateutil/relativedelta.pyi`

* Manually add a few more that the script missed

* Improve `filelock` annotation

Source code here: https://github.com/tox-dev/py-filelock/blob/79ec7b2826e33b982fe83b057f359448b9d966ba/src/filelock/_api.py#L207

* Improve `opentracing/scope` annotation

Source code here: https://github.com/opentracing/opentracing-python/blob/3e1d357a348269ef54d67f761302fab93dbfc0f7/opentracing/scope.py#L71

* Improve `redis/client` stub

Source code here: https://github.com/redis/redis-py/blob/15f315a496c3267c8cbcc6d6d9c6005ea4d4a4d5/redis/client.py#L1217

* Improve `redis/lock` annotation

Source code here: https://github.com/redis/redis-py/blob/15f315a496c3267c8cbcc6d6d9c6005ea4d4a4d5/redis/lock.py#L155

* Improve `requests/models` annotation

Source code here: https://github.com/psf/requests/blob/d718e753834b84018014a23d663369ac27d1ab9c/requests/models.py#L653

## 4.1.6 (2022-01-09)

put redis.client._ScoreCastFuncReturn back (#6876)

#6829 removed it as unused but #6790 added a usage.

Minor improvements to redis stubs for scan and zset methods (#6790)

## 4.1.5 (2022-01-08)

Use lowercase `type` everywhere (#6853)

## 4.1.3 (2022-01-05)

Remove several unused `TypeVar`s (#6829)

## 4.1.2 (2022-01-02)

Never explicitly inherit from `object` in Python 3-only stubs (#6777)

## 4.1.1 (2021-12-28)

redis: Restore type annotations of ping() and save() (#6720)

Use PEP 585 syntax wherever possible (#6717)

## 4.1.0 (2021-12-27)

Update redis stubs to 4.1 (#6711)

Co-authored-by: Akuli <akuviljanen17@gmail.com>
Co-authored-by: pre-commit-ci[bot] <66853113+pre-commit-ci[bot]@users.noreply.github.com>

## 4.0.6 (2021-12-25)

redis: Add stubs for lmove and blmove (#6586)

## 4.0.5 (2021-12-21)

Fix Redis.zpopmin and zpopmax (#6642)

Co-authored-by: Sebastian Rittau <srittau@rittau.biz>

## 4.0.4 (2021-12-17)

Always import Protocol from typing in stubs (#6617)

## 4.0.3 (2021-12-01)

Fix various issues in redis.client (#6464)

## 4.0.2 (2021-12-01)

redis: fix several stubtest warnings (#6378)

Co-authored-by: pre-commit-ci[bot] <66853113+pre-commit-ci[bot]@users.noreply.github.com>
Co-authored-by: Shantanu <12621235+hauntsaninja@users.noreply.github.com>
Co-authored-by: Jelle Zijlstra <jelle.zijlstra@gmail.com>

## 4.0.1 (2021-11-26)

Add mypy error codes to '# type: ignore' comments (#6379)

## 4.0.0 (2021-11-25)

Update redis stubs to version 4 (#6368)

## 3.5.18 (2021-11-23)

Reduce use of deprecated `typing` aliases (#6358)

## 3.5.17 (2021-11-18)

Revert "do not use mypy-specific syntax in '# type: ignore' comments" (#6338)

## 3.5.16 (2021-11-12)

Redis Sentinel master_for, slave_for returns a Redis client (#6269)

## 3.5.15 (2021-10-16)

Annotate Client.decr() and decrby() (#6179)

## 3.5.14 (2021-10-15)

Add redis/sentinel.pyi (#6174)

## 3.5.13 (2021-10-15)

Use lowercase tuple where possible (#6170)

## 3.5.12 (2021-10-12)

Add star to all non-0.1 versions (#6146)

## 3.5.11 (2021-10-09)

Add Redis.memory_purge() (#6138)

## 3.5.10 (2021-10-09)

Add memory_stats() to Redis (#6137)

## 3.5.9 (2021-09-29)

redis: include local property on Lock class (#6083)

The Lock class as a property local that has a token property that sometimes
needs be accessed / set.

```python
lock = redis.lock(key)
lock.local.token = token
lock.extend(10)
```

Technically the type of `local` is `SimpleNamespace | threading.local`
but I think this setup is a bit stricter but satisfies the API.

## 3.5.8 (2021-09-10)

Fix type of blocking_timeout argument to redis.lock.Lock (#6019)

## 3.5.7 (2021-08-29)

do not use mypy-specific syntax in '# type: ignore' comments (#5953)

