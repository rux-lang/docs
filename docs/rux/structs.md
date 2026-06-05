# Structs

Structs define user-owned composite types made from named fields.

A struct groups related values together into a single record-like type with a fixed field order and a compiler-defined memory layout.

Structs are one of the core data types in Rux and are used for everything from small value objects to low-level runtime structures.

---

## Summary

```rux
struct Point {
    x: float64;
    y: float64;
}

let p = Point { x: 1.0, y: 2.0 };

let x = p.x;
```

Struct-related syntax includes:

* struct declarations
* public fields
* generic struct parameters
* struct construction
* field access
* struct patterns
* methods via `extend`

---

## Struct Declarations

A struct is declared with the `struct` keyword.

```rux
struct Point {
    x: float64;
    y: float64;
}
```

Each field has:

* a name
* a type
* an optional `pub` modifier

### Example

```rux
struct Person {
    pub name: char8[];
    age: uint32;
}
```

### Notes

* Fields are written in declaration order.
* Each field ends with a semicolon.
* Struct declarations may appear at module level or inside nested modules.

---

## Generic Structs

Structs may declare type parameters.

```rux
struct Box<T> {
    value: T;
}
```

Type parameters are parsed, preserved through semantic analysis, and carried into lowering.

### Example

```rux
struct Pair<T, U> {
    first: T;
    second: U;
}
```


### Construction with type arguments

```rux
let p = Pair<int32, float64> { first: 1, second: 2.5 };
```

### Notes

* Generic type arguments appear in angle brackets.
* The compiler preserves generic type information in the type system and lowering layers.
* Backend code generation for generics is a separate concern from parsing and semantic tracking.
* Generics are **not** yet implemented in the backend.

---

## Field Rules

A struct field is declared as:

```rux
name: Type;
```

Example:

```rux
struct Size {
    width: uint32;
    height: uint32;
}
```

### Public fields

A field may be marked public:

```rux
struct Token {
    pub kind: uint32;
    value: char8[];
}
```

Public fields are intended to be visible outside the defining module or package according to the language’s visibility rules.

### Notes

* Field names must be identifiers.
* Field types may be any valid Rux type.
* Fields cannot currently be declared without a type.

---

## Struct Construction

A struct value can be constructed using brace syntax.

```rux
let p = Point { x: 1.0, y: 2.0 };
```

### Explicit construction

```rux
let person = Person {
    name: "Alice",
    age: 30
};
```

### Notes

* Field names are written explicitly in the initializer.
* The initializer order does not need to match the declaration order unless the compiler or front end enforces an order rule.
* The parser supports generic struct initialization syntax.

### Example with generics

```rux
let box = Box<int32> { value: 42 };
```

---

## Field Access

Fields are accessed using the `.` operator.

```rux
let p = Point { x: 1.0, y: 2.0 };
let x = p.x;
```

Example:

```rux
Print(person.name);
```

Field access is a normal postfix expression and participates in later semantic checks and lowering.

---

## Struct Patterns

Structs can be destructured in pattern position.

```rux
let Point { x, y } = p;
```

Or with explicit field patterns:

```rux
let Point { x: px, y: py } = p;
```

Struct patterns are used in bindings and match arms.

### Example in a `match`

```rux
match value {
    Point { x: 0, y } => Print(y),
    _ => Print(0)
}
```

### Notes

* Struct patterns must match the struct type shape.
* Field patterns are parsed separately from struct expressions.
* Pattern syntax is part of the parser’s supported feature set, not an afterthought.

---

## Methods and `extend`

Methods can be attached to structs with `extend`.

```rux
struct Vector {
    x: float64;
    y: float64;
    z: float64;
}

extend Vector {
    func Length(self) -> float64 {
        return Sqrt(self.x * self.x + self.y * self.y + self.z * self.z);
    }
}
```

### Instance methods

Instance methods take `self` as their first parameter.

```rux
func Length(self) -> float64 {
    return Sqrt(self.x * self.x + self.y * self.y + self.z * self.z);
}
```

### Static methods

A method without `self` behaves like an associated function.

```rux
extend Vector {
    func New(x: float64, y: float64, z: float64) -> Vector {
        return Vector { x: x, y: y, z: z };
    }
}
```

Called as:

```rux
let v = Vector::New(1.0, 2.0, 3.0);
```

### Operator methods

A struct may define operator methods inside `extend`.

```rux
extend Vector {
    func +(self, other: Vector) -> Vector {
        return Vector {
            x: self.x + other.x,
            y: self.y + other.y,
            z: self.z + other.z
        };
    }
}
```

These are resolved by the compiler like ordinary methods, but using operator syntax.

---

## Interface Implementations

The parser supports `extend` in interface-related forms as well.

```rux
extend Vector : Display {
    func ToString(self) -> String {
        return "Vector";
    }
}
```

or:

```rux
extend Display for Vector {
    func ToString(self) -> String {
        return "Vector";
    }
}
```

