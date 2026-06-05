# Fields

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