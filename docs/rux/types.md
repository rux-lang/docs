# Types

Types describe the shape, size, and compatibility of values in Rux.

Rux has a small set of built-in primitive types and a set of compound type forms built from them.

The compiler tracks types through parsing, semantic analysis, HIR, and lowering, so the same type concept usually appears in more than one stage of compilation.

---

## Summary

```rux
let a: int32 = 42;
let b: float64 = 3.14;
let c: bool = true;
let d: *int32 = null;
let e: int32[] = [1, 2, 3];
let f: (int32, float64) = (1, 2.5);
```

Rux supports:

* primitive scalar types
* pointer types
* slice types
* tuple types
* range types
* function types
* named types
* type parameters
* type aliases

---

## Built-in Primitive Types

Rux includes several built-in primitive types.

### Boolean types

```rux
bool8
bool16
bool32
bool
```

`bool` is an alias for `bool8`.

The compiler treats all boolean widths as mutually assignable across the boolean family.

### Character types

```rux
char8
char16
char32
char
```

`char` is an alias for `char32`.

Character literals can also be prefixed to select a character width.

### Signed integer types

```rux
int8
int16
int32
int64
int
```

`int` is a platform-width integer type.

On 64-bit targets, it behaves like a 64-bit signed integer.

### Unsigned integer types

```rux
uint8
uint16
uint32
uint64
uint
```

`uint` is a platform-width unsigned integer type.

On 64-bit targets, it behaves like a 64-bit unsigned integer.

### Floating-point types

```rux
float32
float64
float
```

`float` is an alias for `float64`.

### Opaque type

```rux
opaque
```

`opaque` represents an untyped, zero-sized, or intentionally uninterpreted value category in the compiler’s type system.

It is commonly used for raw FFI handles and pointer-like interoperability.

---

## Type Aliases

Rux supports type aliases.

```rux
type Bytes = uint8[];
type Count = uint;
```

A type alias gives another name to an existing type.

Aliases are resolved during semantic analysis, but they remain meaningful in documentation and code structure.

---

## Named Types

A named type is a user-defined type name such as a struct, enum, union, interface, or alias target.

```rux
struct Point {
    x: float64;
    y: float64;
}

let p: Point = Point { x: 1.0, y: 2.0 };
```

Named types are the normal way to refer to user-defined data structures.

They also appear in generic instantiations such as:

```rux
Box<int32>
```

---

## Pointer Types

Pointer types use the `*` prefix.

```rux
*int32
*opaque
*const int32
```

Pointers reference memory locations rather than values directly.

### Examples

```rux
let ptr: *int32 = null;
let raw: *opaque = ptr;
```

### Notes

* `*const T` is a const-qualified pointer form.
* `*opaque` is the most permissive pointer-like form in the type system.
* Any pointer is implicitly assignable to `*opaque`.

This is the closest equivalent to a `void*` style pointer in C.

---

## Slice Types

Slices use the `[]` suffix.

```rux
int32[]
char8[]
Point[]
```

Slices represent a sequence of elements.

They are used heavily for arrays, string-like data, and variable-length collections.

### Example

```rux
let values: int32[] = [1, 2, 3];
```

### Runtime shape

Slices are represented as a pair of values:

* data pointer
* length

That is why slice-like values occupy 16 bytes in the lowering pipeline.

---

## Tuple Types

Tuples use parentheses.

```rux
(int32, float64)
(bool, char8, uint32)
```

Tuples group values of possibly different types into one composite value.

### Example

```rux
let pair: (int32, int32) = (10, 20);
```

### Notes

* Tuple elements are ordered.
* Tuple field access may use numeric field names like `0`, `1`, `2` in compiler internals.
* Tuple size is the sum of element sizes in the current size model.

---

## Range Types

Ranges model a lower bound, upper bound, and inclusive/exclusive behavior.

The compiler recognizes range syntax in type positions and carries range types through the type system.

### Example

```rux
let r: Range<int32> = 0..10;
let r2: Range<int32> = 0...10;
```

### Notes

* Range types are parameterized by an element type.
* In lowering, ranges are treated as structured values with `lo`, `hi`, and `inclusive` fields.
* Range size depends on the element type and alignment rules.

---

## Function Types

Functions have a first-class type representation in the compiler.

A function type looks like:

```txt
func(param1, param2, ...) -> returnType
```

### Example

```rux
let f: func(int32, int32) -> int32;
```

### Notes

* Function types preserve parameter order.
* The final element in the internal representation is the return type.
* Variadic parameters are handled specially and are not stored as normal parameters in the internal function type list.

---

## Type Parameters

Rux supports type parameters in the compiler type system.

```rux
func Identity<T>(value: T) -> T {
    return value;
}

struct Box<T> {
    value: T;
}
```

Type parameters are represented in the compiler as unresolved type variables.

### Notes

* Type parameters are preserved through parsing, semantic analysis, and lowering.
* They are not the same as concrete named types.
* They occupy no fixed byte size until specialized into a concrete type.

---

## Type Syntax

### Pointer syntax

```rux
*T
*const T
```

### Tuple syntax

