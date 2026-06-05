# Struct Declarations

A struct is declared with the `struct` keyword.

```rux
struct Point {
    x: float64;
    y: float64;
}
```

Each field has:

* a name
* a type
* an optional `pub` modifier

## Example

```rux
struct Person {
    pub name: char8[];
    age: uint32;
}
```

## Notes

* Fields are written in declaration order.
* Each field ends with a semicolon.
* Struct declarations may appear at module level or inside nested modules.
