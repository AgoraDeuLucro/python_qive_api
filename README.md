# py_qive

Wrapper não oficial da API Qive (Arquivei) para Python.

Cobre os endpoints documentados em [developers.qive.com.br](https://developers.qive.com.br/docs).

## Instalação

```bash
pip install .
# ou
pip install -e .
```

## Autenticação

```python
from py_qive import nfe

client = nfe(api_id="SEU_API_ID", api_key="SEU_API_KEY")
```

Headers usados em todas as chamadas: `X-API-ID`, `X-API-KEY`, `X-Use-ApiGateway: always`.

Base URLs:
- Produção: `https://api.arquivei.com.br`
- Sandbox: `https://sandbox-api.arquivei.com.br`

```python
client = nfe(
    api_id="...",
    api_key="...",
    base_url="https://sandbox-api.arquivei.com.br",
    timeout=120,
    max_tentativas=5,
)
```

## Módulos disponíveis

| Classe | Uso |
|--------|-----|
| `nfe` | NF-e (busca, manifestação, eventos, DANFe, upload) |
| `nfse` | NFS-e |
| `cte` | CT-e |
| `cteos` | CT-e OS |
| `nfce` | NFC-e |
| `mdfe` | MDF-e |
| `flagerp` | FlagErp |
| `etiquetas` | Tags de conta e DFe |
| `upload` | Upload genérico de DFes |
| `empresas` | Empresas e certificado |
| `property` / `property_` | Properties |
| `boletos` | Boletos bancários |
| `comprovantes` | Comprovantes |
| `invoice` | Invoices |
| `utilities` | Utilities |
| `ocr` | OCR |
| `latam` | Docs LATAM |
| `cnpj` | Dados públicos de CNPJ |
| `eventos_lote` | Eventos em lote |
| `webhook` | Webhooks DF-e |

```python
from py_qive import nfe, cte, webhook, empresas
```

## Exemplos — NF-e

### Busca v1 (cursor)

```python
pagina = client.listar_v1(
    role="received",
    cnpj="12345678000199",
    created_at_from="2026-01-01",
    cursor="0",
    limite=50,
)
# pagina["notas"], pagina["proximo_cursor"], pagina["count"]

notas = client.listar_v1_todas(
    role="received",
    cnpj="12345678000199",
    created_at_from="2026-01-01",
)
```

### Busca v2 (filtros + Paginator)

```python
pagina = client.listar_v2(
    filters={
        "EmissionDate": {"From": "2026-01-01", "To": "2026-01-31"},
        "ReceiverCnpj": ["12345678000199"],
    },
    fields=["Xml", "AccessKey", "EmissionDate", "Status"],
    limite=500,
)

notas = client.listar_v2_todas(
    filters={
        "EmissionDate": {"From": "2026-01-01", "To": "2026-01-31"},
        "ReceiverCnpj": ["12345678000199"],
    }
)
```

### Manifestação, eventos e DANFe

```python
client.incluir_manifestacao({"...": "..."})
client.incluir_manifestacao_sync({"...": "..."})
client.listar_manifestacoes(access_key="...")
client.eventos(access_key="...")
client.danfe(access_key="...")
```

## Outros módulos

```python
from py_qive import cte, webhook, cnpj, empresas

cte_client = cte(api_id="...", api_key="...")
cte_client.listar(filters={"EmissionDate": {"From": "2026-01-01", "To": "2026-01-31"}})

wh = webhook(api_id="...", api_key="...")
wh.listar_endpoints()
wh.cadastrar_endpoint({"url": "https://meu.app/hook"})

c = cnpj(api_id="...", api_key="...")
c.obter("12345678000199")

emp = empresas(api_id="...", api_key="...")
emp.listar()
```

## Exceções

```python
from py_qive import QiveCredencialError

try:
    client = nfe(api_id="...", api_key="...")
    client.listar_v1(role="received")
except QiveCredencialError as e:
    print("Credenciais inválidas:", e)
```
