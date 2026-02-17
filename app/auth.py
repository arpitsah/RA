from __future__ import annotations

import streamlit as st

from app.config import settings


def ensure_auth_state() -> None:
    st.session_state.setdefault("user", None)
    st.session_state.setdefault("tier", "free")


def auth_widget() -> None:
    ensure_auth_state()
    with st.sidebar:
        st.subheader("Account")
        if st.session_state["user"]:
            st.success(f"Signed in as {st.session_state['user']}")
            if st.button("Sign out"):
                st.session_state["user"] = None
                st.session_state["tier"] = "free"
        else:
            st.caption("Supabase Auth integration scaffold")
            email = st.text_input("Email", key="login_email")
            if st.button("Demo sign in") and email:
                st.session_state["user"] = email
                st.session_state["tier"] = "pro"
            st.caption("Wire Supabase magic link/OAuth in production.")


def require_login() -> bool:
    ensure_auth_state()
    if not st.session_state["user"]:
        st.warning("Login required for this page.")
        st.info(f"Configure Supabase via SUPABASE_URL ({bool(settings.supabase_url)} configured).")
        return False
    return True


def require_tier(required: str = "pro") -> bool:
    tiers = {"free": 0, "pro": 1, "team": 2}
    current = st.session_state.get("tier", "free")
    if tiers.get(current, 0) < tiers.get(required, 1):
        st.error(f"This feature requires {required.title()} tier.")
        return False
    return True