This allows a struct to implement an interface by attaching the required methods.

### Notes

* The compiler tracks methods by type.
* Interface implementation is associated with the concrete type name.
* Interface method tables are used later during lowering and backend generation.

---

## Visibility

Structs may be public.

```rux
pub struct Point {
    pub x: float64;
    pub y: float64;
}
```

### Notes

* Public visibility can apply to the struct itself.
* Public visibility can also apply to individual fields.
* Visibility is tracked by the parser and semantic analyzer.

---

## Memory Layout

Struct layout is determined by the compiler.

The current layout model preserves field order and computes offsets using alignment rules.

### General rules

* Fields are laid out in declaration order.
* Each field is aligned based on its size.
* The overall struct size is padded up to the maximum alignment.
* Alignment is capped at 8 bytes in the current layout model.

### Example

```rux
struct Point {
    x: float64;
    y: float64;
}
```

A typical layout for this struct is:

| Field | Offset | Size |
| ----- | -----: | ---: |
| x     |      0 |    8 |
| y     |      8 |    8 |

Total size:

```text
16 bytes
```

### Another example

```rux
struct Mixed {
    a: uint8;
    b: uint32;
}
```

A typical layout is:

| Field | Offset | Size |
| ----- | -----: | ---: |
| a     |      0 |    1 |
| b     |      4 |    4 |

The compiler inserts padding between fields when required to satisfy alignment.

### Notes

* Field offsets are compiler-defined, not arbitrary.
* Field order is preserved.
* Layout depends on the field types and their sizes.
* Named fields that themselves resolve to structured types may contribute their own layout and alignment.

---

## Size Rules

The compiler’s size model is used by semantic analysis, lowering, and backend code generation.

### Primitive field sizes

Common field sizes are:

* `bool8`, `char8`, `int8`, `uint8` → 1 byte
* `bool16`, `char16`, `int16`, `uint16` → 2 bytes
* `bool32`, `char32`, `int32`, `uint32`, `float32` → 4 bytes
* `int64`, `uint64`, `int`, `uint`, `float64`, pointers, `String`, function values → 8 bytes
* slices → 16 bytes
* `opaque` → 0 bytes

### Struct size computation

For each field:

1. determine the field’s size
2. compute alignment as the field size clamped to 8 bytes
3. align the current offset
4. place the field
5. advance the offset by the field size

After all fields are placed, the total size is aligned to the maximum field alignment.

### Example

```rux
struct Small {
    a: uint8;
    b: uint8;
    c: uint8;
}
```

Total size is typically 3 bytes, then rounded up to the struct alignment boundary.

### Nested structs

Nested structs contribute their own size and alignment.

```rux
struct Outer {
    inner: Point;
    tag: uint8;
}
```

The compiler uses the known layout of `Point` when computing the layout of `Outer`.

---

## Nested Structs and Named Types

Struct fields may themselves be named types.

```rux
struct Address {
    city: char8[];
    zip: uint32;
}

struct Person {
    name: char8[];
    address: Address;
}
```

The compiler resolves the named field type during semantic analysis and uses the resolved type during layout computation.

### Notes

* Named fields are not flattened automatically.
* The struct contains the nested type as a field.
* Layout is computed recursively through known named types.

---

## Examples

### Simple struct

```rux
struct Point {
    x: float64;
    y: float64;
}
```

### Struct with visibility

```rux
pub struct Config {
    pub enabled: bool;
    pub port: uint32;
}
```

### Generic struct

```rux
struct Box<T> {
    value: T;
}
```

### Nested struct

```rux
struct Rectangle {
    topLeft: Point;
    bottomRight: Point;
}
```

### Struct construction

```rux
let p = Point { x: 1.0, y: 2.0 };
```

### Struct pattern

```rux
let Point { x, y } = p;
```

### Method implementation

```rux
extend Point {
    func Length(self) -> float64 {
        return Sqrt(self.x * self.x + self.y * self.y);
    }
}
```

---

## Common Errors

### Missing field type

```rux
struct Bad {
    x;
}
```

### Missing semicolon after a field

```rux
struct Bad {
    x: int32
}
```

### Invalid construction field

```rux
let p = Point { a: 1.0, y: 2.0 };
```

### Duplicate field names

```rux
struct Bad {
    x: int32;
    x: int32;
}
```

### Pattern mismatch

```rux
let Point { x, y, z } = p;
```

when `Point` does not have a `z` field.

---

## Implementation Notes

### Parsing

The parser recognizes struct declarations with:

* `struct Name { ... }`
* optional generic type parameters
* field declarations
* optional public fields

It also recognizes struct initialization and struct patterns in expression and pattern position.

### Semantic analysis

The semantic analyzer stores struct declarations, tracks their methods, and records whether a type implements an interface.

It also preserves type parameters and uses named struct types during type resolution.

### Lowering

Struct values are lowered to concrete layouts with field offsets and total size.

The backend computes:

* field offsets
* field sizes
* total struct size
* alignment
