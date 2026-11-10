from ._base import auth


class ocr(auth):
    """Recursos de OCR da API Qive (Arquivei)."""

    def upload(self, body=None, files=None):
        """POST /v1/ocr/upload — upload de PDF para OCR."""
        return self.request(
            "POST",
            f"{self.base_url}/v1/ocr/upload",
            data=body,
            files=files,
        )

    def status(self, **params):
        """GET /v1/ocr/status — status do processo de OCR."""
        return self.request(
            "GET", f"{self.base_url}/v1/ocr/status", params=params or None
        )
