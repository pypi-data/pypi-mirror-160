#
# This is an implementation of [Preserves Schema](https://preserves.dev/preserves-schema.html)
# for Python 3.
#

from . import *
import pathlib
import keyword

AND = Symbol('and')
ANY = Symbol('any')
ATOM = Symbol('atom')
BOOLEAN = Symbol('Boolean')
BUNDLE = Symbol('bundle')
BYTE_STRING = Symbol('ByteString')
DEFINITIONS = Symbol('definitions')
DICT = Symbol('dict')
DICTOF = Symbol('dictof')
DOUBLE = Symbol('Double')
EMBEDDED = Symbol('embedded')
FLOAT = Symbol('Float')
LIT = Symbol('lit')
NAMED = Symbol('named')
OR = Symbol('or')
REC = Symbol('rec')
REF = Symbol('ref')
SCHEMA = Symbol('schema')
SEQOF = Symbol('seqof')
SETOF = Symbol('setof')
SIGNED_INTEGER = Symbol('SignedInteger')
STRING = Symbol('String')
SYMBOL = Symbol('Symbol')
TUPLE = Symbol('tuple')
TUPLE_PREFIX = Symbol('tuplePrefix')
VERSION = Symbol('version')

def sequenceish(x):
    return isinstance(x, tuple) or isinstance(x, list)

class SchemaDecodeFailed(ValueError):
    def __init__(self, cls, p, v, failures=None):
        super().__init__()
        self.cls = cls
        self.pattern = p
        self.value = v
        self.failures = [] if failures is None else failures

    def __str__(self):
        b = ExplanationBuilder()
        return f'Could not decode {b.truncated(stringify(self.value))} using {self.cls}' + \
            b.explain(self)

class ExplanationBuilder:
    INDENT = 2
    def __init__(self):
        self.indentLevel = self.INDENT
        self.deepest_failure = (-1, None)

    def truncated(self, s):
        return s[:36] + ' ...' if len(s) > 40 else s

    def explain(self, failure):
        tree = self._tree(failure)
        deepest = self.deepest_failure[1]
        if deepest is None:
            return tree
        else:
            return f'\nMost likely reason: {self._node(deepest)}\nFull explanation: {tree}'

    def _node(self, failure):
        pexp = ' matching' if failure.pattern is None else f' {stringify(failure.pattern)} didn\'t match'
        c = failure.cls.__module__ + '.' + failure.cls.__qualname__
        return f'in {c}:{pexp} {self.truncated(stringify(failure.value))}'

    def _tree(self, failure):
        if self.indentLevel >= self.deepest_failure[0]:
            self.deepest_failure = (self.indentLevel, failure)
        self.indentLevel += self.INDENT
        nested = [self._tree(f) for f in failure.failures]
        self.indentLevel -= self.INDENT
        return '\n' + ' ' * self.indentLevel + self._node(failure) + ''.join(nested)

