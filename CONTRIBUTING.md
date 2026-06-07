# Contributing

Thank you for your interest in contributing to the Rux documentation.

Whether you're fixing a typo, improving an explanation, adding examples, or documenting a new language feature, every contribution is appreciated.

---

## Getting Started

1. Fork the repository.
2. Create a new branch.
3. Make your changes.
4. Open a pull request.

---

## Local Development

To preview the documentation locally, install:

* Python 3.11 or newer
* MkDocs

Start the local development server:

```sh
mkdocs serve
```

Then open the local URL displayed by MkDocs.

---

## Documentation Guidelines

### Keep It Clear

Documentation should prioritize clarity over cleverness.

Prefer:

```text
A union allows multiple fields to share the same storage.
```

Over:

```text
A union exposes alternative views of a memory region through overlapping field definitions.
```

---

### Use Examples

Whenever possible, include examples.

```rux
union Number {
    integer: int32;
    floating: float32;
}
```

Examples are often easier to understand than long explanations.

---

### Keep Pages Focused

Each page should focus on a single topic.

Good:

```text
functions/
structs/
unions/
```

Less ideal:

```text
everything_about_types.md
```

---

### Follow Existing Style

Try to match the style used throughout the documentation:

* Use clear headings.
* Use complete sentences.
* Use fenced code blocks.
* Prefer simple language.

---

## Pull Requests

Before opening a pull request, please:

* Verify that the documentation builds successfully.
* Check for spelling and grammar mistakes.
* Make sure examples are correct.
* Keep changes focused on a specific improvement.

---

## Reporting Issues

If you find incorrect, missing, or unclear documentation, please open an issue describing the problem.
Suggestions for new pages and improvements are welcome.

---

## Thank You

Every contribution helps improve the Rux ecosystem.
Thank you for helping make the documentation better.
