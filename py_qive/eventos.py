from ._base import auth


class eventos_lote(auth):
    """Recursos de Eventos em Lote da API Qive (Arquivei)."""

    def submeter(self, body):
        """POST /v1/event/batch — submete eventos em lote."""
        return self.request("POST", f"{self.base_url}/v1/event/batch", data=body)

    def status(self, batch_id, **params):
        """GET /v1/event/batch/{id} — consulta status de um lote."""
        return self.request(
            "GET",
            f"{self.base_url}/v1/event/batch/{batch_id}",
            params=params or None,
        )
