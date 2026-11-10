from ._base import auth


class boletos(auth):
    """Recursos de Boletos Bancários da API Qive (Arquivei)."""

    def listar(self, **params):
        """GET /v1/bank-billet — lista boletos bancários."""
        return self.request(
            "GET", f"{self.base_url}/v1/bank-billet", params=params or None
        )

    def buscar_v2(self, body):
        """POST /v2/bank-billet/search — busca boletos bancários v2."""
        return self.request(
            "POST", f"{self.base_url}/v2/bank-billet/search", data=body
        )

    def pdf(self, owner, digitable_line, **params):
        """GET /v1/bank-billet/{owner}/{digitableLine}/pdf — PDF do boleto."""
        return self.request(
            "GET",
            f"{self.base_url}/v1/bank-billet/{owner}/{digitable_line}/pdf",
            params=params or None,
        )


class comprovantes(auth):
    """Recursos de Comprovantes da API Qive (Arquivei)."""

    def listar(self, body):
        """POST /v1/receipts/list — busca de comprovantes."""
        return self.request(
            "POST", f"{self.base_url}/v1/receipts/list", data=body
        )


class invoice(auth):
    """Recursos de Invoice da API Qive (Arquivei)."""

    def buscar(self, **params):
        """GET /v1/invoice/search — busca de invoices."""
        return self.request(
            "GET", f"{self.base_url}/v1/invoice/search", params=params or None
        )

    def obter(self, invoice_id, **params):
        """GET /v1/invoice/{id} — retorna invoice por id."""
        return self.request(
            "GET",
            f"{self.base_url}/v1/invoice/{invoice_id}",
            params=params or None,
        )

    def pdf(self, invoice_id, **params):
        """GET /v1/invoice/{id}/pdf — retorna PDF de invoice."""
        return self.request(
            "GET",
            f"{self.base_url}/v1/invoice/{invoice_id}/pdf",
            params=params or None,
        )


class utilities(auth):
    """Recursos de Utilities da API Qive (Arquivei)."""

    def buscar(self, **params):
        """GET /v1/utility/search — busca de utilities."""
        return self.request(
            "GET", f"{self.base_url}/v1/utility/search", params=params or None
        )

    def obter(self, document_type, utility_id, **params):
        """GET /v1/utility/{document_type}/{id} — retorna utility por id."""
        return self.request(
            "GET",
            f"{self.base_url}/v1/utility/{document_type}/{utility_id}",
            params=params or None,
        )

    def pdf(self, document_type, utility_id, **params):
        """GET /v1/utility/{document_type}/{id}/pdf — PDF de utility."""
        return self.request(
            "GET",
            f"{self.base_url}/v1/utility/{document_type}/{utility_id}/pdf",
            params=params or None,
        )

    def xml(self, document_type, utility_id, **params):
        """GET /v1/utility/{document_type}/{id}/xml — XML de utility."""
        return self.request(
            "GET",
            f"{self.base_url}/v1/utility/{document_type}/{utility_id}/xml",
            params=params or None,
        )
