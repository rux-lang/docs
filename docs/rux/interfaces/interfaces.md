# Interfaces

Interfaces define a named contract of methods that a type can satisfy.

An interface says what operations a type must support, not how the type stores its data. That makes interfaces useful for abstraction, dispatch, and code that wants to work across multiple concrete types without caring about the exact representation.

In Rux, interfaces are treated as real declarations by the parser, tracked as first-class symbols by semantic analysis, preserved through HIR lowering, and lowered to a vtable-based fat-pointer model in LIR and the backend pipeline.

---

## Summary

```rux
interface Display {
    func ToString(self) -> String;
}

struct Vector {
    x: float64;
    y: float64;
    z: float64;
}

extend Vector : Display {
    func ToString(self) -> String {
        return "Vector";
    }
}

extend Display for Vector {
    func ToString(self) -> String {
        return "Vector";
    }
}
```

An interface declaration may include:

* an optional `pub` modifier
* a name
* a brace-delimited method list
* one or more `func` declarations in the body

An interface implementation may be written with `extend` in either of these forms:

* `extend TypeName : InterfaceName { ... }`
* `extend InterfaceName for TypeName { ... }`

---

## What an Interface Means

An interface is a method contract.

It does not describe storage layout.
It does not define fields.
It does not define default data.
It only says: a type using this interface must provide the listed methods.

That distinction matters.

### Good practice

Use an interface when you want behavior shared across unrelated types.

```rux
interface Display {
    func ToString(self) -> String;
}
```

```rux
interface Writer {
    func Write(self, data: uint8[]) -> uint64;
}
```

### Bad practice

Do not use an interface as a substitute for a struct, a union, or an enum.

```rux
// bad idea: this is trying to model state, not behavior
interface UserData {
    func Name(self) -> String;
    func Age(self) -> uint32;
}
```

That may look expressive, but if the thing really has data, a concrete type is usually the clearer design.

---

## Interface Declaration Syntax

The general shape of an interface is:

```rux
interface Name {
    func Method(self) -> ReturnType;
}
```

### Example

```rux
interface Display {
    func ToString(self) -> String;
}
```

### Public interfaces

An interface may be marked `pub`.

```rux
pub interface Serializable {
    func Serialize(self) -> uint8[];
}
```

Public visibility controls whether the interface is visible outside the defining scope, using the same visibility model as the rest of the language.

### Notes

* The parser recognizes `interface` declarations at top level.
* Interface bodies contain `func` declarations.
* The reviewed parser does not show interface type parameters.
* The reviewed parser does not show interface fields.

---

## Interface Methods

An interface is made up of methods.

```rux
interface Display {
    func ToString(self) -> String;
}
```

### Method rules

* Each method must be declared with `func`.
* The interface body does not accept random statements or fields.
* The semantic analyzer checks that method names are unique within the interface.
* Each method’s parameters and return type are resolved like normal function types.

### Good practice

Keep interface method sets small and intention-focused.

```rux
interface Display {
    func ToString(self) -> String;
}
```

```rux
interface Readable {
    func Read(self, buffer: uint8[]) -> uint64;
}
```

Small contracts are easier to implement, easier to test, and easier to reason about.

### Bad practice

Do not overload an interface with too many unrelated requirements.

```rux
interface MegaObject {
    func ToString(self) -> String;
    func Serialize(self) -> uint8[];
    func Hash(self) -> uint64;
    func Clone(self) -> Self;
    func DebugDump(self) -> String;
}
```

That kind of interface becomes annoying to implement and hard to reuse.

---

## Interface Body Rules

The reviewed parser accepts `func` declarations inside the interface body.

```rux
interface MathLike {
    func Abs(self) -> int32;
    func Sign(self) -> int32;
}
```

### Notes

* The parser expects `func` inside an interface body.
* Each method is parsed with normal function syntax.
* The semantic analyzer records the method names for duplicate checking and later implementation validation.

### Good practice

Use clean, signature-style method declarations.

```rux
interface Display {
    func ToString(self) -> String;
}
```

### Bad practice

Do not depend on interface methods behaving like full concrete implementations.

```rux
interface Weird {
    func DoThing(self) -> int32 {
        return 1;
    }
}
```

Even if the parser can accept the shape, interfaces are conceptually a contract, not a home for actual behavior.

---

## Implementing an Interface with `extend`

Interfaces are implemented through `extend`.

The parser supports two equivalent forms:

```rux
extend Vector : Display {
    func ToString(self) -> String {
        return "Vector";
    }
}
```

and:

```rux
extend Display for Vector {
    func ToString(self) -> String {
        return "Vector";
    }
}
```

### What this means

Both forms attach methods to a concrete type and optionally declare that the type implements an interface.

The implementation is not just a loose comment. The semantic analyzer checks that the interface exists and that all required methods are present.

