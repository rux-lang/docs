# Variables

Variables bind a name to a value.

In Rux, variables are introduced with `let` or `var`:

* `let` creates an immutable binding.
* `var` creates a mutable binding.

Variables follow lexical scope rules, which means a binding is only visible inside the scope where it was declared and any nested scope that can legally access it.

---

## Summary

```rux
let x = 42;
var count = 0;

let name: char8[] = "Rux";
var total: int32 = 10;
```

A variable declaration may include:

* a binding name or pattern
* an optional type annotation
* an initializer
* mutability (`let` or `var`)

---

## Declaration Forms

### Immutable variable

```rux
let value = 123;
```

Creates a binding that cannot be reassigned after initialization.

### Mutable variable

```rux
var value = 123;
```

Creates a binding that may be reassigned later.

### Explicitly typed variable

```rux
let port: uint16 = 8080;
var index: uint = 0;
```

The declared type constrains the initializer and later assignments.

### Pattern declaration

Rux also supports declarations that bind multiple values through a pattern.

```rux
let (x, y) = GetPoint();
```

Pattern declarations are useful when the initializer returns a structured value.

---

## Mutability

### `let`

`let` introduces an immutable binding.

```rux
let x = 5;
```

After initialization, `x` cannot be assigned a new value.

### `var`

`var` introduces a mutable binding.

```rux
var x = 5;
x = 6;
```

A mutable binding may be reassigned, provided the new value is compatible with the variable’s type.

### Mutability and type compatibility

Mutability only controls whether reassignment is allowed. It does not change the type rules.

```rux
var value: int32 = 10;
value = 20;
```

This is valid because the assigned value matches the declared type.

```rux
var value: int32 = 10;
value = "hello";
```

This is invalid because the assigned value is not compatible with `int32`.

---

## Type Inference

Rux infers variable types from the initializer when possible.

```rux
let x = 42;
let y = 3.14;
let z = true;
```

In these examples, the compiler infers the variable types from the initializer expressions.

Type inference is convenient for local values where the type is obvious from the right-hand side.

### When inference is available

Inference is available when the compiler can determine the initializer type.

```rux
let message = "hello";
let answer = 42;
var counter = 0;
```

### When inference is not enough

If the compiler cannot determine the type from context, an explicit annotation is required.

```rux
let value: int32 = ComputeValue();
```

This is the preferred form when the initializer alone is not enough to establish the type.

### Best practice

Use inference when the type is obvious.
Use an explicit annotation when the type matters for readability, ABI, overload resolution, or precision.

---

## Explicit Types

A variable may declare its type explicitly.

```rux
let count: uint32 = 10;
var total: int64 = 0;
```

The initializer must be compatible with the declared type.

### Why explicit types matter

Explicit types are useful when:

* the value should have a specific width
* the value crosses an FFI boundary
* the compiler would otherwise infer a broader or narrower type
* the code must communicate intent clearly

Example:

```rux
let fd: int = OpenFile(...);
```

Here the type is explicit because the value is part of a system-level interface.

---

## Initialization Rules

A variable declaration normally includes an initializer.

```rux
let x = 10;
var y = 20;
```

In many cases, the initializer is required because the compiler uses it to determine or validate the variable’s type.

### Uninitialized declarations

If a declaration does not have an initializer, it must still be meaningful to the compiler. In practice, this means the declaration needs enough information to establish its type.

```rux
var value: int32;
```

That form can be used when the language permits an explicitly typed declaration without immediate initialization.

If a declaration cannot be typed or made valid without an initializer, it is rejected.

---

## Scope

Variables obey lexical scope.

A binding is visible from its declaration point onward within the current scope and nested scopes, but not outside the scope where it was introduced.

```rux
{
    let x = 10;
    Print(x);
}

Print(x);
```

The second `Print(x)` is invalid because `x` is out of scope.

### Shadowing

A name can be reused in a nested scope.

```rux
let x = 1;

{
    let x = 2;
    Print(x);
}

Print(x);
```

The inner `x` shadows the outer one inside the block.

Shadowing is useful when a value is transformed and the original binding is no longer needed.

---

## Assignment

Only mutable variables can be reassigned.

```rux
var counter = 0;
counter = counter + 1;
```

Attempting to assign to an immutable binding is an error.

```rux
let counter = 0;
counter = 1;
```

### Compound assignment

Rux supports compound assignment operators for common update patterns.

```rux
var value = 10;
value += 5;
value -= 2;
value *= 3;
```

These forms are only valid when the left-hand side is a valid assignable location and the operation is defined for the operand types.

### Assignment compatibility

The assigned value must be compatible with the variable’s type.

```rux
var x: int32 = 5;
x = 10;
```

Valid.

```rux
var x: int32 = 5;
x = 3.14;
```

Invalid unless an explicit conversion is performed.

---

## Destructuring

Rux supports declarations that bind from structured values.

```rux
let (x, y) = GetPoint();
```

This is useful when a function returns multiple values or a tuple-like value.

Pattern declarations are especially useful for unpacking results without introducing temporary variables.

```rux
let (width, height) = GetSize();
```

### Notes on patterns

Pattern bindings should be read as declarations, not as general-purpose assignment syntax.

That means the structure of the pattern must match the structure of the initializer.

---

## Examples

### Simple immutable variable

```rux
let answer = 42;
```

### Simple mutable variable

```rux
var tries = 0;
tries += 1;
```

### Explicit type annotation

```rux
let port: uint16 = 8080;
```

### String value

```rux
let name: char8[] = "Alice";
```

### Shadowing in a nested scope

```rux
let value = 10;

{
    let value = 20;
    Print(value);
}

Print(value);
```

### Destructuring

```rux
let (x, y) = GetPoint();
```

---

## Common Errors

### Assigning to an immutable variable

```rux
let x = 1;
x = 2;
```

### Using a variable outside its scope

```rux
{
    let x = 1;
}

Print(x);
```

### Missing type where the compiler cannot infer one

```rux
let value;
```

### Type mismatch on assignment

```rux
var count: int32 = 0;
count = "hello";
```

### Pattern mismatch

```rux
let (x, y) = GetSingleValue();
```

---

## Notes

### Immutability does not mean deep immutability

`let` prevents reassignment of the binding itself. It does not automatically imply that every referenced object is frozen forever unless the type system or runtime rules say so.

### Types are fixed after declaration

A variable does not change type just because a later assignment uses a different expression.

### Prefer explicit types at boundaries

Use explicit types where the value crosses modules, packages, or FFI boundaries.

### Prefer inference for local clarity

When the initializer makes the type obvious, inference keeps code compact.

---

## Implementation Notes

This section is for readers who want to know how the compiler handles variables internally.

### Parsing

The parser recognizes variable declarations using `let` and `var`.

A declaration may include a name, an optional type annotation, and an initializer.

### Semantic analysis

The semantic analyzer resolves the declared type, checks mutability, validates assignment compatibility, and tracks scope.

It also handles pattern-based declarations and can infer or validate the resulting type.

### HIR lowering

In the high-level intermediate representation, variables keep their type and mutability information.

This is where the compiler preserves the source-level meaning of the declaration before lower-level storage decisions are made.

### LIR lowering

At the low-level IR stage, a local variable typically becomes storage allocated in the current function.

The initializer is written into that storage, and later reads load from the associated slot.

That means the compiler eventually turns a variable declaration into real storage plus load/store operations.
