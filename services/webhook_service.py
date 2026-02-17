from __future__ import annotations

import os

import stripe
from fastapi import FastAPI, Header, HTTPException, Request

app = FastAPI(title="PortfolioLens Webhooks")

stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "")
webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET", "")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/webhooks/stripe")
async def stripe_webhook(request: Request, stripe_signature: str = Header(default="")) -> dict[str, str]:
    payload = await request.body()

    try:
        event = stripe.Webhook.construct_event(payload=payload, sig_header=stripe_signature, secret=webhook_secret)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=400, detail=f"Invalid webhook signature: {exc}") from exc

    event_type = event["type"]
    if event_type == "checkout.session.completed":
        # TODO: upsert subscription tier in Postgres
        pass
    elif event_type == "customer.subscription.deleted":
        # TODO: downgrade user tier in Postgres
        pass

    return {"received": "true", "event": event_type}
