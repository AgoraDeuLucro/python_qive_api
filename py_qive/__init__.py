from ._base import QiveCredencialError, auth
from .nfe import nfe
from .nfse import nfse
from .cte import cte
from .cteos import cteos
from .outros import etiquetas, flagerp, mdfe, nfce, upload
from .empresas import empresas, property_
from .financeiro import boletos, comprovantes, invoice, utilities
from .ocr import ocr
from .latam import latam
from .cnpj import cnpj
from .eventos import eventos_lote
from .webhook import webhook

# Alias amigável: "property" é palavra reservada em alguns contextos
property = property_

__all__ = [
    "QiveCredencialError",
    "auth",
    "nfe",
    "nfse",
    "cte",
    "cteos",
    "nfce",
    "mdfe",
    "flagerp",
    "etiquetas",
    "upload",
    "empresas",
    "property_",
    "property",
    "boletos",
    "comprovantes",
    "invoice",
    "utilities",
    "ocr",
    "latam",
    "cnpj",
    "eventos_lote",
    "webhook",
]