class SchemaObject:
    ROOTNS = None
    SCHEMA = None
    MODULE_PATH = None
    NAME = None
    VARIANT = None

    @classmethod
    def decode(cls, v):
        raise NotImplementedError('Subclass responsibility')

    @classmethod
    def try_decode(cls, v):
        try:
            return cls.decode(v)
        except SchemaDecodeFailed:
            return None

    @classmethod
    def parse(cls, p, v, args):
        if p == ANY:
            return v
        if p.key == NAMED:
            i = cls.parse(p[1], v, args)
            args.append(i)
            return i
        if p.key == ATOM:
            k = p[0]
            if k == BOOLEAN and isinstance(v, bool): return v
            if k == FLOAT and isinstance(v, Float): return v
            if k == DOUBLE and isinstance(v, float): return v
            if k == SIGNED_INTEGER and isinstance(v, int): return v
            if k == STRING and isinstance(v, str): return v
            if k == BYTE_STRING and isinstance(v, bytes): return v
            if k == SYMBOL and isinstance(v, Symbol): return v
            raise SchemaDecodeFailed(cls, p, v)
        if p.key == EMBEDDED:
            if not isinstance(v, Embedded): raise SchemaDecodeFailed(cls, p, v)
            return v.embeddedValue
        if p.key == LIT:
            if v == p[0]: return ()
            raise SchemaDecodeFailed(cls, p, v)
        if p.key == SEQOF:
            if not sequenceish(v): raise SchemaDecodeFailed(cls, p, v)
            return [cls.parse(p[0], w, args) for w in v]
        if p.key == SETOF:
            if not isinstance(v, set): raise SchemaDecodeFailed(cls, p, v)
            return set(cls.parse(p[0], w, args) for w in v)
        if p.key == DICTOF:
            if not isinstance(v, dict): raise SchemaDecodeFailed(cls, p, v)
            return dict((cls.parse(p[0], k, args), cls.parse(p[1], w, args))
                        for (k, w) in v.items())
        if p.key == REF:
            c = lookup(cls.ROOTNS, cls.MODULE_PATH if len(p[0]) == 0 else p[0], p[1])
            failure = None
            try:
                return c.decode(v)
            except SchemaDecodeFailed as exn:
                failure = exn
            raise SchemaDecodeFailed(cls, p, v, [failure])
        if p.key == REC:
            if not isinstance(v, Record): raise SchemaDecodeFailed(cls, p, v)
            cls.parse(p[0], v.key, args)
            cls.parse(p[1], v.fields, args)
            return ()
        if p.key == TUPLE:
            if not sequenceish(v): raise SchemaDecodeFailed(cls, p, v)
            if len(v) != len(p[0]): raise SchemaDecodeFailed(cls, p, v)
            i = 0
            for pp in p[0]:
                cls.parse(pp, v[i], args)
                i = i + 1
            return ()
        if p.key == TUPLE_PREFIX:
            if not sequenceish(v): raise SchemaDecodeFailed(cls, p, v)
            if len(v) < len(p[0]): raise SchemaDecodeFailed(cls, p, v)
            i = 0
            for pp in p[0]:
                cls.parse(pp, v[i], args)
                i = i + 1
            cls.parse(p[1], v[i:], args)
            return ()
        if p.key == DICT:
            if not isinstance(v, dict): raise SchemaDecodeFailed(cls, p, v)
            if len(v) < len(p[0]): raise SchemaDecodeFailed(cls, p, v)
            for (k, pp) in compare.sorted_items(p[0]):
                if k not in v: raise SchemaDecodeFailed(cls, p, v)
                cls.parse(pp, v[k], args)
            return ()
        if p.key == AND:
            for pp in p[0]:
                cls.parse(pp, v, args)
            return ()
        raise ValueError(f'Bad schema {p}')

    def __preserve__(self):
        raise NotImplementedError('Subclass responsibility')

    def __repr__(self):
        n = self._constructor_name()
        if self.SIMPLE:
            if self.EMPTY:
                return n + '()'
            else:
                return n + '(' + repr(self.value) + ')'
        else:
            return n + ' ' + repr(self._as_dict())

    def _as_dict(self):
        raise NotImplementedError('Subclass responsibility')

class Enumeration(SchemaObject):
    VARIANTS = None

    def __init__(self):
        raise TypeError('Cannot create instance of Enumeration')

    @classmethod
    def _set_schema(cls, rootns, module_path, name, schema, _variant, _enumeration):
        cls.ROOTNS = rootns
        cls.SCHEMA = schema
        cls.MODULE_PATH = module_path
        cls.NAME = name
        cls.VARIANTS = []
        cls._ALL = pretty_subclass(Definition, module_path_str(module_path + (name,)), '_ALL')
        for (n, d) in schema[0]:
            n = Symbol(n)
            c = pretty_subclass(cls._ALL, module_path_str(module_path + (name,)), n.name)
            c._set_schema(rootns, module_path, name, d, n, cls)
            cls.VARIANTS.append((n, c))
            safesetattr(cls, n.name, c)

    @classmethod
    def decode(cls, v):
        failures = None
        for (n, c) in cls.VARIANTS:
            try:
                return c.decode(v)
            except SchemaDecodeFailed as failure:
                if failures is None: failures = []
                failures.append(failure)
        raise SchemaDecodeFailed(cls, None, v, failures)

    def __preserve__(self):
        raise TypeError('Cannot encode instance of Enumeration')

def safeattrname(k):
    return k + '_' if keyword.iskeyword(k) else k

def safesetattr(o, k, v):
    setattr(o, safeattrname(k), v)

def safegetattr(o, k):
    return getattr(o, safeattrname(k))

def safehasattr(o, k):
    return hasattr(o, safeattrname(k))

