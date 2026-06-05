# Enums

Enums define a closed set of named variants for a single type.

An enum is useful when a value can be one of several shapes, but the shapes are still part of the same conceptual type.

In Rux, enums can be:

* unit variants with no payload
* tuple-like variants with ordered payload fields
* named-field variants with explicit field names
* optionally assigned an explicit integer discriminant
* optionally marked `pub`

Enums are one of the most important types in the language because they bridge the gap between simple tag values and structured variant data.

---

## Summary

```rux
enum Status {
    Ok,
    NotFound = 404,
    Failed = 500,
}

enum Message: uint8 {
    Ping,
    Data(char8[]),
    Named {
        kind: uint32;
        value: uint64;
    },
}
```

An enum declaration may include:

* an optional `pub` modifier
* a name
* an optional integer base type
* a comma-separated list of variants
* tuple-like payloads in parentheses
* named-field payloads in braces
* an optional discriminant on each variant

---

## What an Enum Means

An enum says that a value belongs to exactly one of a fixed set of alternatives.

That is different from a struct, where all fields exist together.
It is also different from a union, where fields share storage but the language does not automatically name the active variant for you.

### Good practice

Use an enum when the alternatives have clear names and the active case matters.

```rux
enum Result {
    Ok,
    Err,
}
```

### Bad practice

Do not use an enum just to avoid writing a normal structured type.

```rux
// bad idea: this is trying to smuggle a record into a variant list
enum UserLike {
    Person {
        name: char8[];
        age: uint32;
    },
    Company {
        name: char8[];
        employees: uint32;
    },
}
```

That may be valid, but it only makes sense when the program truly has mutually exclusive shapes.

---

## Enum Declaration Syntax

The general shape of an enum is:

```rux
enum Name [: BaseType] {
    Variant,
    Variant = 123,
    Variant(Type, Type),
    Variant {
        field: Type;
    },
}
```

### Example

```rux
enum Color {
    Red,
    Green,
    Blue,
}
```

### Public enums

A type may be marked `pub`.

```rux
pub enum TokenKind {
    Ident,
    Number,
    String,
}
```

Public visibility controls whether the enum is visible outside the defining scope, using the same visibility rules as the rest of the language.

### Notes

* The parser recognizes `enum` declarations at top level.
* Variants are separated by commas.
* A trailing comma before `}` is rejected.
* Enum fields inside payload variants use their own syntax rules.

---

## Base Types

An enum may optionally specify an integer base type after a colon.

```rux
enum Code: uint8 {
    A = 1,
    B = 2,
}
```

The base type is the type of the enum discriminant tag.

### Default base type

If no base type is written, the compiler uses `int`.

```rux
enum Plain {
    A,
    B,
}
```

On the current target model, `int` is 8 bytes.

### Allowed base types

The semantic analyzer requires the base type to be an integer type.

That means things like `uint8`, `uint16`, `uint32`, `uint64`, `int8`, `int16`, `int32`, `int64`, `int`, and `uint` are valid base types, while floats and pointers are not.

### Good practice

Choose the base type deliberately when the enum must match a file format, ABI, or network protocol.

```rux
enum PacketType: uint8 {
    Ping = 1,
    Pong = 2,
    Data = 3,
}
```

### Bad practice

Do not rely on the default base type when the numeric size matters outside the compiler.

```rux
// bad idea if this crosses an ABI boundary
enum WireCode {
    A,
    B,
    C,
}
```

That version is readable, but the exact storage width is not as explicit.

---

## Variants

Each variant names one possible case of the enum.

### Unit variants

A unit variant has no payload.

```rux
enum State {
    Idle,
    Busy,
    Stopped,
}
```

Unit variants are the cleanest form of enum variant.

### Tuple-like variants

A variant may hold ordered payload fields.

```rux
enum Response {
    Ok(uint32),
    Err(char8[]),
}
```

The fields are positional, so the order matters.

### Named-field variants

A variant may hold named fields.

```rux
enum Message {
    Move {
        x: int32;
        y: int32;
    },
    Color {
        r: uint8;
        g: uint8;
        b: uint8;
    },
}
```

Named-field variants behave like structured payloads.

### Good practice

Use tuple-style payloads when the meaning is naturally positional.

```rux
enum Vec2State {
    Point(float32, float32),
}
```

Use named fields when the payload carries semantically distinct values.

```rux
enum Vec2State {
    Point {
        x: float32;
        y: float32;
    },
}
```

### Bad practice

Do not use named fields when the names add no information.

```rux
enum Bad {
    Pair {
        a: int32;
        b: int32;
    },
}
```

That is not wrong, but it often reads like noise unless `a` and `b` actually mean something.

