# Functions

Functions are callable declarations that group executable behavior behind a name.

A function may be:

* a normal function with a body
* a signature-only declaration
* an operator function
* a method declared inside an `extend` block
* an `extern` declaration bound to an external symbol
* an `asm` function backed by hand-written assembly

Functions may also be generic, variadic, overloaded, and optionally public.

---

## Summary

```rux
func Add(a: int32, b: int32) -> int32 {
    return a + b;
}

func PrintLine(text: char8[]);

func Add(a: float64, b: float64) -> float64 {
    return a + b;
}

func +(a: Vector, b: Vector) -> Vector {
    return Vector { x: a.x + b.x, y: a.y + b.y, z: a.z + b.z };
}
```

A function declaration may include:

* an optional `pub` modifier
* an optional `asm` prefix
* a name
* optional type parameters
* a parameter list
* an optional return type
* either a body or a trailing semicolon

---

## Function Kinds

### Regular functions

Regular functions are declared with `func`.

```rux
func Add(a: int32, b: int32) -> int32 {
    return a + b;
}
```

These are the standard callable declarations used for ordinary code.

### Signature-only functions

A function may be declared without a body.

```rux
func PrintLine(text: char8[]);
```

This form is useful for declarations that are defined elsewhere or only needed as a signature.

### Operator functions

Functions may use operator names.

```rux
func +(a: Vector, b: Vector) -> Vector {
    return Vector { x: a.x + b.x, y: a.y + b.y, z: a.z + b.z };
}
```

Operator functions participate in overload resolution like normal named functions.

### Methods

Methods are functions declared inside an `extend` block.

```rux
extend Vector {
    func Length(self) -> float64 {
        return Sqrt(self.x * self.x + self.y * self.y + self.z * self.z);
    }
}
```

Methods are called using the `.` syntax on a value, and the compiler resolves the correct method based on the receiver type.

### External functions

External functions are declared with `extern`.

```rux
extern func CreateFileA(name: char8[], access: uint32) -> *opaque;
```

These declarations describe symbols that are provided by a DLL, system library, or another external object file.

### Assembly functions

A function may be marked `asm`.

```rux
asm func FastAdd(a: int32, b: int32) -> int32;
```

Assembly functions are part of the function system, but their implementation is expected to come from assembly rather than normal Rux source.

---

## Function Declaration Syntax

The general shape of a function is:

```rux
func Name<TypeParams>(params) -> ReturnType {
    body
}
```

or:

```rux
func Name(params) -> ReturnType;
```

### Example

```rux
pub func Clamp(value: int32, min: int32, max: int32) -> int32 {
    if value < min {
        return min;
    }
    if value > max {
        return max;
    }
    return value;
}
```

### Public functions

`pub` marks the function as publicly visible.

```rux
pub func Exported() -> int32 {
    return 1;
}
```

Public visibility is especially important for packages and libraries.

---

## Parameters

A function parameter has a name and a type.

```rux
func Add(a: int32, b: int32) -> int32 {
    return a + b;
}
```

### Parameter syntax

```rux
name: Type
```

Example:

```rux
func Square(value: int32) -> int32 {
    return value * value;
}
```

### Parameter names

Parameter names are part of the declaration and are available inside the function body.

```rux
func Mix(left: int32, right: int32) -> int32 {
    return left + right;
}
```

### Parameter types

Every non-variadic parameter has a type.

```rux
func PrintNumber(value: int32);
```

The compiler uses parameter types for type checking, overload resolution, and lowering.

---

## Return Types

A function may declare a return type with `->`.

```rux
func Add(a: int32, b: int32) -> int32 {
    return a + b;
}
```

If no return type is written, the compiler treats the function as returning an opaque or implicit default return type depending on the compilation stage.

```rux
func Log(text: char8[]) {
    Print(text);
}
```

### Why explicit return types matter

Explicit return types help with:

* readability
* overload resolution
* API stability
* FFI compatibility
* compiler diagnostics

---

## Type Parameters

Functions may be generic.

```rux
func Identity<T>(value: T) -> T {
    return value;
}
```

### Syntax

```rux
func Name<T, U>(params) -> ReturnType
```

### Example

```rux
func First<T>(value: T) -> T {
    return value;
}
```

Type parameters are part of the function signature and influence type resolution.

---

## Variadic Functions

A function may accept a variadic parameter.

```rux
func PrintAll(...items: char8[]) {
    // ...
}
```

Or in parameter form:

```rux
func Sum(values: int32...) -> int32 {
    // ...
}
```

