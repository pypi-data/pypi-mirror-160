import typing as tp
from functools import reduce

import numpy as np
from numpy import char as npc

from static_frame.core.node_selector import Interface
from static_frame.core.node_selector import InterfaceBatch
from static_frame.core.node_selector import TContainer
from static_frame.core.util import array_from_element_method
from static_frame.core.util import DTYPE_STR
from static_frame.core.util import DTYPE_STR_KINDS
from static_frame.core.util import UFunc
from static_frame.core.util import OPERATORS
from static_frame.core.util import GetItemKeyType
from static_frame.core.util import AnyCallable


if tp.TYPE_CHECKING:
    from static_frame.core.batch import Batch  #pylint: disable = W0611 #pragma: no cover
    from static_frame.core.frame import Frame  #pylint: disable = W0611 #pragma: no cover
    from static_frame.core.index import Index  #pylint: disable = W0611 #pragma: no cover
    from static_frame.core.index_hierarchy import IndexHierarchy  #pylint: disable = W0611 #pragma: no cover
    from static_frame.core.series import Series  #pylint: disable = W0611 #pragma: no cover
    from static_frame.core.type_blocks import TypeBlocks  #pylint: disable = W0611 #pragma: no cover


BlocksType = tp.Iterable[np.ndarray]
ToContainerType = tp.Callable[[tp.Iterator[np.ndarray]], TContainer]

INTERFACE_STR = (
        '__getitem__',
        'capitalize',
        'center',
        'contains',
        'count',
        'decode',
        'encode',
        'endswith',
        'find',
        'index',
        'isalnum',
        'isalpha',
        'isdecimal',
        'isdigit',
        'islower',
        'isnumeric',
        'isspace',
        'istitle',
        'isupper',
        'ljust',
        'len',
        'lower',
        'lstrip',
        'partition',
        'replace',
        'rfind',
        'rindex',
        'rjust',
        'rpartition',
        'rsplit',
        'rstrip',
        'split',
        'startswith',
        'strip',
        'swapcase',
        'title',
        'upper',
        'zfill',
)