---

## Discriminants

A variant may be given an explicit integer discriminant.

```rux
enum HttpStatus: uint16 {
    Ok = 200,
    NotFound = 404,
    InternalError = 500,
}
```

The discriminant is the numeric value associated with that variant.

### Automatic numbering

If a variant does not specify a discriminant, the compiler assigns one automatically.

The first unit is `0`, and each later unit increments from the previous value unless overridden.

```rux
enum Mode {
    Off,      // 0
    On,       // 1
    Sleep = 8,
    Deep,     // 9
}
```

### Literal forms

The parser and semantic layer accept integer literal text in a few common forms, including:

* decimal
* hexadecimal
* binary
* octal
* negative values

### Good practice

Use explicit discriminants for stable public APIs, binary formats, and protocol definitions.

```rux
enum Opcode: uint8 {
    Read = 1,
    Write = 2,
    Close = 3,
}
```

### Bad practice

Do not depend on auto-incremented values if the numbers are part of an external contract.

```rux
// bad idea for wire formats
enum Opcode {
    Read,
    Write,
    Close,
}
```

That looks fine in source code, but the numeric meanings can become a maintenance trap if the declaration changes later.

---

## Declaration Rules

### Variant list separators

Variants are separated by commas.

```rux
enum Status {
    Ok,
    Err,
}
```

A trailing comma before the closing brace is rejected.

### Payload and discriminant cannot mix

A variant cannot have both payload fields and an explicit discriminant when the parser and semantic checks expect them to remain separate in that form.

### Named payload validation

Named-field variants validate their own field list.

Duplicate field names are rejected, and every field type must resolve correctly.

---

## Layout and Size

Enums are sized using the base type plus the largest payload layout among all variants that carry data.

That means the compiler does not treat every enum as a magic black box. It computes a real layout model.

### Base storage

The tag width comes from the enum base type.

Examples:

* `uint8` → 1 byte
* `uint16` → 2 bytes
* `uint32` → 4 bytes
* `uint64` → 8 bytes
* `int` → 8 bytes on the current target model

### Payload storage

For payload variants, the compiler computes the payload layout using the same kind of field-layout rules used for structured data:

* fields are placed in order
* each field is aligned by its size, capped at 8 bytes
* padding may be inserted between fields
* the resulting payload layout is rounded up to the payload alignment

### Size formula

The current enum size model works like this:

1. compute the tag size from the base type
2. compute each payload variant size and alignment
3. take the largest payload size and alignment
4. place the payload after the tag with alignment padding if needed
5. round the whole enum up to the final alignment

In shorthand:

```text
size = align_up(
    align_up(tagSize, payloadAlign) + payloadSize,
    max(tagAlign, payloadAlign)
)
```

If the enum has no payload variants, the total size is just the tag size.

### Example: unit enum

```rux
enum State: uint8 {
    Idle,
    Busy,
    Stopped,
}
```

Typical size:

* tag = 1 byte
* payload = none
* total = 1 byte

### Example: small payload enum

```rux
enum MaybeInt: uint8 {
    None,
    Some(int32),
}
```

Typical size:

* tag = 1 byte
* payload = 4 bytes
* payload alignment = 4 bytes
* total = 8 bytes after padding

That extra padding is not wasted in the compiler’s model; it is there so the payload stays aligned.

### Example: named-field payload enum

```rux
enum Command: uint16 {
    Move {
        x: int32;
        y: int32;
    },
}
```

Typical layout reasoning:

* tag = 2 bytes
* payload fields are laid out like a struct
* padding may be inserted after the tag and between payload fields
* total size is aligned to the final enum alignment

### Good practice

Keep payload variants reasonably small when the enum is used heavily.

```rux
enum TokenValue: uint8 {
    KindA,
    KindB(uint32),
}
```

### Bad practice

Do not assume the enum is always a tiny tag just because the syntax looks compact.

```rux
enum BigThing {
    Small,
    Huge(SomeLargeStruct),
}
```

A payload variant can make the overall enum much larger than a plain tag.

---

## Bits, Bytes, and Discriminants

The discriminant is the numeric identity of the current variant.

The compiler stores and reasons about discriminants as integer values, and the base type determines their width.

### Bit-width examples

* `uint8` tag → 8 bits
* `uint16` tag → 16 bits
* `uint32` tag → 32 bits
* `uint64` or `int` tag → 64 bits on the current target model

### Why this matters

Bit-width affects:

* size on disk or in memory
* ABI compatibility
* how much padding is needed
* whether a variant value fits a chosen base type

### Good practice

Use the smallest tag width that can safely represent all variants.

