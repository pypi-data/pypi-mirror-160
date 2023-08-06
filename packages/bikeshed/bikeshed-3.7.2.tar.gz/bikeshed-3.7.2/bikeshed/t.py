# pylint: disable=unused-import
# Module for holding types, for easy importing into the rest of the codebase
from __future__ import annotations

import sys
from typing import (
    Any,
    cast,
    Callable,
    DefaultDict,
    Deque,
    Dict,
    Generator,
    Iterable,
    Iterator,
    List,
    Mapping,
    Optional,
    overload,
    Sequence,
    Set,
    Tuple,
    TYPE_CHECKING,
    TypeVar,
    Union,
)

from lxml import etree
from typing_extensions import Literal, TypeAlias


ElementT: TypeAlias = etree._Element  # pylint: disable=protected-access
DocumentT: TypeAlias = etree._ElementTree  # pylint: disable=protected-access
NodeT: TypeAlias = Union[str, ElementT]

# Can't actually do recursive types yet :(
# Get as close as possible, but let lists be Any
NodesT: TypeAlias = Union[NodeT, List]


if TYPE_CHECKING:
    if "Spec" not in sys.modules:
        from .Spec import Spec  # pylint: disable=cyclic-import
    SpecT = Spec

if TYPE_CHECKING:
    from . import biblio  # pylint: disable=cyclic-import

    BiblioStorageT: TypeAlias = DefaultDict[str, List[biblio.BiblioEntry]]

if TYPE_CHECKING:
    FillContainersT: TypeAlias = DefaultDict[str, List[ElementT]]
