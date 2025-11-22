"""Compatibility shim for importing the AutoHacker package as ``cai``.

This module allows existing code that expects a ``cai`` package to resolve
modules that live at the repository root (e.g., ``sdk``, ``agents``,
``util``). It works by extending the package search path to include the
project root so that subpackages are discovered without modifying import
call sites.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

_here = Path(__file__).resolve().parent
_repo_root = _here.parent

# Provide a safe fallback API key to prevent initialization errors when the
# environment variable is missing. This avoids crashes when running examples
# or the CLI with local-only model providers that do not require a real
# OpenAI key.
os.environ.setdefault("OPENAI_API_KEY", "sk-placeholder-key-for-local-models")

if str(_repo_root) not in sys.path:
  sys.path.insert(0, str(_repo_root))

# Export compatibility helpers from the repository root so callers can do
# ``from cai import is_pentestperf_available`` regardless of whether they import
# through the compatibility shim or the root package directly.
try:  # pragma: no cover - defensive import to preserve CLI startup
  from __init__ import (  # type: ignore  # pylint: disable=import-error
      is_caiextensions_memory_available,
      is_caiextensions_platform_available,
      is_caiextensions_report_available,
      is_pentestperf_available,
  )
except Exception:  # pragma: no cover - fallback if unexpected import issue
  def is_pentestperf_available() -> bool:
    return False

  def is_caiextensions_report_available() -> bool:
    return False

  def is_caiextensions_memory_available() -> bool:
    return False

  def is_caiextensions_platform_available() -> bool:
    return False

__all__ = [
  "is_pentestperf_available",
  "is_caiextensions_report_available",
  "is_caiextensions_memory_available",
  "is_caiextensions_platform_available",
]

__path__ = [str(_here), str(_repo_root)]

