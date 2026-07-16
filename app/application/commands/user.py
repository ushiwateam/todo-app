from dataclasses import dataclass


@dataclass(slots=True)
class User:
    email: str
    name: str
    id: int | None = None


@dataclass(slots=True)
class UserRegisterCommand:
    name: str
    email: str
    password: str


@dataclass(slots=True)
class UserLoginCommand:
    email: str
    password: str
