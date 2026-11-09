from datetime import date, datetime
from decimal import Decimal
from sqlalchemy import Date, DateTime, ForeignKey, Integer, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .db import Base

class Transaction(Base):
    __tablename__ = "transactions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    transaction_date: Mapped[date] = mapped_column(Date, nullable=False)
    vendor_name: Mapped[str] = mapped_column(String(120), nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    payment_reference: Mapped[str] = mapped_column(String(120), nullable=False)
    category: Mapped[str | None] = mapped_column(String(80), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    audit_results: Mapped[list["AuditResult"]] = relationship(back_populates="transaction", cascade="all, delete-orphan")

class AuditResult(Base):
    __tablename__ = "audit_results"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    transaction_id: Mapped[int] = mapped_column(ForeignKey("transactions.id", ondelete="CASCADE"), nullable=False)
    risk_score: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False)
    anomaly_type: Mapped[str] = mapped_column(String(120), nullable=False)
    audit_status: Mapped[str] = mapped_column(String(40), default="Needs review")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    transaction: Mapped[Transaction] = relationship(back_populates="audit_results")
