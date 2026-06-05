# Memory

## Layout

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

The compiler uses the known layout of `Point` when computing the layout of `Outer`
