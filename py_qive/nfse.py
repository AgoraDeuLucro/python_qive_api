from ._base import auth


class nfse(auth):
    """Recursos de NFS-e da API Qive (Arquivei)."""

    def listar(self, filters=None, fields=None, limite=500, paginator=""):
        """POST /v1/dfe/nfse — busca NFSes com filtros."""
        body = {
            "Filters": filters or {},
            "Fields": fields or [],
            "Limit": limite,
        }
        if paginator:
            body["Paginator"] = paginator
        return self.request("POST", f"{self.base_url}/v1/dfe/nfse", data=body)

    def listar_v1(self, role="received", cursor="0", limite=50, **kwargs):
        """GET /v1/nfse/{role} — busca NFSes por papel (cursor)."""
        params = [("cursor", cursor or "0"), ("limit", limite)]
        for cnpj in self._as_list(kwargs.get("cnpj")):
            params.append(("cnpj[]", self._somente_digitos(cnpj)))
        for chave in self._as_list(kwargs.get("access_key")):
            params.append(("access_key[]", chave))
        if kwargs.get("created_at_from"):
            params.append(("created_at[from]", kwargs["created_at_from"]))
        if kwargs.get("created_at_to"):
            params.append(("created_at[to]", kwargs["created_at_to"]))
        if kwargs.get("filter"):
            params.append(("filter", kwargs["filter"]))
        if kwargs.get("format_type"):
            params.append(("format_type", kwargs["format_type"]))
        return self.request("GET", f"{self.base_url}/v1/nfse/{role}", params=params)

    def listar_v2(self, **params):
        """GET /v2/nfse/received — busca NFSes v2."""
        return self.request(
            "GET", f"{self.base_url}/v2/nfse/received", params=params or None
        )

    def incluir_property(self, property_name, body):
        """PUT /v1/nfse/received/{property} — inclui property de NFSe."""
        return self.request(
            "PUT",
            f"{self.base_url}/v1/nfse/received/{property_name}",
            data=body,
        )

    def pdf_ocr(self, role="received", **params):
        """GET /v1/nfse/{role}/manual/pdf — PDF original de NFSe de OCR."""
        return self.request(
            "GET",
            f"{self.base_url}/v1/nfse/{role}/manual/pdf",
            params=params or None,
        )

    def eventos(self, body):
        """POST /v1/dfe/nfse/events — evento de NFSe."""
        return self.request(
            "POST", f"{self.base_url}/v1/dfe/nfse/events", data=body
        )

    def eventos_fila(self, **params):
        """GET /v1/nfse/events — eventos de NFSes (fila)."""
        return self.request(
            "GET", f"{self.base_url}/v1/nfse/events", params=params or None
        )

    def danfse(self, **params):
        """GET /v1/nfse/danfse — busca PDF de NFSe."""
        return self.request(
            "GET", f"{self.base_url}/v1/nfse/danfse", params=params or None
        )

    @staticmethod
    def _as_list(valor):
        if valor is None:
            return []
        if isinstance(valor, (list, tuple)):
            return list(valor)
        return [valor]