```rux
(T, U)
```

### Slice syntax

```rux
T[]
T[N]
```

### Named type syntax

```rux
Name
Namespace::Name
Name<T>
```

### Self type

`self` appears in method and implementation contexts as the current receiver type.

```rux
func Length(self) -> float64
```

---

## Type Inference

The compiler infers types in many places when the surrounding context makes the type clear.

```rux
let x = 42;
let y = 3.14;
let z = true;
```

Inferred types are determined from the initializer and any surrounding expected type.

### Notes

* Inference is convenient for local code.
* Explicit annotations are better when precision or clarity matters.
* If the compiler cannot infer a type, it will report an error or keep the type unknown for recovery.

---

## Type Compatibility

Rux does not treat all numeric types as freely interchangeable.

### Exact matching

Most numeric types must match exactly unless an explicit cast is used.

```rux
let x: int32 = 5;
let y: int64 = x; // not always allowed implicitly
```

### Implicit widening

Some widening conversions are accepted automatically.

* `float32` can widen to `float64`
* `int8`, `int16`, `int32` can widen to `int`
* `uint8`, `uint16`, `uint32` can widen to `uint`
* `int64` and `int` interoperate
* `uint64` and `uint` interoperate

### Boolean compatibility

Boolean types are mutually assignable across boolean widths.

### Pointer compatibility

Any pointer is implicitly assignable to `*opaque`.

### Unknown types

Unknown types are treated leniently during recovery and intermediate compilation stages.

---

## Size and Layout

The compiler tracks type size for code generation and storage allocation.

### Fixed-size primitives

Typical sizes in bytes:

* `bool8`, `char8`, `int8`, `uint8` → 1
* `bool16`, `char16`, `int16`, `uint16` → 2
* `bool32`, `char32`, `int32`, `uint32`, `float32` → 4
* `int64`, `uint64`, `int`, `uint`, `float64`, pointers, `String`, function values → 8
* slices → 16

### Compound sizes

* tuples are the sum of their element sizes in the current model
* ranges depend on the element size and alignment
* named types resolve to their underlying structure where possible

### Notes

* Unknown and type-parameter sizes are not fixed until more type information is available.
* `opaque` has size 0 in the compiler’s size model.
* Some backend paths treat named types with generic arguments as concrete runtime-sized values.

---

## Strings

Rux distinguishes between string-like values and the compiler’s internal string type representation.

### String type

The type system includes a `String`-like built-in representation.

### String literals

String literals often lower into slice-like values with a character element type.

```rux
"hello"
c8"hello"
c16"hello"
c32"hello"
```

The element type depends on the literal prefix.

---

## Character Literals

Character literals may be prefixed to choose width.

```rux
'a'
c8'a'
c16'a'
c32'a'
```

The type of a character literal depends on the prefix.

---

## Numeric Literals

Numeric literals may include base prefixes and type suffixes.

### Base prefixes

```rux
42
0x2A
0b101010
0o52
```

### Suffixes

```rux
1i8
1i16
1i32
1i64
1i
1u8
1u16
1u32
1u64
1u
1f32
1f64
```

Suffixes help lock the literal to a specific type.

### Unsuffixed integers

Unsuffixed integer literals can be checked against the target type.

If the value does not fit, the compiler emits an out-of-range diagnostic.

---

## Examples

### Primitive values

```rux
let a: int32 = 42;
let b: float64 = 12.5;
let c: bool = true;
```

### Pointer and slice values

```rux
let p: *int32 = null;
let s: uint8[] = [1, 2, 3];
```

### Tuple value

```rux
let pair: (int32, int32) = (1, 2);
```

### Generic type usage

```rux
struct Box<T> {
    value: T;
}

let x: Box<int32> = Box<int32> { value: 5 };
```

### Range value

```rux
let r: Range<int32> = 0..10;
```

---

## Common Errors

### Type mismatch

```rux
let x: int32 = 3.14;
```

### Invalid pointer assignment

```rux
let p: *int32 = 10;
```

### Out-of-range integer literal

```rux
let x: uint8 = 1000;
```

### Using an unknown type parameter as a concrete size

```rux
func Foo<T>(value: T) {
    let size = sizeof<T>;
}
```

If the compiler cannot determine a concrete size, it will keep the type unresolved until more information is available.

---

## Implementation Notes

This section reflects what the compiler currently does internally.

### Type representation

The compiler uses an internal `TypeRef` structure with kinds such as:

* `Unknown`
* `Opaque`
* booleans
* characters
* signed and unsigned integers
* floating-point numbers
* pointers
* slices
* ranges
* tuples
* named types
* type parameters
* function types

### Type printing

Types have a canonical string form used in diagnostics and lowering.

Examples:

* `*int32`
* `char8[]`
* `(int32, float64)`
* `func(int32, int32) -> int32`

### Assignability rules

The semantic analyzer uses a lenient compatibility model for unknowns and a narrower model for concrete numeric conversions.

### Backend layout

The lowering pipeline uses the type system to decide:

* stack allocation size
* field offsets
* function argument passing
* slice and interface representation
* interface vtables
* cast insertion
