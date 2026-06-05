# Common Errors

## Missing field type

```rux
struct Bad {
    x;
}
```

## Missing semicolon after a field

```rux
struct Bad {
    x: int32
}
```

## Invalid construction field

```rux
let p = Point { a: 1.0, y: 2.0 };
```

## Duplicate field names

```rux
struct Bad {
    x: int32;
    x: int32;
}
```

## Pattern mismatch

```rux
let Point { x, y, z } = p;
```

when `Point` does not have a `z` field.
