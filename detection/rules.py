from collections import Counter
from decimal import Decimal
from sqlalchemy import select
from sqlalchemy.orm import Session
from database.models import Transaction, AuditResult

# Educational starter rules only. Tune thresholds with a finance/audit professional.
def run_rule_audit(db: Session):
    rows = db.scalars(select(Transaction).order_by(Transaction.id)).all()
    reference_counts = Counter(row.payment_reference for row in rows)
    created = []

    for row in rows:
        reasons = []
        score = 0
        if reference_counts[row.payment_reference] > 1:
            reasons.append("Repeated payment reference")
            score += 70
        if row.amount >= Decimal("100000.00"):
            reasons.append("High-value transaction (review threshold)")
            score += 30
        if not reasons:
            continue

        result = AuditResult(
            transaction_id=row.id,
            risk_score=min(score, 100),
            anomaly_type="; ".join(reasons),
            audit_status="Needs human review",
        )
        db.add(result)
        created.append(result)

    db.commit()
    return created
