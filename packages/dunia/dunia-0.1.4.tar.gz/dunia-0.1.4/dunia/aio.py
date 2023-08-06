# MIT License

# Copyright (c) 2022 Danyal Zia Khan

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from __future__ import annotations

import asyncio
from functools import wraps
from typing import TYPE_CHECKING

from async_timeout import timeout as async_timeout

if TYPE_CHECKING:
    from asyncio import Future
    from collections.abc import Awaitable, Callable, Coroutine, Generator
    from typing import Any, Literal, ParamSpec, TypeVar, overload

    ParamsType = ParamSpec("ParamsType")
    ReturnType = TypeVar("ReturnType")

    _T = TypeVar("_T")
    _T1 = TypeVar("_T1")
    _T2 = TypeVar("_T2")
    _T3 = TypeVar("_T3")
    _T4 = TypeVar("_T4")
    _T5 = TypeVar("_T5")
    _T6 = TypeVar("_T6")
    _T7 = TypeVar("_T7")
    _T8 = TypeVar("_T8")
    _FutureT = Future[_T] | Generator[Any, None, _T] | Awaitable[_T]

    # ? Typing for asyncio.gather() for upto 8 coroutines
    # ? Modified from Playwright's typeshed
    @overload
    def gather(  # type: ignore
        __coro_or_future1: _FutureT[_T1], *, return_exceptions: Literal[False] = ...
    ) -> Future[tuple[_T1]]:
        ...

    @overload
    def gather(  # type: ignore
        __coro_or_future1: _FutureT[_T1],
        __coro_or_future2: _FutureT[_T2],
        *,
        return_exceptions: Literal[False] = ...,
    ) -> Future[tuple[_T1, _T2]]:
        ...

    @overload
    def gather(  # type: ignore
        __coro_or_future1: _FutureT[_T1],
        __coro_or_future2: _FutureT[_T2],
        __coro_or_future3: _FutureT[_T3],
        *,
        return_exceptions: Literal[False] = ...,
    ) -> Future[tuple[_T1, _T2, _T3]]:
        ...

    @overload
    def gather(  # type: ignore
        __coro_or_future1: _FutureT[_T1],
        __coro_or_future2: _FutureT[_T2],
        __coro_or_future3: _FutureT[_T3],
        __coro_or_future4: _FutureT[_T4],
        *,
        return_exceptions: Literal[False] = ...,
    ) -> Future[tuple[_T1, _T2, _T3, _T4]]:
        ...

    @overload
    def gather(  # type: ignore
        __coro_or_future1: _FutureT[_T1],
        __coro_or_future2: _FutureT[_T2],
        __coro_or_future3: _FutureT[_T3],
        __coro_or_future4: _FutureT[_T4],
        __coro_or_future5: _FutureT[_T5],
        *,
        return_exceptions: Literal[False] = ...,
    ) -> Future[tuple[_T1, _T2, _T3, _T4, _T5]]:
        ...

    @overload
    def gather(  # type: ignore
        __coro_or_future1: _FutureT[_T1],
        __coro_or_future2: _FutureT[_T2],
        __coro_or_future3: _FutureT[_T3],
        __coro_or_future4: _FutureT[_T4],
        __coro_or_future5: _FutureT[_T5],
        __coro_or_future6: _FutureT[_T6],
        *,
        return_exceptions: Literal[False] = ...,
    ) -> Future[tuple[_T1, _T2, _T3, _T4, _T5, _T6]]:
        ...

    @overload
    def gather(  # type: ignore
        __coro_or_future1: _FutureT[_T1],
        __coro_or_future2: _FutureT[_T2],
        __coro_or_future3: _FutureT[_T3],
        __coro_or_future4: _FutureT[_T4],
        __coro_or_future5: _FutureT[_T5],
        __coro_or_future6: _FutureT[_T6],
        __coro_or_future7: _FutureT[_T7],
        *,
        return_exceptions: Literal[False] = ...,
    ) -> Future[tuple[_T1, _T2, _T3, _T4, _T5, _T6, _T7]]:
        ...

    @overload
    def gather(  # type: ignore
        __coro_or_future1: _FutureT[_T1],
        __coro_or_future2: _FutureT[_T2],
        __coro_or_future3: _FutureT[_T3],
        __coro_or_future4: _FutureT[_T4],
        __coro_or_future5: _FutureT[_T5],
        __coro_or_future6: _FutureT[_T6],
        __coro_or_future7: _FutureT[_T7],
        __coro_or_future8: _FutureT[_T8],
        *,
        return_exceptions: Literal[False] = ...,
    ) -> Future[tuple[_T1, _T2, _T3, _T4, _T5, _T6, _T7, _T8]]:
        ...

    @overload
    def gather(
        __coro_or_future1: _FutureT[Any],
        __coro_or_future2: _FutureT[Any],
        __coro_or_future3: _FutureT[Any],
        __coro_or_future4: _FutureT[Any],
        __coro_or_future5: _FutureT[Any],
        __coro_or_future6: _FutureT[Any],
        __coro_or_future7: _FutureT[Any],
        __coro_or_future8: _FutureT[Any],
        __coro_or_future9: _FutureT[Any],
        __coro_or_future10: _FutureT[Any],
        *coros_or_futures: _FutureT[Any],
        return_exceptions: bool = ...,
    ) -> Future[list[Any]]:
        ...

    @overload
    def gather(
        __coro_or_future1: _FutureT[_T1], *, return_exceptions: bool = ...
    ) -> Future[tuple[_T1 | BaseException]]:
        ...

    @overload
    def gather(
        __coro_or_future1: _FutureT[_T1],
        __coro_or_future2: _FutureT[_T2],
        *,
        return_exceptions: bool = ...,
    ) -> Future[tuple[_T1 | BaseException, _T2 | BaseException]]:
        ...

    @overload
    def gather(
        __coro_or_future1: _FutureT[_T1],
        __coro_or_future2: _FutureT[_T2],
        __coro_or_future3: _FutureT[_T3],
        *,
        return_exceptions: bool = ...,
    ) -> Future[tuple[_T1 | BaseException, _T2 | BaseException, _T3 | BaseException]]:
        ...

    @overload
    def gather(
        __coro_or_future1: _FutureT[_T1],
        __coro_or_future2: _FutureT[_T2],
        __coro_or_future3: _FutureT[_T3],
        __coro_or_future4: _FutureT[_T4],
        *,
        return_exceptions: bool = ...,
    ) -> Future[
        tuple[
            _T1 | BaseException,
            _T2 | BaseException,
            _T3 | BaseException,
            _T4 | BaseException,
        ]
    ]:
        ...

    @overload
    def gather(
        __coro_or_future1: _FutureT[_T1],
        __coro_or_future2: _FutureT[_T2],
        __coro_or_future3: _FutureT[_T3],
        __coro_or_future4: _FutureT[_T4],
        __coro_or_future5: _FutureT[_T5],
        *,
        return_exceptions: bool = ...,
    ) -> Future[
        tuple[
            _T1 | BaseException,
            _T2 | BaseException,
            _T3 | BaseException,
            _T4 | BaseException,
            _T5 | BaseException,
        ]
    ]:
        ...

    @overload
    def gather(
        __coro_or_future1: _FutureT[_T1],
        __coro_or_future2: _FutureT[_T2],
        __coro_or_future3: _FutureT[_T3],
        __coro_or_future4: _FutureT[_T4],
        __coro_or_future5: _FutureT[_T5],
        __coro_or_future6: _FutureT[_T6],
        *,
        return_exceptions: bool = ...,
    ) -> Future[
        tuple[
            _T1 | BaseException,
            _T2 | BaseException,
            _T3 | BaseException,
            _T4 | BaseException,
            _T5 | BaseException,
            _T6 | BaseException,
        ]
    ]:
        ...

    @overload
    def gather(
        __coro_or_future1: _FutureT[_T1],
        __coro_or_future2: _FutureT[_T2],
        __coro_or_future3: _FutureT[_T3],
        __coro_or_future4: _FutureT[_T4],
        __coro_or_future5: _FutureT[_T5],
        __coro_or_future6: _FutureT[_T6],
        __coro_or_future7: _FutureT[_T7],
        *,
        return_exceptions: bool = ...,
    ) -> Future[
        tuple[
            _T1 | BaseException,
            _T2 | BaseException,
            _T3 | BaseException,
            _T4 | BaseException,
            _T5 | BaseException,
            _T6 | BaseException,
            _T7 | BaseException,
        ]
    ]:
        ...

    @overload
    def gather(
        __coro_or_future1: _FutureT[_T1],
        __coro_or_future2: _FutureT[_T2],
        __coro_or_future3: _FutureT[_T3],
        __coro_or_future4: _FutureT[_T4],
        __coro_or_future5: _FutureT[_T5],
        __coro_or_future6: _FutureT[_T6],
        __coro_or_future7: _FutureT[_T7],
        __coro_or_future8: _FutureT[_T8],
        *,
        return_exceptions: bool = ...,
    ) -> Future[
        tuple[
            _T1 | BaseException,
            _T2 | BaseException,
            _T3 | BaseException,
            _T4 | BaseException,
            _T5 | BaseException,
            _T6 | BaseException,
            _T7 | BaseException,
            _T8 | BaseException,
        ]
    ]:
        ...


async def gather(  # type: ignore
    *coros_or_futures: _FutureT[Any],
    return_exceptions: bool = False,
) -> tuple[Any | BaseException, ...]:
    return await asyncio.gather(*coros_or_futures, return_exceptions=return_exceptions)  # type: ignore


def with_timeout(timeout: int):
    def decorator(
        fn: Callable[ParamsType, Coroutine[Any, Any, ReturnType]]
    ) -> Callable[ParamsType, Coroutine[Any, Any, ReturnType]]:
        @wraps(fn)
        async def wrapper(*args: ParamsType.args, **kwargs: ParamsType.kwargs):
            async with async_timeout(timeout):
                return await fn(*args, **kwargs)

        return wrapper

    return decorator
