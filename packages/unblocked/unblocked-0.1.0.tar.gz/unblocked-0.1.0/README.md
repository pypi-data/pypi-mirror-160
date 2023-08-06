# Unblocked

Unblocked is a simple wrapper around `multiprocessing.Process`,
giving users a nicer API as well as task results.

I wrote Unblocked for educational purposes, but it is also suited
for actual use. If you are interested in the story behind Unblocked
you can read it on my [blog](https://blog.walpot.dev/unblocked)

## Installation

```shell
$ pip install unblocked
```

## Example

In the following snippet, calling `example` starts a background process and
returns an `unblocked.Result` instance. This result can be retrieved with
`unblocked.Result.get`

```python
import unblocked

@unblocked.task
def example():
    return 5 * 5

if __name__ == "__main__":
    result = example()
    print(result.get(timeout=1))
```
