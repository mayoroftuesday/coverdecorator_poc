# Covers decorator and plugin

Normally, lines in source files are marked as "covered" by coverage.py as long as they are executed. However, a
unit test is normally only intended to test one function, not other functions called further down the stack.

Example:

```
def a():
   b()
   return 1

def b():
   return 2

def test_a():
   assert a() == 1

```

In this situation, `test_a` is only intended to test `a`, but coverage.py will also mark `b` as covered code.

This new plugin will only count lines that are explicitly marked as being covered. For example:

```
@covers('a')
def test_a():
   assert a() == 1
```

Now coverage will only report lines inside `a` as being executed, and nothing in `b`.

## Requires

- coverage

## To run

```
coverage run main.py
coverage report
coverage html
```

You should see in the report that only lines in `foo` are marked as covered.