### Good practice

Use the form that reads best for the surrounding codebase, but keep it consistent in the project.

```rux
extend Vector : Display {
    func ToString(self) -> String {
        return "Vector";
    }
}
```

### Bad practice

Do not scatter interface implementations across unrelated files unless the codebase has a strong module convention for it.

```rux
extend Display for Vector {
    func ToString(self) -> String {
        return "Vector";
    }
}
```

That is valid, but if implementations are spread everywhere, searching becomes painful.

---

## How Interface Implementation Is Checked

The semantic analyzer tracks which methods are attached to which type.

When an `extend` block names an interface, the compiler checks:

* that the target type exists
* that the interface exists
* that every required interface method is present in the implementation

### Example

```rux
interface Display {
    func ToString(self) -> String;
}

struct Vector {
    x: float64;
    y: float64;
    z: float64;
}

extend Vector : Display {
    func ToString(self) -> String {
        return "Vector";
    }
}
```

### Missing method example

```rux
extend Vector : Display {
    // missing ToString
}
```

That should be rejected because the implementation does not satisfy the contract.

### Unknown interface example

```rux
extend Vector : NotARealInterface {
    func ToString(self) -> String {
        return "Vector";
    }
}
```

That should be rejected because the interface name must resolve to a known interface.

### Good practice

Keep interface implementations complete and explicit.

```rux
extend Vector : Display {
    func ToString(self) -> String {
        return "Vector";
    }
}
```

### Bad practice

Do not define an `extend` block with an interface name and then leave the required methods half-done.

```rux
extend Vector : Display {
    func SomethingElse(self) -> String {
        return "oops";
    }
}
```

That is the kind of thing that compiles only if your compiler forgets to check the contract, and that would be a bug.

---

## Interface Satisfaction

A type satisfies an interface when the compiler can prove it has the required methods.

That can matter in assignment and conversion contexts.

### Example

```rux
interface Display {
    func ToString(self) -> String;
}

extend Vector : Display {
    func ToString(self) -> String {
        return "Vector";
    }
}

let d: Display = Vector { x: 1.0, y: 2.0, z: 3.0 };
```

### Notes

* The semantic analyzer treats interface compatibility as a distinct assignability rule.
* Empty interfaces are trivially satisfied by any type.
* For non-empty interfaces, the compiler checks whether the type’s recorded interface implementation contains the target interface name.
* Integer platform aliases such as `int` and `uint` may be checked through their corresponding fixed-width forms during interface satisfaction in the current analyzer logic.

### Good practice

Use interface assignments to express abstraction boundaries.

```rux
func PrintAny(value: Display) {
    Print(value.ToString());
}
```

### Bad practice

Do not use interface types everywhere just because you can.

```rux
func Work(value: Display) {
    // if every function becomes interface-driven, you lose concrete clarity fast
}
```

Interfaces are powerful, but overusing them can make code harder to optimize and harder to follow.

---

## Interface Calls

When a value is used as an interface, the compiler lowers method calls through a vtable-based dispatch model.

That means the call is resolved by looking up the method through the interface metadata rather than by calling a concrete symbol directly.

### Example

```rux
func PrintIt(value: Display) {
    Print(value.ToString());
}
```

### What the compiler does conceptually

1. keep the concrete data pointer
2. keep a vtable pointer for the interface implementation
3. use the method index to find the function pointer
4. call indirectly through that function pointer

### Good practice

Use interface dispatch when the caller genuinely does not care about the concrete type.

```rux
func Render(value: Display) {
    Print(value.ToString());
}
```

### Bad practice

Do not route hot inner loops through interface dispatch unless the abstraction is really worth the overhead.

```rux
for item in items {
    Print(item.ToString());
}
```

This may be perfectly fine for application code, but it is not free.

---

## Memory Model

Interfaces are not plain structs.

The current lowering pipeline models them as a 16-byte fat pointer:

* 8 bytes for the data pointer
* 8 bytes for the vtable pointer

### Shape

```text
{ data_ptr, vtable_ptr }
```

### Why this matters

That representation is used by lowering and by the backend when copying, storing, or calling through an interface value.

### Example

```rux
let d: Display = Vector { x: 1.0, y: 2.0, z: 3.0 };
```

The lowered value is not just the raw `Vector`. It is a pair of pointers describing the concrete storage and the interface dispatch table.

### Good practice

Remember that interface values carry indirection.

```rux
func Use(value: Display) {
    Print(value.ToString());
}
```

### Bad practice

Do not assume interface values are zero-cost or the same size as the underlying type.

```rux
let x: Display = Vector { x: 1.0, y: 2.0, z: 3.0 };
```

The interface value is larger and less direct than the concrete value.

---

## Size Rules

The current compiler model gives interfaces a size of 16 bytes.

That matches the fat-pointer representation:

