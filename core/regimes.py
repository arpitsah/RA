"""Scaffold for macro regime classification models (HMM/GMM/MSR).

Future versions can expose a standardized `classify_regime` API used by the recommendation engine.
"""

from __future__ import annotations

import pandas as pd


def classify_regime(features: pd.DataFrame) -> str:
    _ = features
    return "unknown"
