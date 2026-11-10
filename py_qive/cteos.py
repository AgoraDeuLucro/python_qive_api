from ._base import auth


class cteos(auth):
    """Recursos de CT-e OS da API Qive (Arquivei)."""

    def listar(self, filters=None, fields=None, limite=500, paginator=""):
        """POST /v1/dfe/cteos — busca CTe-OS com filtros."""
        body = {
            "Filters": filters or {},
            "Fields": fields or [],
            "Limit": limite,
        }
        if paginator:
            body["Paginator"] = paginator
        return self.request("POST", f"{self.base_url}/v1/dfe/cteos", data=body)

    def listar_v1(self, role="received", cursor="0", limite=50, **kwargs):
        """GET /v1/cte-os/{role} — busca CTe-OS por papel (cursor)."""
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
        return self.request(
            "GET", f"{self.base_url}/v1/cte-os/{role}", params=params
        )

    def incluir_property(self, property_name, body, role="received"):
        """PUT /v1/cte-os/{role}/{property} — inclui property de CTe-OS."""
        return self.request(
            "PUT",
            f"{self.base_url}/v1/cte-os/{role}/{property_name}",
            data=body,
        )

    def eventos(self, **params):
        """GET /v1/cte-os/events — eventos de um CTe-OS."""
        return self.request(
            "GET", f"{self.base_url}/v1/cte-os/events", params=params or None
        )

    def dacteos(self, **params):
        """GET /v1/cte-os/dacteos — busca PDF de um CTe-OS."""
        return self.request(
            "GET", f"{self.base_url}/v1/cte-os/dacteos", params=params or None
        )

    @staticmethod
    def _as_list(valor):
        if valor is None:
            return []
        if isinstance(valor, (list, tuple)):
            return list(valor)
        return [valor]