* `data` pointer = 8 bytes
* `vtable` pointer = 8 bytes

### Layout example

```rux
interface Display {
    func ToString(self) -> String;
}
```

Typical interface layout:

| Field  | Offset | Size |
| ------ | -----: | ---: |
| data   |      0 |    8 |
| vtable |      8 |    8 |

Total size:

```text
16 bytes
```

### Notes

* The HIR size model returns 16 bytes for interface named types.
* The RCU lowering path also treats interface names as 16-byte values in field lookup and layout handling.
* The LIR lowering path copies interface values as two pointer-sized fields.

### Good practice

Treat interface values as a fixed-size abstraction wrapper.

```rux
let value: Display = Vector { x: 1.0, y: 2.0, z: 3.0 };
```

### Bad practice

Do not hard-code assumptions about interface size unless you are specifically targeting this compiler’s current runtime model.

---

## Interface Methods and `self`

Interface methods are usually written with `self` as the first parameter.

```rux
interface Display {
    func ToString(self) -> String;
}
```

That matches the way methods are later lowered and associated with concrete receiver types.

### Notes

* The parser already recognizes `self` as a special parameter form.
* Lowering creates an implicit self binding for methods inside `extend` blocks.
* Interface methods are checked using their declared parameter and return types.

### Good practice

Make the receiver explicit and consistent.

```rux
interface Cloneable {
    func Clone(self) -> Self;
}
```

### Bad practice

Do not hide the receiver in a confusing parameter shape.

```rux
interface Weird {
    func Clone(x: Self) -> Self;
}
```

That is legal-looking but semantically awkward.

---

## Examples

### Simple interface

```rux
interface Display {
    func ToString(self) -> String;
}
```

### Public interface

```rux
pub interface Serializable {
    func Serialize(self) -> uint8[];
}
```

### Type implementing an interface

```rux
struct Vector {
    x: float64;
    y: float64;
    z: float64;
}

extend Vector : Display {
    func ToString(self) -> String {
        return "Vector";
    }
}
```

### Alternative implementation form

```rux
extend Display for Vector {
    func ToString(self) -> String {
        return "Vector";
    }
}
```

### Interface-based API

```rux
interface Writer {
    func Write(self, data: uint8[]) -> uint64;
}

func Log(writer: Writer, bytes: uint8[]) {
    writer.Write(bytes);
}
```

---

## Common Errors

### Missing method in interface body

```rux
interface Bad {
    value: int32;
}
```

### Duplicate method name in interface

```rux
interface Bad {
    func A(self);
    func A(self);
}
```

### Unknown interface in `extend`

```rux
extend Vector : NotAnInterface {
    func ToString(self) -> String {
        return "Vector";
    }
}
```

### Missing required method in implementation

```rux
interface Display {
    func ToString(self) -> String;
}

extend Vector : Display {
    func Other(self) -> String {
        return "Vector";
    }
}
```

### Unknown target type in `extend`

```rux
extend MissingType : Display {
    func ToString(self) -> String {
        return "x";
    }
}
```

### Bad practice: giant interface for tiny behavior

```rux
interface DoEverything {
    func Read(self, data: uint8[]) -> uint64;
    func Write(self, data: uint8[]) -> uint64;
    func Open(self) -> bool;
    func Close(self) -> bool;
    func Flush(self) -> bool;
    func Seek(self, pos: uint64) -> bool;
}
```

That kind of interface often becomes a maintenance burden.

---

## Notes

### Interfaces are contracts, not objects

An interface describes what a type can do.
It does not describe what a type is made of.

### Empty interfaces are special

An empty interface is trivially satisfied by every type in the current semantic model.

That is useful, but it also means empty interfaces can easily become too broad to be meaningful.

### The current implementation is vtable-based

The lowering pipeline turns interface values into a concrete data pointer plus a vtable pointer.

That is why interface calls and interface copies behave differently from plain value copies.

### Methods are tracked by name

The semantic analyzer stores interface method names and compares them against implementation methods when validating `extend` blocks.

### No interface type parameters in the reviewed parser

The reviewed parser shows plain `interface Name { ... }` syntax, not a generic `interface Name<T> { ... }` form.

---

## Implementation Notes

This section describes how the compiler currently handles interfaces internally.

### Parsing

The parser recognizes:

* `interface Name { ... }`
* optional `pub`
* `func` declarations in the interface body
* `extend TypeName : InterfaceName { ... }`
* `extend InterfaceName for TypeName { ... }`

### Semantic analysis

The semantic analyzer:

* stores interfaces in a dedicated symbol kind
* records method names for each interface
* rejects duplicate method names inside one interface
* resolves method parameter and return types
* checks `extend` blocks against required interface methods
* tracks which concrete types implement which interfaces
* uses interface satisfaction during assignability checks
