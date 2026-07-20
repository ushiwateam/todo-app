from dataclasses import dataclass, asdict


@dataclass()
class TodoBaseModel:
    def model_dump(self, exclude_unset=False):
        if exclude_unset:
            return {k: v for k, v in asdict(self).items() if v is not None}
        return asdict(self)

@dataclass(slots=True)
class TodoCreateCommand(TodoBaseModel):
    title: str
    description: str | None = None


@dataclass(slots=True)
class TodoUpdateCommand(TodoBaseModel):
    title: str
    description: str | None


@dataclass(slots=True)
class TodoPatchCommand(TodoBaseModel):
    title: str | None
    description: str | None
