"""Compatibility shim for importing the AutoHacker package as ``cai``.

This module allows existing code that expects a ``cai`` package to resolve
modules that live at the repository root (e.g., ``sdk``, ``agents``,
``util``). It works by extending the package search path to include the
project root so that subpackages are discovered without modifying import
call sites.
"""

from __future__ import annotations

import sys
from pathlib import Path

_here = Path(__file__).resolve().parent
_repo_root = _here.parent

if str(_repo_root) not in sys.path:
  sys.path.insert(0, str(_repo_root))

__path__ = [str(_here), str(_repo_root)]

