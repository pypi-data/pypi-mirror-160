from .values import Float, Symbol, Record, ImmutableDict, Embedded, preserve
from .values import Annotated, is_annotated, strip_annotations, annotate

from .compare import cmp

from .error import DecodeError, EncodeError, ShortPacket

from .binary import Decoder, Encoder, decode, decode_with_annotations, encode, canonicalize
from .text import Parser, Formatter, parse, parse_with_annotations, stringify

from .merge import merge

from . import fold, compare

loads = parse
dumps = stringify
