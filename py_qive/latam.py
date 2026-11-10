from ._base import auth


class latam(auth):
    """Recursos LATAM da API Qive (Arquivei)."""

    def upload(self, body=None, files=None):
        """POST /v1/latam/upload — upload de docs LATAM."""
        return self.request(
            "POST",
            f"{self.base_url}/v1/latam/upload",
            data=body,
            files=files,
        )

    def buscar(self, **params):
        """GET /v1/latam/search — busca de docs LATAM."""
        return self.request(
            "GET", f"{self.base_url}/v1/latam/search", params=params or None
        )

    def obter(self, doc_id, **params):
        """GET /v1/latam/{id} — retorna doc LATAM por id."""
        return self.request(
            "GET", f"{self.base_url}/v1/latam/{doc_id}", params=params or None
        )

    def xml(self, doc_id, **params):
        """GET /v1/latam/{id}/xml — retorna XML de doc LATAM."""
        return self.request(
            "GET",
            f"{self.base_url}/v1/latam/{doc_id}/xml",
            params=params or None,
        )

    def cancelar(self, doc_id, body=None):
        """POST /v1/latam/{id}/cancel — cancelamento de doc LATAM."""
        return self.request(
            "POST",
            f"{self.base_url}/v1/latam/{doc_id}/cancel",
            data=body or {},
        )
