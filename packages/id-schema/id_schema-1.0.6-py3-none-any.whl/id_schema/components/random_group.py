from typing import *
from .base_component import BaseComponent
import random
import collections


class LengthRange:
    def __init__(self, min_length: int, max_length: Optional[int] = None):
        self.min = min_length
        self.max = max_length if max_length is not None else min_length
        self._validate_range()
        
    def _validate_range(self) -> None:
        if self.min > self.max:
            raise ValueError("Constraint failed: min <= max.")

    def one_in_range(self) -> int:
        return random.randint(self.min, self.max)

    def __contains__(self, number: int) -> bool:
        return self.min <= number <= self.max

    def __iter__(self):
        return iter(range(self.min, self.max+1))

class LengthSequence:
    def __init__(self, *lengths) -> None:
        self.lengths = self._parse_lengths(lengths)
    
    def _parse_lengths(self, lengths):
        if len(lengths) == 0:
            raise ValueError("you have to specify at least one length!")
        if isinstance(lengths[0], collections.abc.Sequence):
            return lengths[0]
        if not all(map(lambda x: isinstance(x, int), lengths)):
            raise TypeError("all arguments have to be of type 'int'.")
        return lengths

    def one_in_range(self) -> int:
        return random.choice(self.lengths)

    def __contains__(self, number: int) -> bool:
        return number in self.lengths

    def __iter__(self):
        return iter(self.lengths)


class RandomGroup(BaseComponent):
    def __init__(self, alphabet: Sequence[str], length: Union[LengthRange,LengthSequence,int,None] = None, weights: Optional[Sequence[float]] = None, unique: bool=False) -> None:
        if not isinstance(alphabet, str):
            raise TypeError(f"alphabet has to be of type 'str', not '{str(alphabet.__class__.__name__)}'.")
        if len(set(alphabet)) != len(alphabet):
            raise ValueError(f"alphabet has to be unique.")
        self.alphabet = alphabet
        self.length = self._parse_length(length)
        self.weights = weights
        self.unique = unique


    def _parse_length(self, length: Union[LengthRange,LengthSequence,int,None]) -> Union[LengthRange, LengthSequence]:
        if length is None:
            return LengthSequence(len(self.alphabet))
        if isinstance(length, int):
            return LengthSequence(length)
        if isinstance(length, (LengthRange, LengthSequence)):
            return length
        raise TypeError("type of 'length' has to be one of ('LengthRange', 'LengthSequence', 'int', 'NoneType').")

    def generate(self) -> str:
        if self.unique:
            return "".join(random.sample(self.alphabet, self.length.one_in_range()))
        return "".join(random.choices(self.alphabet, weights=self.weights, k=self.length.one_in_range()))


    def validate(self, group: Sequence[str]) -> bool:
        if len(group) not in self.length:
            return False

        if self.unique and len(set(group)) != len(group):
            return False

        return all(map(lambda x: x in self.alphabet, group))

    def reduce_all_matching(self, sub_id: str) -> Iterator[str]:
        for i in self.length:
            if self.validate(sub_id[:i]):
                yield sub_id[i:]
