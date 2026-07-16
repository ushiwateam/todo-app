from dataclasses import dataclass


@dataclass(slots=True)
class User:
    email: str
    name: str
    id: int | None = None


@dataclass(slots=True)
class NewUser:
    name: str
    email: str
    password: str


@dataclass(slots=True)
class UserCredentials:
    email: str
    password: str
