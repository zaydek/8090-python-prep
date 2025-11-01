from typing import Generic, TypeVar, NamedTuple

T = TypeVar("T")
E = TypeVar("E")


class Ok(NamedTuple, Generic[T]):
    value: T


class Err(NamedTuple, Generic[E]):
    error: E


type Result[T, E] = Ok[T] | Err[E]
