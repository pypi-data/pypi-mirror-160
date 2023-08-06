from __future__ import annotations

from enum import IntEnum
from typing import TYPE_CHECKING, Any, Callable, NoReturn, Sequence, Type, Union, Protocol

import vapoursynth as vs

__all__ = [
    'VideoProp', 'VSFunction', 'Matrix', 'VideoFormatT'
]

VideoProp = Union[
    int, Sequence[int],
    float, Sequence[float],
    str, Sequence[str],
    vs.VideoNode, Sequence[vs.VideoNode],
    vs.VideoFrame, Sequence[vs.VideoFrame],
    Callable[..., Any], Sequence[Callable[..., Any]]
]


class VSFunction(Protocol):
    def __call__(self, clip: vs.VideoNode, *args: Any, **kwargs: Any) -> vs.VideoNode:
        ...


if TYPE_CHECKING:
    class Matrix(vs.MatrixCoefficients):
        RGB = 0
        GBR = 0
        BT709 = 1
        UNKNOWN = 2
        FCC = 4
        BT470BG = 5
        SMPTE170M = 6
        SMPTE240M = 7
        YCGCO = 8
        BT2020NC = 9
        BT2020C = 10
        SMPTE2085 = 11
        CHROMA_DERIVED_NC = 12
        CHROMA_DERIVED_C = 13
        ICTCP = 14

        def __new__(cls: type[Matrix], value: int | Matrix | vs.MatrixCoefficients | None) -> Matrix:
            ...
else:
    class Matrix(IntEnum):
        """Matrix coefficients (ITU-T H.265 Table E.5)."""

        _value_: int

        @classmethod
        def _missing_(cls: Type[Matrix], value: Any) -> Matrix | None:
            if value is None:
                return Matrix.UNKNOWN

            return None

        RGB = 0
        GBR = 0
        BT709 = 1
        UNKNOWN = 2
        _RESERVED = 3
        FCC = 4
        BT470BG = 5
        SMPTE170M = 6
        SMPTE240M = 7
        YCGCO = 8
        BT2020NC = 9
        BT2020C = 10
        SMPTE2085 = 11
        CHROMA_DERIVED_NC = 12
        CHROMA_DERIVED_C = 13
        ICTCP = 14

        @property
        def RESERVED(self) -> NoReturn:
            """Disallow matrix, as it is reserved."""
            raise PermissionError

MatrixT = Union[int, vs.MatrixCoefficients, Matrix]
VideoFormatT = Union[int, vs.PresetFormat, vs.VideoFormat]
