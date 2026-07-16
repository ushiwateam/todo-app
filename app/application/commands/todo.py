from dataclasses import dataclass, asdict


@dataclass(slots=True)
class Todo:
    title: str
    description: str
    user_id: int
    id: int | None = None

    def to_json(self, exclude_unset=False):
        if exclude_unset:
            return {k: v for k, v in asdict(self).items() if v is not None}
        return asdict(self)