```rux
enum SmallCode: uint8 {
    A = 1,
    B = 2,
    C = 3,
}
```

### Bad practice

Do not use a huge tag type if the values are tiny and stable.

```rux
enum SmallCode: uint64 {
    A = 1,
    B = 2,
    C = 3,
}
```

That works, but it is bloated for no benefit.

---

## Construction

Enum construction depends on the variant shape.

### Unit variants

Unit variants behave like simple values.

```rux
let s = State::Idle;
```

### Tuple-like variants

Tuple-like variants are constructed with positional arguments.

```rux
let r = Response::Ok(123);
```

### Named-field variants

Named-field variants are constructed with brace syntax.

```rux
let m = Message::Move {
    x: 10,
    y: 20,
};
```

### Notes

* Unit variants do not need payload syntax.
* Payload variants must supply the payload shape expected by the variant.
* Named-field variants must provide the required named fields.

### Good practice

Match the construction form to the variant form.

```rux
enum Event {
    Tick,
    Move { x: int32; y: int32; },
    Data(uint32),
}
```

```rux
let a = Event::Tick;
let b = Event::Move { x: 1, y: 2 };
let c = Event::Data(42);
```

### Bad practice

Do not mix construction styles randomly.

```rux
let bad = Event::Move(1, 2);
```

If the variant is named-field based, the brace form is the one that communicates intent best.

---

## Pattern Matching

Enums are intended to work naturally with `match`.

```rux
match value {
    State::Idle => 0,
    State::Busy => 1,
    _ => 2,
}
```

Payload variants can bind payload data in patterns.

```rux
match value {
    Response::Ok(code) => Print(code),
    Response::Err(msg) => Print(msg),
    _ => Print("unknown"),
}
```

Named-field variants can bind fields by name.

```rux
match value {
    Message::Move { x, y } => Print(x + y),
    _ => Print(0),
}
```

### Good practice

Prefer exhaustive matches when the set of variants is small and stable.

```rux
match state {
    State::Idle => ...,
    State::Busy => ...,
    State::Stopped => ...,
}
```

### Bad practice

Do not rely on a default arm to hide missing cases if the enum is central to the logic.

```rux
match state {
    _ => ...,
}
```

That is legal in many contexts, but it can make the code less explicit than it should be.

---

## Examples

### Simple enum

```rux
enum Color {
    Red,
    Green,
    Blue,
}
```

### Enum with explicit base type

```rux
enum Opcode: uint8 {
    Read = 1,
    Write = 2,
    Close = 3,
}
```

### Enum with tuple payloads

```rux
enum Response {
    Ok(uint32),
    Err(char8[]),
}
```

### Enum with named-field payloads

```rux
enum Command {
    Move {
        x: int32;
        y: int32;
    },
    Stop,
}
```

### Public enum

```rux
pub enum TokenKind {
    Ident,
    Number,
    String,
}
```

---

## Common Errors

### Missing variant name

```rux
enum Bad {
    ,
}
```

### Duplicate variant names

```rux
enum Bad {
    A,
    A,
}
```

### Invalid base type

```rux
enum Bad: float32 {
    A,
}
```

### Duplicate named field in a variant

```rux
enum Bad {
    Move {
        x: int32;
        x: int32;
    },
}
```

### Mixing payload and discriminant incorrectly

```rux
enum Bad {
    Item(123) = 1,
}
```

### Missing field in a named variant construction

```rux
enum Command {
    Move {
        x: int32;
        y: int32;
    },
}

let c = Command::Move { x: 1 };
```

### Unknown field in a named variant construction

```rux
let c = Command::Move { x: 1, z: 2 };
```

---

## Notes

### Enum values are tagged values

An enum value is identified by its tag, and payload variants carry extra data alongside that tag.

### The size model is real

The compiler computes enum size using tag size, payload size, and alignment.

That matters for stack allocation, ABI decisions, and lowering.

### Explicit discriminants are the stable option

If a number must never silently change, write the number yourself.

### Keep payloads intentional

Payload variants are powerful, but they also make the enum larger and more complex.

### No generic enums in the reviewed parser

The reviewed parser shows `enum Name ...`, not a generic `enum Name<T> ...` form.

---

## Implementation Notes

This section describes how the compiler currently handles enums internally.

### Parsing

The parser recognizes:

* `enum Name { ... }`
* optional `: BaseType`
* unit variants
* tuple-like variants
* named-field variants
* optional `= discriminant`
* comma-separated variants

### Semantic analysis

The semantic analyzer checks:

* the base type is an integer type
* variant names are unique
* named-field names are unique inside each variant
* payload fields resolve correctly
* a variant does not mix incompatible forms in the checked representation
