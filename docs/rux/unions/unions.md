# Unions

Unions are user-defined composite types where multiple field names share the same storage.

A union gives one block of memory several possible shapes. At any moment, that memory should be interpreted as exactly one of the declared fields.

That makes unions useful for compact representations, low-level interop, tagged data models, and internal compiler or runtime structures.

---

## Summary

```rux
union Value {
    i: int32;
    f: float32;
    ptr: *opaque;
}

pub union TokenData {
    kind: uint32;
    payload: uint64;
}
```

A union declaration may include:

* an optional `pub` modifier
* a name
* a field list
* one type annotation per field

Union fields are written with semicolons.

---

## What a Union Means

A union is not a struct with extra memory tricks.

A struct stores each field separately.
A union shares one storage area across all fields.

That difference matters a lot:

* structs are for records where every field exists at once
* unions are for alternatives where only one interpretation is active at a time

### Good practice

Use a union when the alternatives are mutually exclusive.

```rux
union Number {
    i: int32;
    f: float32;
}
```

### Bad practice

Do not use a union just because it looks compact if the data is actually a record.

```rux
// bad idea: these values are not alternatives
union PersonLike {
    name: char8[];
    age: uint32;
    height: float32;
}
```

If all fields are supposed to be valid together, a struct is the correct choice.

---

## Union Declaration Syntax

The general shape of a union is:

```rux
union Name {
    field1: Type;
    field2: Type;
}
```

### Example

```rux
union Value {
    integer: int32;
    floating: float32;
    pointer: *opaque;
}
```

### Public unions

A union may be marked `pub`.

```rux
pub union ExportedValue {
    a: uint64;
    b: uint64;
}
```

Public visibility controls whether the union is visible outside the defining scope, following the same visibility rules used by the rest of the language.

### Notes

* The parser recognizes `union` declarations as top-level items.
* Union declarations may appear at module level or inside nested modules.
* The current parser does not show a type-parameter list for unions.

---

## Fields

Each union field is declared as:

```rux
name: Type;
```

Example:

```rux
union FlagValue {
    bits: uint32;
    raw: uint32;
}
```

### Field rules

* Field names must be identifiers.
* Each field must have a type.
* Each field ends with a semicolon.
* Field order is preserved in the declaration.

### Good practice

Keep field names descriptive of the active interpretation.

```rux
union PacketData {
    headerBytes: uint8[];
    checksum: uint32;
}
```

### Bad practice

Do not use vague field names like `x`, `y`, `z` unless the meaning is actually obvious.

```rux
union BadNaming {
    x: int32;
    y: float32;
    z: *opaque;
}
```

A reader should be able to tell what each alternative means without decoding the whole codebase.

---

## Field Type Rules

Fields may use any valid Rux type.

```rux
union Storage {
    byte: uint8;
    text: char8[];
    ptr: *opaque;
}
```

### Good practice

Prefer small, explicit types when the goal is a compact representation.

```rux
union SmallValue {
    flag: bool8;
    code: uint8;
}
```

### Bad practice

Do not hide huge or unrelated payloads behind a union unless that is really the intended model.

```rux
union EverythingBagel {
    number: uint64;
    name: char8[];
    nested: SomeHugeStruct;
}
```

That kind of design can become unclear fast if the active alternative is not tracked carefully.

---

## Semantic Behavior

The compiler currently treats a union as a named type during semantic analysis.

The semantic analyzer records the union name in the type table and validates the field list.

From the reviewed implementation, unions are checked for:

* duplicate field names
* valid field type resolution

### Example diagnostic cases

```rux
union Bad {
    value: int32;
    value: float32;
}
```

```rux
union Bad {
    value: UnknownType;
}
```

### Good practice

Keep union field sets small and obvious.

```rux
union ParseResult {
    ok: uint32;
    error: int32;
}
```

That kind of declaration is easy to reason about in both the compiler and the reader's head.

### Bad practice

Do not rely on a union to document meaning by itself.

A union only says the storage is shared. It does not automatically tell the reader which field is active.

If the program needs to know which field is currently valid, that state should usually be stored separately.

---

## Front End and Backend Status

Unions are currently supported in the front end.

The reviewed pipeline shows:

* parser support for `union Name { ... }`
* semantic-analysis support for registering unions as types
* lowering metadata that carries union declarations forward

The reviewed files do not show a dedicated union-specific backend layout or code-generation path.

That means unions should be documented as a parsed and analyzed feature, not as a fully proven backend feature.

### Good practice

Describe the current status honestly.

```rux
union Data {
    ptr: *opaque;
    id: uint64;
}
```

The syntax is real, but the backend story should be treated as implementation-dependent until the union path is explicitly finished.

### Bad practice

Do not claim full runtime support if the lower layers have not been verified yet.

That leads to docs that look polished but become misleading the moment someone tries to use the feature seriously.

---

## Examples

### Simple union

```rux
union Number {
    integer: int32;
    floating: float32;
}
```

### Union with pointers

```rux
union Data {
    ptr: *opaque;
    id: uint64;
}
```

### Public union

```rux
pub union Payload {
    bytes: uint8[];
    count: uint32;
}
```

### Compact enum-like storage

```rux
union TokenData {
    kind: uint32;
    payload: uint64;
}
```

This is a reasonable union shape when the code needs one of several interpretations but does not want a larger record type.

---

## Common Errors

### Missing field type

```rux
union Bad {
    value;
}
```

### Missing semicolon after a field

```rux
union Bad {
    value: int32
}
```

### Duplicate field names

```rux
union Bad {
    value: int32;
    value: float32;
}
```

### Unknown field type

```rux
union Bad {
    value: UnknownType;
}
```

### Bad practice: treating a union like a struct

```rux
union BadModel {
    name: char8[];
    age: uint32;
}
```

If both values are always needed together, this should be a struct instead.

---

## Notes

### Keep the active variant obvious

A union is only safe when the program can tell which field is currently meaningful.

If that information is not stored somewhere, the code becomes easy to misuse.
