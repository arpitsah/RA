#!/usr/bin/env bash
set -euo pipefail
uvicorn services.webhook_service:app --host 0.0.0.0 --port "${WEBHOOK_PORT:-8000}" --reload
