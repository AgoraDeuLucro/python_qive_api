from ._base import auth


class nfe(auth):
    """Recursos de NF-e da API Qive (Arquivei)."""

    # --- Busca ---

    def listar_v1(self, role="received", cursor="0", limite=50, **kwargs):
        """GET /v1/nfe/{role} — busca XMLs de NFes por papel.

        Args:
            role: received | emitted | transporter | authorized
            cursor: posição de paginação (default ``"0"``)
            limite: máx. 50 por página
            **kwargs: cnpj, access_key (str ou list), created_at_from, created_at_to,
                      filter, format_type
        """
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

        dados = self.request("GET", f"{self.base_url}/v1/nfe/{role}", params=params)

        itens = dados.get("data") or []
        notas = []
        erros_xml = []
        for item in itens:
            chave = (item.get("access_key") or "").strip()
            xml = self._decodificar_xml(item.get("xml") or "")
            if not xml and item.get("xml"):
                erros_xml.append(chave or "?")
                continue
            notas.append({"chave": chave, "xml": xml, "raw": item})

        count = dados.get("count")
        return {
            "notas": notas,
            "proximo_cursor": self._cursor_do_link(
                (dados.get("page") or {}).get("next")
            ),
            "count": (
                int(count)
                if isinstance(count, (int, str)) and str(count).isdigit()
                else len(itens)
            ),
            "erros_xml": erros_xml,
            "page": dados.get("page") or {},
            "status": dados.get("status"),
        }

    def listar_v1_todas(self, role="received", limite=50, max_paginas=200, **kwargs):
        """Pagina automaticamente via cursor até esgotar as páginas."""
        todas = []
        cursor = kwargs.pop("cursor", "0") or "0"
        vistos = set()

        for _ in range(1, max_paginas + 1):
            pagina = self.listar_v1(
                role=role, cursor=cursor, limite=limite, **kwargs
            )
            todas.extend(pagina["notas"])

            proximo = pagina.get("proximo_cursor")
            count = pagina.get("count", 0)

            if count < limite:
                break
            if not proximo or proximo == cursor:
                break
            if proximo in vistos:
                break
            vistos.add(proximo)
            cursor = proximo
        else:
            if self.print_error:
                print(f"[Qive] Limite de {max_paginas} páginas (v1) atingido")

        return todas

    def listar_v2(self, filters=None, fields=None, limite=500, paginator=""):
        """POST /v2/dfe/nfe — busca NFes com filtros ricos.

        Args:
            filters: dict de filtros (EmissionDate, ReceiverCnpj, etc.)
            fields: lista de campos a retornar
            limite: tamanho da página (default 500)
            paginator: token da página anterior
        """
        body = {
            "Filters": filters or {},
            "Fields": fields
            or ["Xml", "AccessKey", "EmissionDate", "Status", "CreatedAt"],
            "Limit": limite,
        }
        if paginator:
            body["Paginator"] = paginator

        dados = self.request("POST", f"{self.base_url}/v2/dfe/nfe", data=body)

        notas = []
        for item in dados.get("Nfes") or []:
            chave = (item.get("AccessKey") or "").strip()
            xml_raw = item.get("Xml") or ""
            xml = self._decodificar_xml(xml_raw) if xml_raw else None
            notas.append(
                {
                    "chave": chave,
                    "xml": xml,
                    "status": item.get("Status"),
                    "emissao": item.get("EmissionDate"),
                    "raw": item,
                }
            )

        return {
            "notas": notas,
            "paginator": (dados.get("Paginator") or "").strip(),
            "total": dados.get("Total"),
        }

    def listar_v2_todas(
        self, filters=None, fields=None, limite=500, max_paginas=1000
    ):
        """Pagina automaticamente via Paginator até esgotar as páginas."""
        todas = []
        paginator = ""
        vistos = set()

        for _ in range(1, max_paginas + 1):
            pagina = self.listar_v2(
                filters=filters, fields=fields, limite=limite, paginator=paginator
            )
            todas.extend(pagina["notas"])

            paginator = pagina.get("paginator") or ""
            if not paginator:
                break
            if not pagina["notas"]:
                break
            if paginator in vistos:
                break
            vistos.add(paginator)
        else:
            if self.print_error:
                print(f"[Qive] Limite de {max_paginas} páginas (v2) atingido")

        return todas

    # --- Property ---

    def incluir_property(self, property_name, body, role="received"):
        """PUT /v1/nfe/{role}/{property} — aplica valor de property nas NFes."""
        return self.request(
            "PUT",
            f"{self.base_url}/v1/nfe/{role}/{property_name}",
            data=body,
        )

    # --- Upload ---

    def upload(self, body):
        """POST /v1/nfe/upload — upload em bulk de NFes."""
        return self.request("POST", f"{self.base_url}/v1/nfe/upload", data=body)

    def upload_status(self, **params):
        """GET /v1/nfe/upload/status — status do upload de NFes."""
        return self.request(
            "GET", f"{self.base_url}/v1/nfe/upload/status", params=params or None
        )

    # --- Manifestação ---

    def listar_manifestacoes_v2(self, **params):
        """GET /v2/nfe/manifest — lista manifestações (v2)."""
        return self.request(
            "GET", f"{self.base_url}/v2/nfe/manifest", params=params or None
        )

    def listar_manifestacoes(self, **params):
        """GET /v1/nfe/manifest — lista manifestações (v1)."""
        return self.request(
            "GET", f"{self.base_url}/v1/nfe/manifest", params=params or None
        )

    def incluir_manifestacao(self, body):
        """POST /v1/nfe/manifest — inclui manifestação do destinatário."""
        return self.request("POST", f"{self.base_url}/v1/nfe/manifest", data=body)

    def status_manifestacao(self, **params):
        """GET /v1/nfe/manifest/status — status de uma manifestação."""
        return self.request(
            "GET", f"{self.base_url}/v1/nfe/manifest/status", params=params or None
        )

    def incluir_manifestacao_sync(self, body):
        """POST /v1/nfe/manifest/sync — inclui manifestação síncrona."""
        return self.request(
            "POST", f"{self.base_url}/v1/nfe/manifest/sync", data=body
        )

    # --- Eventos ---

    def eventos(self, **params):
        """GET /v2/nfe/events — eventos de uma NFe."""
        return self.request(
            "GET", f"{self.base_url}/v2/nfe/events", params=params or None
        )

    def eventos_fila(self, **params):
        """GET /v1/events/nfe — eventos de NFes (fila)."""
        return self.request(
            "GET", f"{self.base_url}/v1/events/nfe", params=params or None
        )

    def eventos_rtc(self, body):
        """POST /v1/dfe/nfe/events — eventos RTC."""
        return self.request(
            "POST", f"{self.base_url}/v1/dfe/nfe/events", data=body
        )

    # --- PDF ---

    def danfe(self, **params):
        """GET /v1/nfe/danfe — busca PDF (DANFe) em base64."""
        return self.request(
            "GET", f"{self.base_url}/v1/nfe/danfe", params=params or None
        )

    # --- helpers ---

    @staticmethod
    def _as_list(valor):
        if valor is None:
            return []
        if isinstance(valor, (list, tuple)):
            return list(valor)
        return [valor]