class Definition(SchemaObject):
    EMPTY = False
    SIMPLE = False
    FIELD_NAMES = []
    SAFE_FIELD_NAMES = []
    ENUMERATION = None

    def _constructor_name(self):
        if self.VARIANT is None:
            return self.NAME.name
        else:
            return self.NAME.name + '.' + self.VARIANT.name

    def __init__(self, *args, **kwargs):
        self._fields = args
        if self.SIMPLE:
            if self.EMPTY:
                if len(args) != 0:
                    raise TypeError('%s takes no arguments' % (self._constructor_name(),))
            else:
                if len(args) != 1:
                    raise TypeError('%s needs exactly one argument' % (self._constructor_name(),))
                self.value = args[0]
        else:
            i = 0
            for arg in args:
                if i >= len(self.FIELD_NAMES):
                    raise TypeError('%s given too many positional arguments' % (self._constructor_name(),))
                setattr(self, self.SAFE_FIELD_NAMES[i], arg)
                i = i + 1
            for (argname, arg) in kwargs.items():
                if hasattr(self, argname):
                    raise TypeError('%s given duplicate attribute: %r' % (self._constructor_name, argname))
                if argname not in self.SAFE_FIELD_NAMES:
                    raise TypeError('%s given unknown attribute: %r' % (self._constructor_name, argname))
                setattr(self, argname, arg)
                i = i + 1
            if i != len(self.FIELD_NAMES):
                raise TypeError('%s needs argument(s) %r' % (self._constructor_name(), self.FIELD_NAMES))

    def __eq__(self, other):
        return (other.__class__ is self.__class__) and (self._fields == other._fields)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self._fields) ^ hash(self.__class__)

    def _accept(self, visitor):
        if self.VARIANT is None:
            return visitor(*self._fields)
        else:
            return visitor[self.VARIANT.name](*self._fields)

    @classmethod
    def _set_schema(cls, rootns, module_path, name, schema, variant, enumeration):
        cls.ROOTNS = rootns
        cls.SCHEMA = schema
        cls.MODULE_PATH = module_path
        cls.NAME = name
        cls.EMPTY = is_empty_pattern(schema)
        cls.SIMPLE = is_simple_pattern(schema)
        cls.FIELD_NAMES = []
        cls.VARIANT = variant
        cls.ENUMERATION = enumeration
        gather_defined_field_names(schema, cls.FIELD_NAMES)
        cls.SAFE_FIELD_NAMES = [safeattrname(n) for n in cls.FIELD_NAMES]

    @classmethod
    def decode(cls, v):
        if cls.SIMPLE:
            i = cls.parse(cls.SCHEMA, v, [])
            if cls.EMPTY:
                return cls()
            else:
                return cls(i)
        else:
            args = []
            cls.parse(cls.SCHEMA, v, args)
            return cls(*args)

    def __preserve__(self):
        if self.SIMPLE:
            if self.EMPTY:
                return encode(self.SCHEMA, ())
            else:
                return encode(self.SCHEMA, self.value)
        else:
            return encode(self.SCHEMA, self)

    def _as_dict(self):
        return dict((k, safegetattr(self, k)) for k in self.FIELD_NAMES)

    def __getitem__(self, name):
        return safegetattr(self, name)

    def __setitem__(self, name, value):
        return safesetattr(self, name, value)

class escape:
    def __init__(self, escaped):
        self.escaped = escaped
    def __escape_schema__(self):
        return self.escaped

def encode(p, v):
    if hasattr(v, '__escape_schema__'):
        return preserve(v.__escape_schema__())
    if p == ANY:
        return v
    if p.key == NAMED:
        return encode(p[1], safegetattr(v, p[0].name))
    if p.key == ATOM:
        return v
    if p.key == EMBEDDED:
        return Embedded(v)
    if p.key == LIT:
        return p[0]
    if p.key == SEQOF:
        return tuple(encode(p[0], w) for w in v)
    if p.key == SETOF:
        return set(encode(p[0], w) for w in v)
    if p.key == DICTOF:
        return dict((encode(p[0], k), encode(p[1], w)) for (k, w) in v.items())
    if p.key == REF:
        return preserve(v)
    if p.key == REC:
        return Record(encode(p[0], v), encode(p[1], v))
    if p.key == TUPLE:
        return tuple(encode(pp, v) for pp in p[0])
    if p.key == TUPLE_PREFIX:
        return tuple(encode(pp, v) for pp in p[0]) + encode(p[1], v)
    if p.key == DICT:
        return dict((k, encode(pp, v)) for (k, pp) in p[0].items())
    if p.key == AND:
        return merge(*[encode(pp, v) for pp in p[0]])
    raise ValueError(f'Bad schema {p}')

def module_path_str(mp):
    return '.'.join([e.name for e in mp])

SIMPLE_PATTERN_KEYS = [ATOM, EMBEDDED, LIT, SEQOF, SETOF, DICTOF, REF]
def is_simple_pattern(p):
    return p == ANY or (isinstance(p, Record) and p.key in SIMPLE_PATTERN_KEYS)

