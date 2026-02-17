#!/usr/bin/env bash
set -euo pipefail
streamlit run app/Home.py --server.port "${PORT:-8501}" --server.address 0.0.0.0
