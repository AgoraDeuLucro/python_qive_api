"""Compatibilidade: reexporta auth, nfe e QiveCredencialError.

Prefira importar diretamente de ``py_qive``::

    from py_qive import auth, nfe, QiveCredencialError
"""

from ._base import QiveCredencialError, auth
from .nfe import nfe

__all__ = ["QiveCredencialError", "auth", "nfe"]