def is_empty_pattern(p):
    return isinstance(p, Record) and p.key == LIT

def gather_defined_field_names(s, acc):
    if is_simple_pattern(s):
        pass
    elif sequenceish(s):
        for p in s:
            gather_defined_field_names(p, acc)
    elif s.key == NAMED:
        acc.append(s[0].name)
        gather_defined_field_names(s[1], acc)
    elif s.key == AND:
        gather_defined_field_names(s[0], acc)
    elif s.key == REC:
        gather_defined_field_names(s[0], acc)
        gather_defined_field_names(s[1], acc)
    elif s.key == TUPLE:
        gather_defined_field_names(s[0], acc)
    elif s.key == TUPLE_PREFIX:
        gather_defined_field_names(s[0], acc)
        gather_defined_field_names(s[1], acc)
    elif s.key == DICT:
        gather_defined_field_names(tuple(item[1] for item in compare.sorted_items(s[0])), acc)
    else:
        raise ValueError('Bad schema')

def pretty_subclass(C, module_name, class_name):
    class S(C): pass
    S.__module__ = module_name
    S.__name__ = class_name
    S.__qualname__ = class_name
    return S

def lookup(ns, module_path, name):
    for e in module_path:
        if e not in ns:
            definition_not_found(module_path, name)
        ns = ns[e]
    if name not in ns:
        definition_not_found(module_path, name)
    return ns[name]

def definition_not_found(module_path, name):
    raise KeyError('Definition not found: ' + module_path_str(module_path + (name,)))

class Namespace:
    def __init__(self, prefix):
        self._prefix = prefix

    def __getitem__(self, name):
        return safegetattr(self, Symbol(name).name)

    def __setitem__(self, name, value):
        name = Symbol(name).name
        if name in self.__dict__:
            raise ValueError('Name conflict: ' + module_path_str(self._prefix + (name,)))
        safesetattr(self, name, value)

    def __contains__(self, name):
        return safeattrname(Symbol(name).name) in self.__dict__

    def _items(self):
        return dict((k, v) for (k, v) in self.__dict__.items() if k[0] != '_')

    def __repr__(self):
        return repr(self._items())

class Compiler:
    def __init__(self):
        self.root = Namespace(())

    def load(self, filename):
        filename = pathlib.Path(filename)
        with open(filename, 'rb') as f:
            x = Decoder(f.read()).next()
            if x.key == SCHEMA:
                self.load_schema((Symbol(filename.stem),), x)
            elif x.key == BUNDLE:
                for (p, s) in x[0].items():
                    self.load_schema(p, s)

    def load_schema(self, module_path, schema):
        if schema[0][VERSION] != 1:
            raise NotImplementedError('Unsupported Schema version')
        ns = self.root
        for e in module_path:
            if not e in ns:
                ns[e] = Namespace(ns._prefix + (e,))
            ns = ns[e]
        for (n, d) in schema[0][DEFINITIONS].items():
            if isinstance(d, Record) and d.key == OR:
                superclass = Enumeration
            else:
                superclass = Definition
            c = pretty_subclass(superclass, module_path_str(module_path), n.name)
            c._set_schema(self.root, module_path, n, d, None, None)
            ns[n] = c

def load_schema_file(filename):
    c = Compiler()
    c.load(filename)
    return c.root

# a decorator
def extend(cls):
    def extender(f):
        setattr(cls, f.__name__, f)
        return f
    return extender

__metaschema_filename = pathlib.Path(__file__).parent / 'schema.prb'
meta = load_schema_file(__metaschema_filename).schema

if __name__ == '__main__':
    with open(__metaschema_filename, 'rb') as f:
        x = Decoder(f.read()).next()
    print(meta.Schema.decode(x))
    print(preserve(meta.Schema.decode(x)))
    assert preserve(meta.Schema.decode(x)) == x

    @extend(meta.Schema)
    def f(self, x):
        return ['yay', self.embeddedType, x]
    print(meta.Schema.decode(x).f(123))
    print(f)

    print()

    path_bin_filename = pathlib.Path(__file__).parent / 'path.prb'
    path = load_schema_file(path_bin_filename).path
    with open(path_bin_filename, 'rb') as f:
        x = Decoder(f.read()).next()
    print(meta.Schema.decode(x))
    assert meta.Schema.decode(x) == meta.Schema.decode(x)
    assert preserve(meta.Schema.decode(x)) == x

    print()
    print(path)
