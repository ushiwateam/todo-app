from abc import ABC
from typing import Generic, TypeVar, List

TDomain = TypeVar("TDomain")


class IRepository(ABC, Generic[TDomain]):
    def create(self, entity: TDomain) -> TDomain:
        pass

    def update(self, entity: TDomain, data: dict) -> TDomain:
        pass

    def delete(self, entity: TDomain) -> None:
        pass

    def get_by_id(self, entity_id: int) -> TDomain | None:
        pass

    def get_one_or_none(self, *conditions) -> TDomain | None:
        pass

    def get_all(self, *conditions, offset=0, limit=1000) -> List[TDomain] | []:
        pass