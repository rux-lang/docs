# Struct Patterns

Structs can be destructured in pattern position.

```rux
let Point { x, y } = p;
```

Or with explicit field patterns:

```rux
let Point { x: px, y: py } = p;
```

Struct patterns are used in bindings and match arms.

## Example in a `match`

```rux
match value {
    Point { x: 0, y } => Print(y),
    _ => Print(0)
}
```


### Notes

* Struct patterns must match the struct type shape.
* Field patterns are parsed separately from struct expressions.
* Pattern syntax is part of the parser’s supported feature set, not an afterthought.
