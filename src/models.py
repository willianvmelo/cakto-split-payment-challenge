from dataclasses import dataclass
from enum import Enum
from decimal import Decimal
from typing import List, Optional

# Modelo simplificado — no projeto real, usar Django ORM com migrations

class SplitPolicyStatus(str, Enum):
    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    RETIRED = "RETIRED"
    ARCHIVED = "ARCHIVED"

@dataclass
class SplitRule:
    recipient_id: str
    type: str  # 'percentage' or 'fixed'
    value: int  # stored in cents if fixed, or basis points if percentage (e.g., 6500 = 65.00%)
    account_info: Optional[dict] = None

@dataclass
class SplitPolicy:
    id: str
    product_id: str
    version: int
    rules: List[SplitRule]
    status: SplitPolicyStatus
    effective_date: str

# Ledger / execution
@dataclass
class SplitExecutionLine:
    recipient_id: str
    amount_cents: int
    payout_status: str  # PENDING, SUCCESS, FAILED
    transaction_ref: Optional[str] = None

@dataclass
class SplitExecution:
    payment_id: str
    total_amount_cents: int
    currency: str
    lines: List[SplitExecutionLine]
    status: str  # PENDING, COMPLETED, COMPENSATED, FAILED