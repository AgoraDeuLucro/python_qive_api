from ._base import auth


class cnpj(auth):
    """Recursos de Dados Públicos de CNPJs da API Qive (Arquivei)."""

    def listar(self, **params):
        """GET /v1/cnpj — dados públicos de CNPJs."""
        return self.request(
            "GET", f"{self.base_url}/v1/cnpj", params=params or None
        )

    def obter(self, cnpj_valor, **params):
        """GET /v1/cnpj/{CNPJ} — dados públicos de um CNPJ."""
        cnpj_limpo = self._somente_digitos(cnpj_valor)
        return self.request(
            "GET",
            f"{self.base_url}/v1/cnpj/{cnpj_limpo}",
            params=params or None,
        )
