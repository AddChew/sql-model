from uuid import uuid4
from typing import List
from pydantic import UUID4, BaseModel, Field, model_validator


class Account(BaseModel):
    id: UUID4 = Field(default_factory = uuid4)
    acctno: int
    currency: str
    owner_id: UUID4 = None


class Person(BaseModel):
    id: UUID4 = Field(default_factory = uuid4)
    name: str
    cif: int
    accounts: List[Account] = []

    @model_validator(mode = "after")
    def add_owner_id(self) -> "Person":
        for account in self.accounts:
            account.owner_id = self.id
        return self

account = Account(acctno = 123, currency = "SGD")
owner = Person(name = "bob", cif = 123, accounts = [account])

print(owner.model_dump_json())