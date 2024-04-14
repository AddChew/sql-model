from uuid import uuid4
from typing import List
from difflib import HtmlDiff
from pydantic import UUID4, BaseModel, Field, computed_field


class BaseModel(BaseModel):
    id: UUID4 = Field(default_factory = uuid4, frozen = True)


class Account(BaseModel):
    acctno: int
    currency: str
    owner_id: UUID4 = Field(default = None)


class Customer(BaseModel):
    name: str
    cif: int
    accounts_: List[Account] = Field(default = [], exclude = True, alias = "accounts", repr = False)
    company_id: UUID4 = None

    @computed_field
    @property
    def accounts(self) -> List[Account]:
        for account in self.accounts_:
            account.owner_id = self.id
        return self.accounts_

    @accounts.setter
    def accounts(self, accounts: List[Account]):
        self.accounts_ = accounts     


class Company(BaseModel):
    cif: int
    regNo: str
    customers_: List[Customer] = Field(default = [], exclude = True, alias = "customers", repr = False)

    @computed_field
    @property
    def customers(self) -> List[Customer]:
        for customer in self.customers_:
            customer.company_id = self.id
        return self.customers_
    
    @customers.setter
    def customers(self, customers: List[Customer]):
        self.customers_ = customers


### Generate JSON
account1 = Account(acctno = 123, currency = "SGD")
account2 = Account(acctno = 456, currency = "USD")

customer1 = Customer(name = "bob", cif = 123, accounts = [account1, account2])
customer2 = Customer(name = "collin", cif = 456)
customer3 = Customer(name = "dolly", cif = 789)

customer2.accounts.append(account1)
customer3.accounts = [account2]

company1 = Company(cif = 1011, regNo = "123D", customers = [customer1, customer2])
company2 = Company(cif = 1213, regNo = "456F")
company3 = Company(cif = 1516, regNo = "789H")

company2.customers.append(customer3)
company3.customers = [customer2]

# print(company1.model_dump())
# print(company1.model_dump_json(indent = 2))
print(company1.model_dump_json(
    indent = 2, 
    exclude = {
        "id": True,
        "customers": {
            "__all__": {
                "id": True,
                "company_id": True,
                "accounts": {
                    "__all__": {"id", "owner_id"}
                }
            }
        }
    })
)

# with open("789.json", "w") as f:
#     f.write(company1.model_dump_json(indent = 2))


### Compare JSON
# html_diff = HtmlDiff().make_file(
#     str(company1.model_dump_json(indent = 2)).split(), 
#     str(company2.model_dump_json(indent = 2)).split()
# )

# with open("diff.html", "w") as f:
#     f.write(html_diff)


### Load JSON
# with open("789.json", "r") as f:
#     company = Company.model_validate_json(f.read())

# print(company)