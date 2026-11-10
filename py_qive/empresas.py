from ._base import auth


class empresas(auth):
    """Recursos de Empresas e Certificados da API Qive (Arquivei)."""

    def listar(self, **params):
        """GET /v1/company — lista empresas da conta."""
        return self.request(
            "GET", f"{self.base_url}/v1/company", params=params or None
        )

    def upload_certificado(self, body=None, files=None):
        """POST /v1/certificate/upload — upload de certificado digital."""
        return self.request(
            "POST",
            f"{self.base_url}/v1/certificate/upload",
            data=body,
            files=files,
        )


class property_(auth):
    """Recursos de Property da API Qive (Arquivei)."""

    def listar(self, **params):
        """GET /v1/property — lista de properties."""
        return self.request(
            "GET", f"{self.base_url}/v1/property", params=params or None
        )
