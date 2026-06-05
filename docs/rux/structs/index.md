# Structs

Structs define user-owned composite types made from named fields.

A struct groups related values together into a single record-like type with a fixed field order and a compiler-defined memory layout.

Structs are one of the core data types in Rux and are used for everything from small value objects to low-level runtime structures.

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
* methods via `extend`.
