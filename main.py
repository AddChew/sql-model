from uuid import uuid4
from typing import List
from pydantic import UUID4, BaseModel, Field, model_serializer


# Proposed method is to have two sets of models, one set with id fields, another set without
# Set with id fields is used for actual prod
# Set without id fields is used for testing evaluation purpose


class IDMixin(BaseModel):
    id: UUID4 = Field(default_factory = uuid4)


class AccountBase(BaseModel):
    acctno: int
    currency: str


class Account(AccountBase, IDMixin):
    owner_id: UUID4 = None


class CustomerBase(BaseModel):
    name: str
    cif: int
    accounts: List[AccountBase]


class Customer(CustomerBase, IDMixin):
    accounts: List[Account]
    company_id: UUID4 = None

    @model_serializer
    def serialize(self):
        for account in self.accounts:
            account.owner_id = self.id
        return self.__dict__
    

class CompanyBase(BaseModel):
    cif: int
    regNo: str
    customers: List[CustomerBase]


class Company(CompanyBase, IDMixin):
    customers: List[Customer]

    @model_serializer
    def serialize(self):
        for customer in self.customers:
            customer.company_id = self.id
        return self.__dict__


account1 = Account(acctno = 123, currency = "SGD")
account2 = Account(acctno = 456, currency = "USD")

customer = Customer(name = "bob", cif = 123, accounts = [account1, account2])
# customer.accounts = [account1, account2]
# customer.accounts.append(account2)

company = Company(cif = 789, regNo = "123D", customers = [customer])
# print(company.model_dump())
print(company.model_dump_json(indent = 2))

# with open("789.json", "w") as f:
#     f.write(company.model_dump_json(indent = 2))