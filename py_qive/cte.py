from ._base import auth


class cte(auth):
    """Recursos de CT-e da API Qive (Arquivei)."""

    def listar(self, filters=None, fields=None, limite=500, paginator=""):
        """POST /v1/dfe/cte — busca CTes com filtros."""
        body = {
            "Filters": filters or {},
            "Fields": fields or [],
            "Limit": limite,
        }
        if paginator:
            body["Paginator"] = paginator
        return self.request("POST", f"{self.base_url}/v1/dfe/cte", data=body)

    def listar_v1(self, role="received", cursor="0", limite=50, **kwargs):
        """GET /v1/cte/{role} — busca CTes por papel (cursor)."""
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
        return self.request("GET", f"{self.base_url}/v1/cte/{role}", params=params)

    def incluir_property(self, property_name, body, role="received"):
        """PUT /v1/cte/{role}/{property} — inclui property de CTe."""
        return self.request(
            "PUT",
            f"{self.base_url}/v1/cte/{role}/{property_name}",
            data=body,
        )

    def eventos(self, **params):
        """GET /v1/cte/events — eventos de um CTe."""
        return self.request(
            "GET", f"{self.base_url}/v1/cte/events", params=params or None
        )

    def eventos_fila(self, **params):
        """GET /v2/cte/events — eventos de CTes (fila)."""
        return self.request(
            "GET", f"{self.base_url}/v2/cte/events", params=params or None
        )

    def upload(self, body):
        """POST /v1/cte/upload — upload em bulk de CTes."""
        return self.request("POST", f"{self.base_url}/v1/cte/upload", data=body)

    def upload_status(self, **params):
        """GET /v1/cte/upload/status — status do upload de CTes."""
        return self.request(
            "GET", f"{self.base_url}/v1/cte/upload/status", params=params or None
        )

    def dacte(self, **params):
        """GET /v1/cte/dacte — busca PDF de um CTe."""
        return self.request(
            "GET", f"{self.base_url}/v1/cte/dacte", params=params or None
        )

    @staticmethod
    def _as_list(valor):
        if valor is None:
            return []
        if isinstance(valor, (list, tuple)):
            return list(valor)
        return [valor]
