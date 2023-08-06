# cargparse :blue_car:

A lightweight library to parse configuration files using `argparse`.

- Robust type validation with `argparse`
- Supports nested arguments with recursive calls to `argparse`
- No syntax to learn, just use `argparse`!! :rocket:

Currently supports `yaml`/`yml` and `json` files. `ini`, `toml`,
and others are under development.

Contributions welcome! :handshake:

![python](https://img.shields.io/pypi/pyversions/cargparse)
![pypi version](https://img.shields.io/pypi/v/cargparse)
![license](https://img.shields.io/pypi/l/cargparse)
[![code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Installation

```bash
pip install cargparse
```

## Usage

Given  `config.yaml`...

```yaml
text: hello world
decimal: 0.5
boolean: False
```

...your script might look like this...

```python
import argparse
import cargparse

parser = argparse.ArgumentParser()
parser.add_argument('--text', type=str)
parser.add_argument('--decimal', type=float)
parser.add_argument('--boolean', type=lambda x: eval(x))
args = cargparse.YAML(parser=parser, filename='config.yaml')
```

...which returns a `Namespace` object, just like `ArgumentParser.parse_args()`!

```bash
>> args
Namespace(text='hello world', decimal=0.5, boolean=False)
>> args.text
'hello world'
>> type(args.decimal)
<class 'float'>
```

:boom: Nested dictionaries are `Namespace` objects, too!
