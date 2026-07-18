from dataclasses import dataclass

@dataclass(slots=True)
class User:
    email: str
    name: str
    password: str
    id: int | None = None