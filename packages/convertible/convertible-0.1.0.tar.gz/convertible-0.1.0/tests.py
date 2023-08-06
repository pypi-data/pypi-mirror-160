import unittest
from dataclasses import dataclass
from typing import NamedTuple, NewType, Annotated, Literal

from convertible import From, Convertible


@dataclass
class User(Convertible):
    age: int
    name: str
    is_active: bool


class _AdminTuple(NamedTuple):
    name: str
    permissions: int


class Admin(Convertible, _AdminTuple):
    pass


# impl From<Test> for Dict


class UserFromDict(From[dict, User]):
    def try_from(self, value: dict) -> User:
        return User(**value)


class UserIntoDict(From[User, dict]):
    def try_from(self, value: User) -> dict:
        return value.__dict__


class UserFromString(From[str, User]):
    def try_from(self, value: str) -> User:
        return User(
            age=23,
            name=value,
            is_active=True,
        )


PublicId = NewType("PublicId", str)
# PublicId = Annotated[str, Literal["PublicId"]]


class UserFromPublicId(From[PublicId, User]):
    def try_from(self, value: PublicId) -> User:
        return User(
            age=32,
            name=value.capitalize(),
            is_active=False,
        )


class AdminFromUser(From[User, Admin]):
    def try_from(self, value: User) -> Admin:
        return Admin(name=value.name, permissions=10011)


class UserFromAdmin(From[Admin, User]):
    def try_from(self, value: Admin) -> User:
        return User(name=value.name, age=22, is_active=True)


class TestConversion(unittest.TestCase):
    def test(self):
        data = {"age": 34, "name": "foo", "is_active": True}
        obj = User.try_from(data)
        assert data == obj.try_into(dict)

    def test_from_string(self):
        obj = User.try_from("foo")
        data = obj.try_into(dict)
        assert obj.is_active == data["is_active"] == True

    def test_from_public_id(self):
        obj = User.try_from("bar", PublicId)
        data = obj.try_into(dict)
        assert obj.is_active == data["is_active"] == False

    def test_cross_conversion(self):
        user_1 = User.try_from("foo")
        admin_1 = user_1.try_into(Admin)
        admin_2 = Admin.try_from(user_1)
        assert admin_1.name == admin_2.name
        user_2 = admin_1.try_into(User)
        assert user_2.name == admin_2.name

    def test_conversion(self):
        user = From[PublicId, User].try_from("bar")
        assert not user.is_active
        admin = From[User, Admin].try_from(user)
        assert admin.name == "Bar"

    def test_manual_register(self):
        class IntFromString:
            def try_from(self, value):
                return int(value)

        From[str, int].register_converter(IntFromString)

        value = From[str, int].try_from("123")
        assert value == 123


if __name__ == "__main__":
    unittest.main()
