# Struct Construction

A struct value can be constructed using brace syntax.

```rux
let p = Point { x: 1.0, y: 2.0 };
```

## Explicit construction

```rux
let person = Person {
    name: "Alice",
    age: 30
};
```

## Notes

* Field names are written explicitly in the initializer.
* The initializer order does not need to match the declaration order unless the compiler or front end enforces an order rule.
* The parser supports generic struct initialization syntax.

## Example with generics

```rux
let box = Box<int32> { value: 42 };
```
