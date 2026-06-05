# Implementation Notes

## Parsing

The parser recognizes struct declarations with:

* `struct Name { ... }`
* optional generic type parameters
* field declarations
* optional public fields

It also recognizes struct initialization and struct patterns in expression and pattern position.

## Semantic analysis

The semantic analyzer stores struct declarations, tracks their methods, and records whether a type implements an interface.

It also preserves type parameters and uses named struct types during type resolution.

## Lowering

Struct values are lowered to concrete layouts with field offsets and total size.

The backend computes:

* field offsets
* field sizes
* total struct size
* alignment
