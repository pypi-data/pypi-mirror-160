# ID Schema

## How to install it?

You can install *ID Schema* from this Github repository with `python3 setup.py install`,
or just install it directly from pypi with `pip3 install id-schema`.

## What is it?

*ID Schema* allows you to define your custom Schema, how an identifier string should look like. Each identifier string consists of one or more *components*, which are then concatenated into one large identifier string.
Currently there are three components.

## Components


### RandomGroup

The `RandomGroup` component allows to generate a random sequence of a predefined alphabet
with a predefined length range. A length range can have a minimum length and a maximum length. Valid length ranges are for example:

```python
LengthRange(1) # always maps to 1
LengthRange(1, max_length=1) # always maps to 1
LengthRange(1, 3) # length range between 1 and 3, interval [1,3]
LengthRange(5,10) # interval [5,10]
LengthRange(10, max_length=1) # INVALID RANGE! , because min > max
```

If you only want the resulting random string sequence to contain only unique elements,
you can use the keyword argument `unique=True`. The default is `unique=False`.

Here are some examples on how to use the `RandomGroup` component.
```python
RandomGroup(alphabet="abcd", length=1)
RandomGroup(alphabet="abcd", length=(1,3))
RandomGroup(alphabet="abcd", length=LengthRange(1,3))
RandomGroup(alphabet="abcd", length=(1,3), unique=True)
RandomGroup(alphabet="ab", length=(1,3), weights=[0.75,0.25]) # 'a' will occur 3/4 as much as 'b'
```

### ExactLiteral

The `ExactLiteral` component allows to generate an exact literal sequence. The usage is very simple.

```python
ExactLiteral("-") # will always generate '-'
ExactLiteral("abcd") # will always generate 'abcd'
```


### OneOf

The `OneOf` component allows to generate exactly one other component based on a component subset. Specifying a pure string automatically transforms it to an `ExactLiteral` for you.

```python
OneOf(components=(
	"gmail.com",
	"yahoo.com",
	"hotmail.com"
))
OneOf(components=(
	RandomGroup(alphabet="abcd", length=LengthRange(1,3)),
	RandomGroup(alphabet="efgh", length=LengthRange(1,3)),
), weights=(0.75, 0.25))
```

## ID Schema

To actually use these components, you have to create an `IDSchema` subclass. Just define your components under the `Components` class attribute and you are done.

```python
from id_schema import OneOf, IDSchema, RandomGroup, ExactLiteral
import string

class EmailSchema(IDSchema):
	Components = (
		RandomGroup(alphabet=string.ascii_letter, length=(1,20)),
		ExactLiteral("@"),
		OneOf(components=(
			"gmail.com",
			"yahoo.com",
			"hotmail.com"
		))
	)

class SerialNumberSchema(IDSchema):
	Components = (
		RandomGroup(alphabet=string.ascii_letter, length=5),
		ExactLiteral("-"),
		RandomGroup(alphabet=string.ascii_letter, length=(5,10)),
		ExactLiteral("-"),
		RandomGroup(alphabet=string.ascii_letter, length=5),
	)
```

`IDSchema` exposes various functions:

- `generate_one()` : generate one string from the Schema
- `generate_n(n)`: generate n strings from the same Schema
- `generate_n_unique(n, max_retry=20)` : generate n unique strings from the same Schema. Fail after `max_retry` attempts.
- `validate(string)`: validate if a given string matches the Schema (note that `weights` are not validated)
