from __future__ import annotations

import streamlit as st

from app.auth import auth_widget, require_login
from app.config import settings

st.set_page_config(page_title="Billing", layout="wide")
auth_widget()
st.title("Billing")

if not require_login():
    st.stop()

st.markdown("### Stripe subscription management")
st.write("Use Stripe Checkout + Billing Portal URLs from your backend.")

if settings.stripe_billing_portal_url:
    st.link_button("Open Billing Portal", settings.stripe_billing_portal_url)
else:
    st.warning("Set STRIPE_BILLING_PORTAL_URL in environment.")