class InterfaceString(Interface[TContainer]):

    # NOTE: based on https://numpy.org/doc/stable/reference/routines.char.html

    __slots__ = (
            '_blocks',
            '_blocks_to_container',
            )
    INTERFACE = INTERFACE_STR

    def __init__(self,
            blocks: BlocksType,
            blocks_to_container: ToContainerType[TContainer]
            ) -> None:
        self._blocks: BlocksType = blocks
        self._blocks_to_container: ToContainerType[TContainer] = blocks_to_container

    #---------------------------------------------------------------------------

    @staticmethod
    def _process_blocks(
            blocks: BlocksType,
            func: UFunc,
            args: tp.Tuple[tp.Any, ...] = (),
            astype_str: bool = True,
            ) -> tp.Iterator[np.ndarray]:
        '''
        Block-wise processing of blocks after optional string conversion. Non-string conversion is necessary for ``decode``.
        '''
        for block in blocks:
            if astype_str and block.dtype not in DTYPE_STR_KINDS:
                block = block.astype(DTYPE_STR)
            array = func(block, *args)
            array.flags.writeable = False
            yield array

    @staticmethod
    def _process_tuple_blocks(*,
            blocks: BlocksType,
            method_name: str,
            dtype: np.dtype,
            args: tp.Tuple[tp.Any, ...] = (),
            ) -> tp.Iterator[np.ndarray]:
        '''
        Element-wise processing of a methods on objects in a block, with pre-insert conversion to a tuple.
        '''
        for block in blocks:
            if block.dtype not in DTYPE_STR_KINDS:
                block = block.astype(DTYPE_STR)

            # resultant array is immutable
            array = array_from_element_method(
                    array=block,
                    method_name=method_name,
                    args=args,
                    dtype=dtype,
                    pre_insert=tuple,
                    )
            yield array

    @staticmethod
    def _process_element_blocks(*,
            blocks: BlocksType,
            method_name: str,
            dtype: np.dtype,
            args: tp.Tuple[tp.Any, ...] = (),
            ) -> tp.Iterator[np.ndarray]:
        '''
        Element-wise processing of a methods on objects in a block, with pre-insert conversion to a tuple.
        '''
        for block in blocks:
            if block.dtype not in DTYPE_STR_KINDS:
                block = block.astype(DTYPE_STR)

            # resultant array is immutable
            array = array_from_element_method(
                    array=block,
                    method_name=method_name,
                    args=args,
                    dtype=dtype,
                    )
            yield array


    #---------------------------------------------------------------------------
    def __getitem__(self,  key: GetItemKeyType) -> TContainer:
        '''
        Return a container with the provided selection or slice of each element.
        '''
        block_gen = self._process_element_blocks(
                blocks=self._blocks,
                method_name='__getitem__',
                args=(key,),
                dtype=DTYPE_STR,
                )
        return self._blocks_to_container(block_gen)

    def capitalize(self) -> TContainer:
        '''
        Return a container with only the first character of each element capitalized.
        '''
        # return self._blocks_to_container(npc.capitalize(self._blocks()))
        block_gen = self._process_blocks(self._blocks, npc.capitalize)
        return self._blocks_to_container(block_gen)

    def center(self,
            width: int,
            fillchar: str = ' '
            ) -> TContainer:
        '''
        Return a container with its elements centered in a string of length ``width``.
        '''
        block_gen = self._process_blocks(self._blocks, npc.center, (width, fillchar))
        return self._blocks_to_container(block_gen)

    def contains(self,  item: str) -> TContainer:
        '''
        Return a Boolean container showing True of item is a substring of elements.
        '''
        block_gen = self._process_element_blocks(
                blocks=self._blocks,
                method_name='__contains__',
                args=(item,),
                dtype=DTYPE_STR,
                )
        return self._blocks_to_container(block_gen)

    def count(self,
            sub: str,
            start: tp.Optional[int] = None,
            end: tp.Optional[int] = None
            ) -> TContainer:
        '''
        Returns a container with the number of non-overlapping occurrences of substring sub in the optional range ``start``, ``end``.
        '''
        block_gen = self._process_blocks(self._blocks, npc.count, (sub, start, end))
        return self._blocks_to_container(block_gen)

    def decode(self,
            encoding: tp.Optional[str] = None,
            errors: tp.Optional[str] = None,
            ) -> TContainer:
        '''
        Apply str.decode() to each element. Elements must be bytes.
        '''
        block_gen = self._process_blocks(
                blocks=self._blocks,
                func=npc.decode,
                args=(encoding, errors),
                astype_str=False, # needs to be bytes
                )
        return self._blocks_to_container(block_gen)

    def encode(self,
            encoding: tp.Optional[str] = None,
            errors: tp.Optional[str] = None,
            ) -> TContainer:
        '''
        Apply str.encode() to each element. Elements must be strings.
        '''
        block_gen = self._process_blocks(self._blocks, npc.encode, (encoding, errors))
        return self._blocks_to_container(block_gen)

    def endswith(self,
            suffix: tp.Union[str, tp.Iterable[str]],
            start: tp.Optional[int] = None,
            end: tp.Optional[int] = None
            ) -> TContainer:
        '''
        Returns a container with the number of non-overlapping occurrences of substring ``suffix`` (or an interable of suffixes) in the optional range ``start``, ``end``.
        '''

        if isinstance(suffix, str):
            block_iter = self._process_blocks(self._blocks, npc.endswith, (suffix, start, end))
            return self._blocks_to_container(block_iter)

        def block_gen() -> tp.Iterator[np.ndarray]:
            blocks_per_sub = (
                    self._process_blocks(self._blocks, npc.endswith, (sub, start, end))
                    for sub in suffix)
            func = OPERATORS['__or__']
            for block_layers in zip(*blocks_per_sub):
                array = reduce(func, block_layers)
                array.flags.writeable = False
                yield array

        return self._blocks_to_container(block_gen())

    def find(self,
            sub: str,
            start: tp.Optional[int] = None,
            end: tp.Optional[int] = None
            ) -> TContainer:
        '''
        For each element, return the lowest index in the string where substring ``sub`` is found.
        '''
        block_gen = self._process_blocks(self._blocks, npc.find, (sub, start, end))
        return self._blocks_to_container(block_gen)

    def index(self,
            sub: str,
            start: tp.Optional[int] = None,
            end: tp.Optional[int] = None
            ) -> TContainer:
        '''
        Like ``find``, but raises ``ValueError`` when the substring is not found.
        '''
        block_gen = self._process_blocks(self._blocks, npc.index, (sub, start, end))
        return self._blocks_to_container(block_gen)

    def isalnum(self) -> TContainer:
        '''
        Returns true for each element if all characters in the string are alphanumeric and there is at least one character, false otherwise.
        '''
        block_gen = self._process_blocks(self._blocks, npc.isalnum)
        return self._blocks_to_container(block_gen)

    def isalpha(self) -> TContainer:
        '''
        Returns true for each element if all characters in the string are alphabetic and there is at least one character, false otherwise.
        '''
        block_gen = self._process_blocks(self._blocks, npc.isalpha)
        return self._blocks_to_container(block_gen)

    def isdecimal(self) -> TContainer:
        '''
        For each element, return True if there are only decimal characters in the element.
        '''
        block_gen = self._process_blocks(self._blocks, npc.isdecimal)
        return self._blocks_to_container(block_gen)

    def isdigit(self) -> TContainer:
        '''
        Returns true for each element if all characters in the string are digits and there is at least one character, false otherwise.
        '''
        block_gen = self._process_blocks(self._blocks, npc.isdigit)
        return self._blocks_to_container(block_gen)

    def islower(self) -> TContainer:
        '''
        Returns true for each element if all cased characters in the string are lowercase and there is at least one cased character, false otherwise.
        '''
        block_gen = self._process_blocks(self._blocks, npc.islower)
        return self._blocks_to_container(block_gen)

    def isnumeric(self) -> TContainer:
        '''
        For each element in self, return True if there are only numeric characters in the element.
        '''
        block_gen = self._process_blocks(self._blocks, npc.isnumeric)
        return self._blocks_to_container(block_gen)

    def isspace(self) -> TContainer:
        '''
        Returns true for each element if there are only whitespace characters in the string and there is at least one character, false otherwise.
        '''
        block_gen = self._process_blocks(self._blocks, npc.isspace)
        return self._blocks_to_container(block_gen)

    def istitle(self) -> TContainer:
        '''
        Returns true for each element if the element is a titlecased string and there is at least one character, false otherwise.
        '''
        block_gen = self._process_blocks(self._blocks, npc.istitle)
        return self._blocks_to_container(block_gen)

    def isupper(self) -> TContainer:
        '''
        Returns true for each element if all cased characters in the string are uppercase and there is at least one character, false otherwise.
        '''
        block_gen = self._process_blocks(self._blocks, npc.isupper)
        return self._blocks_to_container(block_gen)

    def len(self) -> TContainer:
        '''
        Return the length of the string.
        '''
        block_gen = self._process_blocks(self._blocks, npc.str_len)
        return self._blocks_to_container(block_gen)

    def ljust(self,
            width: int,
            fillchar: str = ' '
            ) -> TContainer:
        '''
        Return a container with its elements ljusted in a string of length ``width``.
        '''
        block_gen = self._process_blocks(self._blocks, npc.ljust, (width, fillchar))
        return self._blocks_to_container(block_gen)

    def lower(self) -> TContainer:
        '''
        Return an array with the elements of self converted to lowercase.
        '''
        block_gen = self._process_blocks(self._blocks, npc.lower)
        return self._blocks_to_container(block_gen)

    def lstrip(self,
            chars: tp.Optional[str] = None,
            ) -> TContainer:
        '''
        For each element, return a copy with the leading characters removed.
        '''
        block_gen = self._process_blocks(self._blocks, npc.lstrip, (chars,))
        return self._blocks_to_container(block_gen)

    def partition(self,
            sep: str,
            ) -> TContainer:
        '''
        Partition each element around ``sep``.
        '''
        # NOTE: py str.partition gives a tuple.
        block_gen = self._process_tuple_blocks(
                blocks=self._blocks,
                method_name='partition',
                args=(sep,),
                dtype=object
                )
        return self._blocks_to_container(block_gen)

    def replace(self,
            old: str,
            new: str,
            count: tp.Optional[int] = None,
            ) -> TContainer:
        '''
        Return a container with its elements replaced in a string of length ``width``.
        '''
        block_gen = self._process_blocks(self._blocks, npc.replace, (old, new, count))
        return self._blocks_to_container(block_gen)

    def rfind(self,
            sub: str,
            start: tp.Optional[int] = None,
            end: tp.Optional[int] = None
            ) -> TContainer:
        '''
        For each element, return the highest index in the string where substring ``sub`` is found, such that sub is contained within ``start``, ``end``.
        '''
        block_gen = self._process_blocks(self._blocks, npc.rfind, (sub, start, end))
        return self._blocks_to_container(block_gen)

    def rindex(self,
            sub: str,
            start: tp.Optional[int] = None,
            end: tp.Optional[int] = None
            ) -> TContainer:
        '''
        Like ``rfind``, but raises ``ValueError`` when the substring ``sub`` is not found.
        '''
        block_gen = self._process_blocks(self._blocks, npc.rindex, (sub, start, end))
        return self._blocks_to_container(block_gen)

    def rjust(self,
            width: int,
            fillchar: str = ' '
            ) -> TContainer:
        '''
        Return a container with its elements rjusted in a string of length ``width``.
        '''
        block_gen = self._process_blocks(self._blocks, npc.rjust, (width, fillchar))
        return self._blocks_to_container(block_gen)

    def rpartition(self,
            sep: str,
            ) -> TContainer:
        '''
        Partition (split) each element around the right-most separator.
        '''
        # NOTE: py str.rpartition gives a tuple.
        block_gen = self._process_tuple_blocks(
                blocks=self._blocks,
                method_name='rpartition',
                args=(sep,),
                dtype=object
                )
        return self._blocks_to_container(block_gen)

    def rsplit(self,
            sep: str,
            maxsplit: int = -1,
            ) -> TContainer:
        '''
        For each element, return a tuple of the words in the string, using sep as the delimiter string.
        '''
        # NOTE: npc.rsplit gives an array of lists, so implement our own routine to get an array of tuples.
        block_gen = self._process_tuple_blocks(
                blocks=self._blocks,
                method_name='rsplit',
                args=(sep, maxsplit),
                dtype=object
                )
        return self._blocks_to_container(block_gen)

    def rstrip(self,
            chars: tp.Optional[str] = None,
            ) -> TContainer:
        '''
        For each element, return a copy with the trailing characters removed.
        '''
        block_gen = self._process_blocks(self._blocks, npc.rstrip, (chars,))
        return self._blocks_to_container(block_gen)

    def split(self,
            sep: str,
            maxsplit: int = -1,
            ) -> TContainer:
        '''
        For each element, return a tuple of the words in the string, using sep as the delimiter string.
        '''
        # NOTE: npc.split gives an array of lists, so implement our own routine to get an array of tuples.
        block_gen = self._process_tuple_blocks(
                blocks=self._blocks,
                method_name='split',
                args=(sep, maxsplit),
                dtype=object
                )
        return self._blocks_to_container(block_gen)

    #splitlines: not likely useful

    def startswith(self,
            prefix: tp.Union[str, tp.Iterable[str]],
            start: tp.Optional[int] = None,
            end: tp.Optional[int] = None
            ) -> TContainer:
        '''
        Returns a container with the number of non-overlapping occurrences of substring `prefix` (or an interable of prefixes) in the optional range ``start``, ``end``.
        '''
        if isinstance(prefix, str):
            block_iter = self._process_blocks(self._blocks, npc.startswith, (prefix, start, end))
            return self._blocks_to_container(block_iter)

        def block_gen() -> tp.Iterator[np.ndarray]:
            blocks_per_sub = (
                    self._process_blocks(self._blocks, npc.startswith, (sub, start, end))
                    for sub in prefix)
            func = OPERATORS['__or__']
            for block_layers in zip(*blocks_per_sub):
                array = reduce(func, block_layers)
                array.flags.writeable = False
                yield array

        return self._blocks_to_container(block_gen())

    def strip(self,
            chars: tp.Optional[str] = None,
            ) -> TContainer:
        '''
        For each element, return a copy with the leading and trailing characters removed.
        '''
        block_gen = self._process_blocks(self._blocks, npc.strip, (chars,))
        return self._blocks_to_container(block_gen)

    def swapcase(self) -> TContainer:
        '''
        Return a container with uppercase characters converted to lowercase and vice versa.
        '''
        block_gen = self._process_blocks(self._blocks, npc.swapcase)
        return self._blocks_to_container(block_gen)

    def title(self) -> TContainer:
        '''
        Return a container with uppercase characters converted to lowercase and vice versa.
        '''
        block_gen = self._process_blocks(self._blocks, npc.title)
        return self._blocks_to_container(block_gen)

    # translate: akward input

    def upper(self) -> TContainer:
        '''
        Return a container with uppercase characters converted to lowercase and vice versa.
        '''
        block_gen = self._process_blocks(self._blocks, npc.upper)
        return self._blocks_to_container(block_gen)

    def zfill(self,
            width: int,
            ) -> TContainer:
        '''
        Return the string left-filled with zeros.
        '''
        block_gen = self._process_blocks(self._blocks, npc.zfill, (width,))
        return self._blocks_to_container(block_gen)



