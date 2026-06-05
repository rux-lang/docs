# Nested Structs and Named Types

Struct fields may themselves be named types.

```rux
struct Address {
    city: char8[];
    zip: uint32;
}

struct Person {
    name: char8[];
    address: Address;
}
```

The compiler resolves the named field type during semantic analysis and uses the resolved type during layout computation.

## Notes

* Named fields are not flattened automatically.
* The struct contains the nested type as a field.
* Layout is computed recursively through known named types.
