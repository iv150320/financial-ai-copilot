"""
Value objects — immutable, self-validating primitives of the domain.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from enum import Enum


class Currency(str, Enum):
    """Supported ISO-4217 currencies."""

    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    JPY = "JPY"
    CHF = "CHF"
    RUB = "RUB"
    CNY = "CNY"


class ReportType(str, Enum):
    """Supported financial report types."""

    BALANCE_SHEET = "balance_sheet"
    INCOME_STATEMENT = "income_statement"
    CASH_FLOW = "cash_flow"
    FINANCIAL_RATIOS = "financial_ratios"
    CUSTOM_ANALYSIS = "custom_analysis"


class AnalysisStatus(str, Enum):
    """Lifecycle status for an analysis request."""

    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class RiskLevel(str, Enum):
    """Qualitative risk classification."""

    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass(frozen=True)
class Money:
    """An amount in a specific currency."""

    amount: Decimal
    currency: Currency

    def __post_init__(self) -> None:
        if self.amount < Decimal("0"):
            raise ValueError("Money amount cannot be negative")

    def __add__(self, other: Money) -> Money:
        if other.currency != self.currency:
            raise ValueError("Cannot add different currencies")
        return Money(self.amount + other.amount, self.currency)

    def __mul__(self, factor: Decimal) -> Money:
        return Money(self.amount * factor, self.currency)


@dataclass(frozen=True)
class FinancialRatio:
    """A single computed financial ratio."""

    name: str
    value: float
    benchmark: float | None = None
    interpretation: str = ""


@dataclass(frozen=True)
class DateRange:
    """Inclusive date range for financial queries."""

    start: str  # ISO-8601 date
    end: str  # ISO-8601 date