Variadic parameters collect extra arguments into a slice-like value during lowering.

### Example

```rux
func LogAll(prefix: char8[], values: int32...) {
    // ...
}
```

### Call behavior

Variadic calls can be made in two ways:

* by passing separate trailing arguments
* by passing a spread argument when the language supports it

Example:

```rux
LogAll("sum", 1, 2, 3);
```

### Notes

* Variadic parameters are treated specially by the compiler.
* Only the last parameter may be variadic.
* Extra arguments beyond the fixed parameters are gathered into a slice.

---

## Default Parameters

A parameter may have a default value.

```rux
func DrawLine(x: int32, y: int32 = 0) {
    // ...
}
```

This allows a caller to omit trailing arguments when the compiler can safely fill them in.

### Example

```rux
func CreatePoint(x: float64, y: float64 = 0.0) -> Point {
    return Point { x: x, y: y };
}
```

### Call usage

```rux
CreatePoint(5.0);
CreatePoint(5.0, 7.0);
```

### Rules

* Default arguments are used for omitted trailing parameters.
* Defaults are applied in order from left to right.
* Default values must be compatible with the parameter type.

### Common mistake

```rux
func Foo(a: int32 = 1, b: int32) {
    // ...
}
```

Defaults only help when the omitted arguments are at the end of the call.

---

## Calling Functions

Functions are called by writing the function name followed by parentheses.

```rux
Add(1, 2);
```

### Argument checking

The compiler checks:

* number of arguments
* argument types
* variadic usage
* spread usage
* whether overload resolution can find a match

### Example

```rux
func Add(a: int32, b: int32) -> int32 {
    return a + b;
}

let result = Add(10, 20);
```

### Result type

The result of a call expression is the function’s return type.

---

## Overloads

Rux allows multiple functions with the same name.

```rux
func Add(a: int32, b: int32) -> int32 {
    return a + b;
}

func Add(a: float64, b: float64) -> float64 {
    return a + b;
}
```

### Overload selection

The compiler chooses a candidate based on the argument types.

In practice, overload resolution prefers:

1. exact matches
2. assignable matches
3. compatible variadic forms when relevant

If the compiler cannot prove a better match, it falls back to a reasonable candidate rather than leaving the call unresolved.

### Example

```rux
Add(1, 2);       // picks the int overload
Add(1.0, 2.0);   // picks the float overload
```

### Overload names in lowering

If a function name is overloaded, the compiler mangles the callee name using the parameter types so each overload gets a distinct internal symbol.

That means the source-level name stays the same, but the backend sees a unique implementation name.

---

## Methods and `extend`

Methods are functions attached to a type through `extend`.

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

Instance methods receive `self` as their first parameter.

```rux
func Length(self) -> float64 {
    return Sqrt(self.x * self.x + self.y * self.y + self.z * self.z);
}
```

When called, the compiler automatically supplies the receiver as the first argument.

```rux
let len = value.Length();
```

### Static methods

Methods that do not use `self` behave like associated functions.

```rux
extend Vector {
    func New(x: float64, y: float64, z: float64) -> Vector {
        return Vector { x: x, y: y, z: z };
    }
}
```

These are called with `::`:

```rux
let v = Vector::New(1.0, 2.0, 3.0);
```

### Method resolution

The compiler looks up methods based on the receiver type.

If the receiver is a pointer, that pointer type is used directly.
If the receiver is a value, the compiler takes its address when needed so methods can still receive `self` as a pointer.

### Method overloads

Methods can also be overloaded.

```rux
extend Vector {
    func Scale(self, factor: float64) -> Vector {
        return Vector { x: self.x * factor, y: self.y * factor, z: self.z * factor };
    }

    func Scale(self, factor: int32) -> Vector {
        return self.Scale(float64(factor));
    }
}
```

---

## Operator Methods

Functions may implement operators for a type.

```rux
extend Vector {
    func +(self, other: Vector) -> Vector {
        return Vector { x: self.x + other.x, y: self.y + other.y, z: self.z + other.z };
    }
}
```

This lets values of the type participate in operator syntax.

```rux
let sum = a + b;
```

Operator methods are still functions, so they follow the same type and overload rules as regular methods.

---

## External Functions

External functions describe symbols that live outside Rux source.

```rux
extern func MessageBoxA(text: char8[], caption: char8[]) -> int32;
```

### External blocks

Rux also supports grouped external declarations:

```rux
extern {
    func CreateFileA(...);
    func WriteFile(...);
    handle: *opaque;
}
```

### Attributes

