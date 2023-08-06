# Convertible

Value-to-value conversion in Python.

# Usage

## Convertible

First, let's create a model for conversion. The model can be any class.

For convenience, let's take `dataclass`:

```python
from dataclasses import dataclass
from convertible import Convertible

@dataclass
class User(Convertible):
    name: str
    age: int
```

Now `User` has conversion methods `try_from` and `try_into`. But we haven't
implemented any converter. Let's do this.

## `From` Converter

```python
from typing import Tuple
from convertible import From

class UserFromTuple(From[tuple[str, int], User]):
    def try_from(self, value: tuple[str, int]) -> User:
        return User(name=value[0], age=value[1])
```

Now we can instantiate `User` from `tuple`:

```python
user = User.try_from(("John", 23))
assert user.age == 23
```

## `Into` Converter

We can convert user into another type. Let's define the converter:

```python
# note that User is now the first parameter:
class UserIntoDict(From[User, dict]):
    def try_from(self, user: User) -> dict:
        return {
            "username": user.name,
            "age": user.age
        }

data = user.try_into(dict)
assert data["username"] == user.name
```

## Cross conversion

Implementing `From` for two `Convertible` classes automatically provides the
second `Convertible` with an implementation for `try_into`:

```python
@dataclass
class Admin(Convertible):
    name: str


class AdminFromUser(From[User, Admin]):
    def try_from(self, user: User) -> Admin:
        return Admin(name=user.name)


# these are equivalent
assert user.try_into(Admin) == Admin.try_from(user)
```

## Manual converter registration

You may need to define converters for types that are not `Convertible`.
This can be done using the `register_converter` function:

```python
class IntFromString:
    def try_from(self, value: str) -> int:
        return int(value)

From[int, str].register_converter(IntFromString)

value = From[int, str].try_from("123")
assert value == 123
```

