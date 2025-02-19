import sys
from typing import Any, Callable, Generic, Dict, Iterable, Mapping, Optional, Sequence, Tuple, Type, TypeVar, NamedTuple, Union, overload

_AnyCallable = Callable[..., Any]

_T = TypeVar("_T")
_S = TypeVar("_S")
@overload
def reduce(function: Callable[[_T, _S], _T],
           sequence: Iterable[_S], initial: _T) -> _T: ...
@overload
def reduce(function: Callable[[_T, _T], _T],
           sequence: Iterable[_T]) -> _T: ...


class _CacheInfo(NamedTuple('CacheInfo', [
    ('hits', int),
    ('misses', int),
    ('maxsize', int),
    ('currsize', int)
])): ...

class _lru_cache_wrapper(Generic[_T]):
    __wrapped__: Callable[..., _T]
    def __call__(self, *args: Any, **kwargs: Any) -> _T: ...
    def cache_info(self) -> _CacheInfo: ...
    def cache_clear(self) -> None: ...

class lru_cache():
    def __init__(self, maxsize: Optional[int] = ..., typed: bool = ...) -> None: ...
    def __call__(self, f: Callable[..., _T]) -> _lru_cache_wrapper[_T]: ...


WRAPPER_ASSIGNMENTS: Sequence[str]
WRAPPER_UPDATES: Sequence[str]

def update_wrapper(wrapper: _AnyCallable, wrapped: _AnyCallable, assigned: Sequence[str] = ...,
                   updated: Sequence[str] = ...) -> _AnyCallable: ...
def wraps(wrapped: _AnyCallable, assigned: Sequence[str] = ..., updated: Sequence[str] = ...) -> Callable[[_AnyCallable], _AnyCallable]: ...
def total_ordering(cls: type) -> type: ...
def cmp_to_key(mycmp: Callable[[_T, _T], int]) -> Callable[[_T], Any]: ...

class partial(Generic[_T]):
    func: Callable[..., _T]
    args: Tuple[Any, ...]
    keywords: Dict[str, Any]
    def __init__(self, func: Callable[..., _T], *args: Any, **kwargs: Any) -> None: ...
    def __call__(self, *args: Any, **kwargs: Any) -> _T: ...

# With protocols, this could change into a generic protocol that defines __get__ and returns _T
_Descriptor = Any

class partialmethod(Generic[_T]):
    func: Union[Callable[..., _T], _Descriptor]
    args: Tuple[Any, ...]
    keywords: Dict[str, Any]

    @overload
    def __init__(self, func: Callable[..., _T], *args: Any, **keywords: Any) -> None: ...
    @overload
    def __init__(self, func: _Descriptor, *args: Any, **keywords: Any) -> None: ...
    def __get__(self, obj: Any, cls: Type[Any]) -> Callable[..., _T]: ...
    @property
    def __isabstractmethod__(self) -> bool: ...

class _SingleDispatchCallable(Generic[_T]):
    registry: Mapping[Any, Callable[..., _T]]
    def dispatch(self, cls: Any) -> Callable[..., _T]: ...
    @overload
    def register(self, cls: Any) -> Callable[[Callable[..., _T]], Callable[..., _T]]: ...
    @overload
    def register(self, cls: Any, func: Callable[..., _T]) -> Callable[..., _T]: ...
    def _clear_cache(self) -> None: ...
    def __call__(self, *args: Any, **kwargs: Any) -> _T: ...

def singledispatch(func: Callable[..., _T]) -> _SingleDispatchCallable[_T]: ...

def _make_key(args, kwds, typed,
             kwd_mark = (object(),),
             fasttypes = {int, str, frozenset, type(None)},
             tuple=tuple, type=type, len=len): pass