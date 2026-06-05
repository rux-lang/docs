# Examples

## Simple struct

```rux
struct Point {
    x: float64;
    y: float64;
}
```

## Struct with visibility

```rux
pub struct Config {
    pub enabled: bool;
    pub port: uint32;
}
```

## Generic struct

```rux
struct Box<T> {
    value: T;
}
```

## Nested struct

```rux
struct Rectangle {
    topLeft: Point;
    bottomRight: Point;
}
```

## Struct construction

```rux
let p = Point { x: 1.0, y: 2.0 };
```

## Struct pattern

```rux
let Point { x, y } = p;
```

## Method implementation

```rux
extend Point {
    func Length(self) -> float64 {
        return Sqrt(self.x * self.x + self.y * self.y);
    }
}
```