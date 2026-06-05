# Interface Implementations

The parser supports `extend` in interface-related forms as well.

```rux
extend Vector : Display {
    func ToString(self) -> String {
        return "Vector";
    }
}
```

or:

```rux
extend Display for Vector {
    func ToString(self) -> String {
        return "Vector";
    }
}
```

This allows a struct to implement an interface by attaching the required methods.

### Notes

* The compiler tracks methods by type.
* Interface implementation is associated with the concrete type name.
* Interface method tables are used later during lowering and backend generation.

---

## Visibility

Structs may be public.

```rux
pub struct Point {
    pub x: float64;
    pub y: float64;
}
```

### Notes

* Public visibility can apply to the struct itself.
* Public visibility can also apply to individual fields.
* Visibility is tracked by the parser and semantic analyzer.
