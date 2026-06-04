# Pointers

Pointers represent memory addresses rather than values.

A pointer stores the address of another object and allows indirect access to that object's storage.

Pointers are a fundamental part of Rux and are commonly used for:

* low-level memory manipulation
* FFI interoperability
* operating system APIs
* dynamic data structures
* slice and interface implementations

## Summary

```rux
let value = 42;

let ptr: *int32 = &value;

let current = *ptr;

*ptr = 100;

let raw: *opaque = ptr;

let empty: *int32 = null;
```

Pointer-related syntax:

```rux
*T
*const T

&value
*pointer

null

value as *T
```

---

# Description

Pointers refer to memory locations rather than directly storing values.

A pointer type always refers to another type called the **pointee type**.

```rux
*int32
```

The above type represents a pointer to an `int32`.

```rux
*Point
```

The above type represents a pointer to a `Point`.

Pointers are strongly typed.

A pointer to one type is not automatically interchangeable with a pointer to another type.

---

# Pointer Types

## Mutable Pointers

Mutable pointers are declared using:

```rux
*T
```

Example:

```rux
var value = 10;

let ptr: *int32 = &value;

*ptr = 20;
```

The pointer may be dereferenced to read or modify the referenced value.

---

## Const Pointers

The parser recognizes:

```rux
*const T
```

Example:

```rux
let text: *const char8;
```

This syntax is commonly used when interacting with foreign APIs that expect read-only memory.

Example:

```rux
extern {
    func Print(
        text: *const char8
    );
}
```

---

## Opaque Pointers

Untyped pointers use:

```rux
*opaque
```

Example:

```rux
let handle: *opaque;
```

`opaque` represents an intentionally uninterpreted type.

It is most commonly used for:

* operating system handles
* foreign library objects
* generic FFI pointers
* raw memory references

Example:

```rux
extern {
    func CreateHandle() -> *opaque;
}
```

### Notes

Any pointer type may be assigned to `*opaque`.

```rux
let ptr: *int32 = &value;

let raw: *opaque = ptr;
```

This behavior is implemented directly in the compiler's assignability rules.

---

# Creating Pointers

## Address-Of Operator

The unary `&` operator creates a pointer.

```rux
let value = 5;

let ptr = &value;
```

The resulting type is a pointer to the operand's type.

Example:

```rux
let number: int32 = 42;

let ptr = &number;
```

Result:

```rux
*int32
```

---

# Dereferencing

The unary `*` operator dereferences a pointer.

```rux
let value = *ptr;
```

Dereferencing accesses the value stored at the memory location referenced by the pointer.

Example:

```rux
let number = 42;

let ptr = &number;

let copy = *ptr;
```

Result:

```rux
copy == 42
```

---

## Writing Through a Pointer

Dereferencing may also be used on the left side of an assignment.

```rux
*ptr = 100;
```

Example:

```rux
var number = 42;

let ptr = &number;

*ptr = 100;
```

Result:

```rux
number == 100
```

---

# Null Pointers

Rux provides a dedicated null pointer literal.

```rux
null
```

Example:

```rux
let ptr: *int32 = null;
```

Null represents the absence of a valid memory address.

Common uses:

* optional references
* uninitialized handles
* FFI APIs
* sentinel values

---

## Notes

The parser recognizes `null` as a built-in keyword.

During lowering, null is represented internally as a zero-valued pointer.

---

# Casting Pointers

Pointers may participate in explicit casts.

```rux
value as Type
```

Example:

```rux
let raw: *opaque;

let ptr = raw as *int32;
```

Pointer reinterpretation should always be explicit.

The compiler does not automatically convert between unrelated pointer types.

---

# Type Compatibility

Pointer compatibility is intentionally strict.

## Valid

```rux
let ptr: *int32 = &value;
```

```rux
let raw: *opaque = ptr;
```

## Invalid

```rux
let ptr: *float64 = &value;
```

where:

```rux
value: int32
```

The pointee types do not match.

---

# Pointer Size

All pointer types occupy a fixed size.

Current size:

| Type     | Size    |
| -------- | ------- |
| *T       | 8 bytes |
| *const T | 8 bytes |
| *opaque  | 8 bytes |

This size is used by the compiler's internal layout model.

---

# Pointers and Slices

Slices internally contain a pointer and a length.

Example:

```rux
let values: int32[];
```

Conceptually:

```rux
struct Slice<T> {
    data: *T;
    length: uint;
}
```

A slice therefore occupies:

```text
16 bytes
```

on current targets.

---

# Pointers and Interfaces

Interface values internally contain pointer data.

Conceptually:

```rux
struct Interface {
    data: *opaque;
    vtable: *opaque;
}
```

The compiler treats interface values as a pair of pointers.

---

# FFI Usage

Pointers are heavily used for interoperability.

Example:

```rux
@[Import(lib: "Kernel32.dll")]
extern {
    func CloseHandle(
        handle: *opaque
    ) -> bool32;
}
```

Example:

```rux
let handle = CreateHandle();

CloseHandle(handle);
```

---

# Examples

## Basic Pointer

```rux
let value = 42;

let ptr = &value;

Print(*ptr);
```

---

## Modifying a Value

```rux
var count = 10;

let ptr = &count;

*ptr = 20;
```

---

## Opaque Pointer

```rux
let handle: *opaque;
```

---

## Null Pointer

```rux
let ptr: *int32 = null;
```

---

## Cast

```rux
let raw: *opaque;

let typed = raw as *int32;
```

---

# Common Errors

## Dereferencing a Non-Pointer

```rux
let value = 10;

let x = *value;
```

Error:

```text
cannot dereference non-pointer type
```

---

## Invalid Assignment

```rux
let ptr: *int32 = 10;
```

Error:

```text
cannot assign integer to pointer
```

---

## Incompatible Pointer Types

```rux
let ptr: *float64 = &value;
```

where:

```rux
value: int32
```

Error:

```text
incompatible pointer types
```

---

# Implementation Notes

## Parsing

The parser recognizes:

```rux
*T
```

```rux
*const T
```

for pointer types.

The parser also recognizes:

```rux
&expr
```

and

```rux
*expr
```

as unary operators.

---

## Type System

Pointers are represented internally using:

```text
TypeRef::Kind::Pointer
```

The pointee type is stored as the pointer's inner type.

Example:

```rux
*int32
```

becomes:

```text
Pointer(
    Int32
)
```

---

## Assignability

The semantic analyzer contains a special compatibility rule:

```rux
*T -> *opaque
```

This conversion is implicit.

Other pointer conversions require explicit casts.

---

## Lowering

Pointers are lowered as native machine-address values.

Current pointer size:

```text
8 bytes
```

The backend treats pointer values as address-sized storage locations.
