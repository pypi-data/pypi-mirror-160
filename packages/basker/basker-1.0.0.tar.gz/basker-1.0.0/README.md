# Basker

Basker is a simple wrapper around `multiprocessing.Process`,
giving users a nicer API as well as task results.

I wrote Basker for educational purposes, but it is also suited
for actual use. If you are interested in the story behind Basker
you can read it on my [blog](https://blog.walpot.dev/basker)

## Installation

```shell
$ pip install basker
```

## Example

In the following snippet, calling `example` starts a background process and
returns a `unbocked.Result` instance. This result can be retrieved with
`unbocked.Result.get`

```python
import basker

@basker.task
def example():
    return 5 * 5

if __name__ == "__main__":
    result = example()
    print(result.get(timeout=1))
```
