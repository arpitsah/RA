from __future__ import annotations

import json

from db.models import SavedReport, User
from db.session import SessionLocal


def save_report_for_user(
    supabase_user_id: str,
    email: str,
    name: str,
    benchmark: str,
    cagr: float,
    sharpe: float,
    metadata: dict,
) -> None:
    with SessionLocal() as session:
        user = session.query(User).filter(User.supabase_user_id == supabase_user_id).one_or_none()
        if user is None:
            user = User(supabase_user_id=supabase_user_id, email=email, tier="pro")
            session.add(user)
            session.flush()

        report = SavedReport(
            user_id=user.id,
            name=name,
            benchmark=benchmark,
            cagr=cagr,
            sharpe=sharpe,
            metadata_json=json.dumps(metadata),
        )
        session.add(report)
        session.commit()


def list_reports_for_user(supabase_user_id: str) -> list[dict]:
    with SessionLocal() as session:
        user = session.query(User).filter(User.supabase_user_id == supabase_user_id).one_or_none()
        if user is None:
            return []
        reports = (
            session.query(SavedReport)
            .filter(SavedReport.user_id == user.id)
            .order_by(SavedReport.created_at.desc())
            .all()
        )
        return [
            {
                "name": r.name,
                "benchmark": r.benchmark,
                "cagr": r.cagr,
                "sharpe": r.sharpe,
                "created_at": r.created_at.isoformat() if r.created_at else "",
            }
            for r in reports
        ]
