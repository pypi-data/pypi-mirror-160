<div align=center>
  <br>
  <img width=60% src='https://raw.githubusercontent.com/oruwmztbnz4q/sayori/main/images/sayori.svg'></img>
  <br>
</div>


# Sayori

Sayori is a tiny library for composing [pure functions](https://en.wikipedia.org/wiki/Pure_function) using pipeline notation. If `f` and `g` are functions then `f | g` is a function such that `(f | g)(x) = g(f(x))`.


## Installation

```sh
pip install sayori
```


## Usage

Sayori exports a simple decorator called `Composable` which implements the pipe operator. It can be used as follows:

```py
from sayori import Composable
```

Create two composable functions...

```py
f = Composable(lambda x: x + 1)

g = Composable(lambda x: x * 2)
```

Compose them...

```py
h = f | g
```

Apply the composite...

```py
h(2)  # returns 6
```
