from dataclasses import dataclass


@dataclass(slots=True)
class UserRegisterCommand:
    name: str
    email: str
    password: str


@dataclass(slots=True)
class UserLoginCommand:
    email: str
    password: str
