# Methods and `extend`

Methods can be attached to structs with `extend`.

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

## Instance methods

Instance methods take `self` as their first parameter.

```rux
func Length(self) -> float64 {
    return Sqrt(self.x * self.x + self.y * self.y + self.z * self.z);
}
```

## Static methods

A method without `self` behaves like an associated function.

```rux
extend Vector {
    func New(x: float64, y: float64, z: float64) -> Vector {
        return Vector { x: x, y: y, z: z };
    }
}
```

Called as:

```rux
let v = Vector::New(1.0, 2.0, 3.0);
```

## Operator methods

A struct may define operator methods inside `extend`.

```rux
extend Vector {
    func +(self, other: Vector) -> Vector {
        return Vector {
            x: self.x + other.x,
            y: self.y + other.y,
            z: self.z + other.z
        };
    }
}
```

These are resolved by the compiler like ordinary methods, but using operator syntax.
