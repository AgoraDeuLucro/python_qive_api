from ._base import auth


class nfce(auth):
    """Recursos de NFC-e da API Qive (Arquivei)."""

    def listar(self, **params):
        """GET /v1/nfce/emitted — busca de NFCes emitidas."""
        return self.request(
            "GET", f"{self.base_url}/v1/nfce/emitted", params=params or None
        )


class mdfe(auth):
    """Recursos de MDF-e da API Qive (Arquivei)."""

    def listar(self, filters=None, fields=None, limite=500, paginator=""):
        """POST /v1/dfe/mdfe — busca MDFes."""
        body = {
            "Filters": filters or {},
            "Fields": fields or [],
            "Limit": limite,
        }
        if paginator:
            body["Paginator"] = paginator
        return self.request("POST", f"{self.base_url}/v1/dfe/mdfe", data=body)


class flagerp(auth):
    """Recursos de FlagErp da API Qive (Arquivei)."""

    def incluir(self, body):
        """POST /v1/dfe/flagerp — inclui FlagErp em documentos."""
        return self.request("POST", f"{self.base_url}/v1/dfe/flagerp", data=body)


class etiquetas(auth):
    """Recursos de Etiquetas (Tags) da API Qive (Arquivei)."""

    def listar_conta(self, body=None):
        """POST /v1/account/tags/list — lista etiquetas da conta."""
        return self.request(
            "POST", f"{self.base_url}/v1/account/tags/list", data=body or {}
        )

    def listar_dfe(self, body):
        """POST /v1/dfe/tags/list — lista etiquetas de um DFe."""
        return self.request("POST", f"{self.base_url}/v1/dfe/tags/list", data=body)

    def atualizar_dfe(self, body):
        """POST /v1/dfe/tags/update — altera etiquetas de um DFe."""
        return self.request(
            "POST", f"{self.base_url}/v1/dfe/tags/update", data=body
        )


class upload(auth):
    """Upload genérico de DFes da API Qive (Arquivei)."""

    def enviar(self, body):
        """POST /v1/dfe/upload — upload de DFes."""
        return self.request("POST", f"{self.base_url}/v1/dfe/upload", data=body)
