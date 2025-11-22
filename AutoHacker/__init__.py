"""
Biblioteca para construir IAs de Ciberseguridad (CAI) al nivel de Bug Bounty.
"""


def is_pentestperf_available():
  """Comprobar si el módulo pentestperf está disponible."""

  try:
    from pentestperf.ctf import CTF  # pylint: disable=import-error,import-outside-toplevel,unused-import  # noqa: E501,F401
  except ImportError:
    return False
  return True


def is_caiextensions_report_available():
  """Comprobar si está disponible caiextensions report."""

  try:
    from caiextensions.report.common import get_base_instructions  # pylint: disable=import-error,import-outside-toplevel,unused-import  # noqa: E501,F401
  except ImportError:
    return False
  return True


def is_caiextensions_memory_available():
  """Comprobar si está disponible caiextensions memory."""

  try:
    from caiextensions.memory import is_memory_installed  # pylint: disable=import-error,import-outside-toplevel,unused-import  # noqa: E501,F401
  except ImportError:
    return False
  return True


def is_caiextensions_platform_available():
  """Comprobar si está disponible caiextensions-platform."""

  try:
    from caiextensions.platform.base import platform_manager  # pylint: disable=import-error,import-outside-toplevel,unused-import  # noqa: E501,F401
  except ImportError:
    return False
  return True
