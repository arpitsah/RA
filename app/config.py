from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(slots=True)
class Settings:
    database_url: str = os.getenv(
        "DATABASE_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/portfoliolens"
    )
    supabase_url: str = os.getenv("SUPABASE_URL", "")
    supabase_anon_key: str = os.getenv("SUPABASE_ANON_KEY", "")
    stripe_publishable_key: str = os.getenv("STRIPE_PUBLISHABLE_KEY", "")
    stripe_billing_portal_url: str = os.getenv("STRIPE_BILLING_PORTAL_URL", "")


settings = Settings()
