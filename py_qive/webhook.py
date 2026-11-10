from ._base import auth


class webhook(auth):
    """Recursos de Webhook DF-e da API Qive (Arquivei)."""

    # --- Endpoints ---

    def cadastrar_endpoint(self, body):
        """POST /v1/webhooks/endpoints — cadastra endpoint."""
        return self.request(
            "POST", f"{self.base_url}/v1/webhooks/endpoints", data=body
        )

    def listar_endpoints(self, **params):
        """GET /v1/webhooks/endpoints — lista endpoints."""
        return self.request(
            "GET",
            f"{self.base_url}/v1/webhooks/endpoints",
            params=params or None,
        )

    def obter_endpoint(self, endpoint_id, **params):
        """GET /v1/webhooks/endpoints/{id} — consulta endpoint."""
        return self.request(
            "GET",
            f"{self.base_url}/v1/webhooks/endpoints/{endpoint_id}",
            params=params or None,
        )

    def alterar_endpoint(self, endpoint_id, body):
        """PATCH /v1/webhooks/endpoints/{id} — altera URL do endpoint."""
        return self.request(
            "PATCH",
            f"{self.base_url}/v1/webhooks/endpoints/{endpoint_id}",
            data=body,
        )

    def remover_endpoint(self, endpoint_id):
        """DELETE /v1/webhooks/endpoints/{id} — remove endpoint."""
        return self.request(
            "DELETE", f"{self.base_url}/v1/webhooks/endpoints/{endpoint_id}"
        )

    def reativar_endpoint(self, endpoint_id, body=None):
        """POST /v1/webhooks/endpoints/{id}/reactivate — reativa endpoint."""
        return self.request(
            "POST",
            f"{self.base_url}/v1/webhooks/endpoints/{endpoint_id}/reactivate",
            data=body or {},
        )

    # --- Subscriptions ---

    def criar_subscription(self, body):
        """POST /v1/webhooks/subscriptions — cria subscription."""
        return self.request(
            "POST", f"{self.base_url}/v1/webhooks/subscriptions", data=body
        )

    def listar_subscriptions(self, **params):
        """GET /v1/webhooks/subscriptions — lista subscriptions."""
        return self.request(
            "GET",
            f"{self.base_url}/v1/webhooks/subscriptions",
            params=params or None,
        )

    def remover_subscription(self, subscription_id):
        """DELETE /v1/webhooks/subscriptions/{id} — remove subscription."""
        return self.request(
            "DELETE",
            f"{self.base_url}/v1/webhooks/subscriptions/{subscription_id}",
        )

    # --- Metadata ---

    def metadata(self, **params):
        """GET /v1/webhooks/metadata — valores de webhook."""
        return self.request(
            "GET",
            f"{self.base_url}/v1/webhooks/metadata",
            params=params or None,
        )