class InterfaceBatchString(InterfaceBatch):
    '''Alternate string interface specialized for the :obj:`Batch`.
    '''
    __slots__ = (
            '_batch_apply',
            )
    INTERFACE = INTERFACE_STR

    def __init__(self,
            batch_apply: tp.Callable[[AnyCallable], 'Batch'],
            ) -> None:
        self._batch_apply = batch_apply

    #---------------------------------------------------------------------------
    def __getitem__(self,  key: GetItemKeyType) -> 'Batch':
        '''
        Return a container with the provided selection or slice of each element.
        '''
        return self._batch_apply(lambda c: c.via_str.__getitem__(key))


    def capitalize(self) -> 'Batch':
        '''
        Return a container with only the first character of each element capitalized.
        '''
        return self._batch_apply(lambda c: c.via_str.capitalize())

    def center(self,
            width: int,
            fillchar: str = ' '
            ) -> 'Batch':
        '''
        Return a container with its elements centered in a string of length ``width``.
        '''
        return self._batch_apply(lambda c: c.via_str.center(width, fillchar))

    def count(self,
            sub: str,
            start: tp.Optional[int] = None,
            end: tp.Optional[int] = None
            ) -> 'Batch':
        '''
        Returns a container with the number of non-overlapping occurrences of substring sub in the optional range ``start``, ``end``.
        '''
        return self._batch_apply(lambda c: c.via_str.count(sub, start, end))

    def contains(self,
            item: str,
            ) -> 'Batch':
        '''
        Returns a container with the number of non-overlapping occurrences of substring sub in the optional range ``start``, ``end``.
        '''
        return self._batch_apply(lambda c: c.via_str.contains(item))

    def decode(self,
            encoding: tp.Optional[str] = None,
            errors: tp.Optional[str] = None,
            ) -> 'Batch':
        '''
        Apply str.decode() to each element. Elements must be bytes.
        '''
        return self._batch_apply(lambda c: c.via_str.decode(encoding, errors))

    def encode(self,
            encoding: tp.Optional[str] = None,
            errors: tp.Optional[str] = None,
            ) -> 'Batch':
        '''
        Apply str.encode() to each element. Elements must be strings.
        '''
        return self._batch_apply(lambda c: c.via_str.encode(encoding, errors))

    def endswith(self,
            suffix: tp.Union[str, tp.Iterable[str]],
            start: tp.Optional[int] = None,
            end: tp.Optional[int] = None
            ) -> 'Batch':
        '''
        Returns a container with the number of non-overlapping occurrences of substring ``suffix`` (or an interable of suffixes) in the optional range ``start``, ``end``.
        '''
        return self._batch_apply(lambda c: c.via_str.endswith(suffix, start, end))

    def find(self,
            sub: str,
            start: tp.Optional[int] = None,
            end: tp.Optional[int] = None
            ) -> 'Batch':
        '''
        For each element, return the lowest index in the string where substring ``sub`` is found.
        '''
        return self._batch_apply(lambda c: c.via_str.find(sub, start, end))

    def index(self,
            sub: str,
            start: tp.Optional[int] = None,
            end: tp.Optional[int] = None
            ) -> 'Batch':
        '''
        Like ``find``, but raises ``ValueError`` when the substring is not found.
        '''
        return self._batch_apply(lambda c: c.via_str.index(sub, start, end))

    def isalnum(self) -> 'Batch':
        '''
        Returns true for each element if all characters in the string are alphanumeric and there is at least one character, false otherwise.
        '''
        return self._batch_apply(lambda c: c.via_str.isalnum())

    def isalpha(self) -> 'Batch':
        '''
        Returns true for each element if all characters in the string are alphabetic and there is at least one character, false otherwise.
        '''
        return self._batch_apply(lambda c: c.via_str.isalpha())

    def isdecimal(self) -> 'Batch':
        '''
        For each element, return True if there are only decimal characters in the element.
        '''
        return self._batch_apply(lambda c: c.via_str.isdecimal())

    def isdigit(self) -> 'Batch':
        '''
        Returns true for each element if all characters in the string are digits and there is at least one character, false otherwise.
        '''
        return self._batch_apply(lambda c: c.via_str.isdigit())

    def islower(self) -> 'Batch':
        '''
        Returns true for each element if all cased characters in the string are lowercase and there is at least one cased character, false otherwise.
        '''
        return self._batch_apply(lambda c: c.via_str.islower())

    def isnumeric(self) -> 'Batch':
        '''
        For each element in self, return True if there are only numeric characters in the element.
        '''
        return self._batch_apply(lambda c: c.via_str.isnumeric())

    def isspace(self) -> 'Batch':
        '''
        Returns true for each element if there are only whitespace characters in the string and there is at least one character, false otherwise.
        '''
        return self._batch_apply(lambda c: c.via_str.isspace())

    def istitle(self) -> 'Batch':
        '''
        Returns true for each element if the element is a titlecased string and there is at least one character, false otherwise.
        '''
        return self._batch_apply(lambda c: c.via_str.istitle())

    def isupper(self) -> 'Batch':
        '''
        Returns true for each element if all cased characters in the string are uppercase and there is at least one character, false otherwise.
        '''
        return self._batch_apply(lambda c: c.via_str.isupper())

    def len(self) -> 'Batch':
        '''
        Return the length of the string.
        '''
        return self._batch_apply(lambda c: c.via_str.len())

    def ljust(self,
            width: int,
            fillchar: str = ' '
            ) -> 'Batch':
        '''
        Return a container with its elements ljusted in a string of length ``width``.
        '''
        return self._batch_apply(lambda c: c.via_str.ljust(width, fillchar))

    def lower(self) -> 'Batch':
        '''
        Return an array with the elements of self converted to lowercase.
        '''
        return self._batch_apply(lambda c: c.via_str.lower())

    def lstrip(self,
            chars: tp.Optional[str] = None,
            ) -> 'Batch':
        '''
        For each element, return a copy with the leading characters removed.
        '''
        return self._batch_apply(lambda c: c.via_str.lstrip(chars))

    def partition(self,
            sep: str,
            ) -> 'Batch':
        '''
        Partition each element around ``sep``.
        '''
        return self._batch_apply(lambda c: c.via_str.partition(sep))

    def replace(self,
            old: str,
            new: str,
            count: tp.Optional[int] = None,
            ) -> 'Batch':
        '''
        Return a container with its elements replaced in a string of length ``width``.
        '''
        return self._batch_apply(lambda c: c.via_str.replace(old, new, count))

    def rfind(self,
            sub: str,
            start: tp.Optional[int] = None,
            end: tp.Optional[int] = None
            ) -> 'Batch':
        '''
        For each element, return the highest index in the string where substring ``sub`` is found, such that sub is contained within ``start``, ``end``.
        '''
        return self._batch_apply(lambda c: c.via_str.rfind(sub, start, end))

    def rindex(self,
            sub: str,
            start: tp.Optional[int] = None,
            end: tp.Optional[int] = None
            ) -> 'Batch':
        '''
        Like ``rfind``, but raises ``ValueError`` when the substring ``sub`` is not found.
        '''
        return self._batch_apply(lambda c: c.via_str.rindex(sub, start, end))

    def rjust(self,
            width: int,
            fillchar: str = ' '
            ) -> 'Batch':
        '''
        Return a container with its elements rjusted in a string of length ``width``.
        '''
        return self._batch_apply(lambda c: c.via_str.rjust(width, fillchar))

    def rpartition(self,
            sep: str,
            ) -> 'Batch':
        '''
        Partition (split) each element around the right-most separator.
        '''
        return self._batch_apply(lambda c: c.via_str.rpartition(sep))

    def rsplit(self,
            sep: str,
            maxsplit: int = -1,
            ) -> 'Batch':
        '''
        For each element, return a tuple of the words in the string, using sep as the delimiter string.
        '''
        return self._batch_apply(lambda c: c.via_str.rsplit(sep, maxsplit))

    def rstrip(self,
            chars: tp.Optional[str] = None,
            ) -> 'Batch':
        '''
        For each element, return a copy with the trailing characters removed.
        '''
        return self._batch_apply(lambda c: c.via_str.rstrip(chars))

    def split(self,
            sep: str,
            maxsplit: int = -1,
            ) -> 'Batch':
        '''
        For each element, return a tuple of the words in the string, using sep as the delimiter string.
        '''
        return self._batch_apply(lambda c: c.via_str.split(sep, maxsplit))

    #splitlines: not likely useful

    def startswith(self,
            prefix: tp.Union[str, tp.Iterable[str]],
            start: tp.Optional[int] = None,
            end: tp.Optional[int] = None
            ) -> 'Batch':
        '''
        Returns a container with the number of non-overlapping occurrences of substring `prefix` (or an interable of prefixes) in the optional range ``start``, ``end``.
        '''
        return self._batch_apply(lambda c: c.via_str.startswith(prefix, start, end))

    def strip(self,
            chars: tp.Optional[str] = None,
            ) -> 'Batch':
        '''
        For each element, return a copy with the leading and trailing characters removed.
        '''
        return self._batch_apply(lambda c: c.via_str.strip(chars))

    def swapcase(self) -> 'Batch':
        '''
        Return a container with uppercase characters converted to lowercase and vice versa.
        '''
        return self._batch_apply(lambda c: c.via_str.swapcase())

    def title(self) -> 'Batch':
        '''
        Return a container with uppercase characters converted to lowercase and vice versa.
        '''
        return self._batch_apply(lambda c: c.via_str.title())

    # translate: akward input

    def upper(self) -> 'Batch':
        '''
        Return a container with uppercase characters converted to lowercase and vice versa.
        '''
        return self._batch_apply(lambda c: c.via_str.upper())

    def zfill(self,
            width: int,
            ) -> 'Batch':
        '''
        Return the string left-filled with zeros.
        '''
        return self._batch_apply(lambda c: c.via_str.zfill(width))

