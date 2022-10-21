from typing import Optional
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

@dataclass
class Account:
    id: str
    username: str
    balance: int
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_dict(cls, data: dict) -> "Account":
        return cls(
            id=data["id"],
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
            username=data["username"],
            balance=data["balance"],
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "username": self.username,
            "balance": self.balance,
        }

class TransactionTypes(Enum):
    TASK_ASSIGNED = "task_created"
    TASK_COMPLETED = "task_completed"
    PAYMENT = "payment"

@dataclass
class Transaction:
    id: str
    created_at: datetime
    account_id: str
    billing_period_id: int
    type: str
    debit: int
    credit: int
    description: str = ""

    @classmethod
    def from_dict(cls, data: dict) -> "Transaction":
        return cls(
            id=data["id"],
            created_at=datetime.fromisoformat(data["created_at"]),
            account_id=data["account_id"],
            billing_period_id=data["billing_period_id"],
            type=data["type"],
            description=data["description"],
            debit=data["debit"],
            credit=data["credit"],
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "account_id": self.account_id,
            "billing_period_id": self.billing_period_id,
            "type": self.type,
            "description": self.description,
            "debit": self.debit,
            "credit": self.credit,
        }

    def amount(self) -> int:
        return self.debit - self.credit

@dataclass
class BillingPeriod:
    id: str
    account_id: str
    created_at: datetime
    updated_at: datetime
    start_date: datetime
    end_date: Optional[datetime]

    @classmethod
    def from_dict(cls, data: dict) -> "BillingPeriod":
        return cls(
            id=data["id"],
            account_id=data["account_id"],
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
            start_date=datetime.fromisoformat(data["start_date"]),
            end_date=datetime.fromisoformat(data["end_date"]),
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "account_id": self.account_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
        }