External functions may be decorated with attributes such as:

* `@[Import(lib: "...")]`
* `@[Call(.Win64)]`
* `@[Target("Windows")]`

These control import libraries, calling conventions, and target-specific availability.

### Example

```rux
@[Import(lib: "Kernel32.dll")]
extern func GetCurrentProcessId() -> uint32;
```

### Notes

* External declarations usually do not have bodies.
* They are intended for FFI and platform integration.
* The compiler uses the declaration to generate the correct link and call information.

---

## Calling Conventions

Functions may use a calling convention.

```rux
@[Call(.Win64)]
extern func GetTickCount64() -> uint64;
```

Calling conventions matter when interfacing with foreign code, especially on Windows.

They affect how arguments are passed and how the backend emits calls.

---

## Empty Bodies and Signatures

A function can be declared as a pure signature.

```rux
func DoSomething(value: int32);
```

This is useful when only the type information is needed.

A normal function with a body is written with braces:

```rux
func DoSomething(value: int32) {
    Print(value);
}
```

---

## Examples

### Simple function

```rux
func Add(a: int32, b: int32) -> int32 {
    return a + b;
}
```

### Function with default parameter

```rux
func Greet(name: char8[] = "world") {
    Print("Hello, ");
    Print(name);
}
```

### Generic function

```rux
func Identity<T>(value: T) -> T {
    return value;
}
```

### Variadic function

```rux
func Sum(values: int32...) -> int32 {
    var total = 0;
    for value in values {
        total += value;
    }
    return total;
}
```

### Method

```rux
extend Point {
    func Length(self) -> float64 {
        return Sqrt(self.x * self.x + self.y * self.y);
    }
}
```

### Operator function

```rux
extend Point {
    func +(self, other: Point) -> Point {
        return Point { x: self.x + other.x, y: self.y + other.y };
    }
}
```

### External function

```rux
@[Import(lib: "Kernel32.dll")]
extern func GetCurrentProcessId() -> uint32;
```

---

## Common Errors

### Missing parameter type

```rux
func Bad(x) {
}
```

### Wrong number of arguments

```rux
Add(1);
```

### Calling an immutable-typed or unresolved overload incorrectly

```rux
Add("hello", "world");
```

### Invalid reassignment inside the function body

```rux
func Test() {
    let x = 1;
    x = 2;
}
```

### Invalid variadic usage

```rux
func Log(values: int32...) {
}

Log(1, 2, ...);
```

### Missing body when a body is required

```rux
func Compute(x: int32) -> int32
```

Depending on context, the compiler expects either a body or a trailing semicolon.

---

## Notes

### Functions are first-class at the type level

The compiler tracks function signatures as types.

That is why functions can be resolved, overloaded, lowered, and passed through the backend in a structured way.

### Methods are still functions

A method is not a separate language species.
It is a function attached to a type, with `self` handled specially by the compiler.

### Overload names may be mangled internally

Source code uses the same name for overloaded functions.
The backend uses a mangled form so each overload can be emitted as a distinct symbol.

### Variadic arguments become a slice-like value

Trailing variadic arguments are collected into a slice representation during lowering.

### Default arguments are inserted during lowering

If a call omits trailing parameters with defaults, the compiler fills them in before reaching the lower-level representation.

---

## Implementation Notes

This section describes how the compiler currently handles functions internally.

### Parsing

The parser recognizes:

* normal function declarations
* generic parameters
* parameter lists
* optional return types
* bodies or signatures
* `asm func`
* `extern func`
* methods inside `extend`
* operator function names

Parameters can also be marked variadic or given default values.

### Semantic analysis

The semantic analyzer records function symbols, resolves signatures, checks argument compatibility, and handles overload sets.

Function overloads are grouped under the same name.

When a function is called, the analyzer selects a matching overload using argument count and assignability rules.

### Method resolution

Method lookup is based on the receiver type.

The analyzer also handles interface methods and associated function types so that method calls and method references can be typed correctly.

### HIR lowering

At the HIR stage, a function is converted into a structured representation with:

* name
* public visibility
* calling convention
* parameter list
* return type
* body
* generic parameters

Overloaded functions are given distinct internal names.

Default arguments are injected during call lowering.
Variadic arguments are collapsed into a slice-like value when needed.

### LIR lowering

At the low-level IR stage, each function becomes an entry block plus the instructions needed to represent its body.

The lowering step allocates storage for ordinary parameters, treats slices and interfaces specially, and emits calls, loads, stores, and returns as needed.

External functions are lowered as declarations without bodies.
