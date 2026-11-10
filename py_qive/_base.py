import base64
import threading
from collections import deque
from datetime import date
from time import sleep, time
from urllib.parse import parse_qs, urlparse

import requests


class QiveCredencialError(Exception):
    """apiId / api-key ausentes ou rejeitados pela Qive (HTTP 401/403)."""


class auth:
    """Cliente base da API Qive (Arquivei) com autenticação por API Key."""

    _RATE_LIMIT_PER_SECOND = 3
    _RATE_LIMIT_DAILY = 120_000
    _MAX_TENTATIVAS = 5
    _TIMEOUT = 120

    def __init__(
        self,
        api_id="",
        api_key="",
        base_url="https://api.arquivei.com.br",
        print_error=True,
        timeout=None,
        max_tentativas=None,
    ):
        if not api_id or not api_key:
            raise QiveCredencialError("api_id e api_key do Qive são obrigatórios")

        self.api_id = api_id
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.print_error = print_error
        self.timeout = timeout if timeout is not None else self._TIMEOUT
        self.max_tentativas = (
            max_tentativas if max_tentativas is not None else self._MAX_TENTATIVAS
        )

        self._rl_lock = threading.Lock()
        self._rl_second_ts: deque = deque()
        self._rl_daily_count = 0
        self._rl_daily_date = date.today()

    def _headers(self, content_type="application/json"):
        headers = {
            "X-API-ID": self.api_id,
            "X-API-KEY": self.api_key,
            "X-Use-ApiGateway": "always",
        }
        if content_type:
            headers["Content-Type"] = content_type
        return headers

    def _rl_acquire(self):
        """Garante respeito aos limites de req/s e req/dia. Thread-safe."""
        with self._rl_lock:
            now = time()
            today = date.today()

            if self._rl_daily_date != today:
                self._rl_daily_count = 0
                self._rl_daily_date = today

            if self._rl_daily_count >= self._RATE_LIMIT_DAILY:
                raise Exception(
                    f"Limite diário de {self._RATE_LIMIT_DAILY} requisições da API Qive atingido. "
                    "Tente novamente amanhã."
                )

            while self._rl_second_ts and now - self._rl_second_ts[0] > 1.0:
                self._rl_second_ts.popleft()

            if len(self._rl_second_ts) >= self._RATE_LIMIT_PER_SECOND:
                wait = 1.0 - (now - self._rl_second_ts[0])
                if wait > 0:
                    sleep(wait)
                now = time()
                while self._rl_second_ts and now - self._rl_second_ts[0] > 1.0:
                    self._rl_second_ts.popleft()

            self._rl_second_ts.append(now)
            self._rl_daily_count += 1

    def request(self, method, url, params=None, data=None, files=None):
        """Requisição HTTP com rate limiting, retry e backoff em 429/5xx/rede."""
        ultimo_erro = None

        for tentativa in range(1, self.max_tentativas + 1):
            self._rl_acquire()
            try:
                content_type = None if files is not None else "application/json"
                kwargs = {
                    "headers": self._headers(content_type=content_type),
                    "timeout": self.timeout,
                }
                if params is not None:
                    kwargs["params"] = params
                if files is not None:
                    kwargs["files"] = files
                    if data is not None:
                        kwargs["data"] = data
                elif data is not None:
                    kwargs["json"] = data

                resp = requests.request(method, url, **kwargs)
            except requests.RequestException as e:
                ultimo_erro = e
                espera = min(60, 2 ** tentativa)
                if self.print_error:
                    print(
                        f"[Qive] Erro de rede (tentativa {tentativa}/{self.max_tentativas}): {e} "
                        f"— aguardando {espera}s"
                    )
                sleep(espera)
                continue

            if resp.status_code in (401, 403):
                raise QiveCredencialError(
                    f"Qive rejeitou as credenciais (HTTP {resp.status_code}): {resp.text[:300]}"
                )

            if resp.status_code == 429 or resp.status_code >= 500:
                retry_after = resp.headers.get("Retry-After")
                espera = (
                    int(retry_after)
                    if retry_after and retry_after.isdigit()
                    else min(60, 2 ** tentativa)
                )
                ultimo_erro = RuntimeError(
                    f"HTTP {resp.status_code}: {resp.text[:300]}"
                )
                if self.print_error:
                    print(
                        f"[Qive] HTTP {resp.status_code} "
                        f"(tentativa {tentativa}/{self.max_tentativas}) — aguardando {espera}s"
                    )
                sleep(espera)
                continue

            if resp.status_code >= 400:
                raise RuntimeError(
                    f"[Qive] HTTP {resp.status_code}: {resp.text[:500]}"
                )

            try:
                return resp.json() or {}
            except ValueError:
                return {"_raw": resp.content, "_status": resp.status_code}

        raise RuntimeError(
            f"[Qive] Falha após {self.max_tentativas} tentativas: {ultimo_erro}"
        )

    @staticmethod
    def _decodificar_xml(xml_b64):
        """Decodifica XML em base64 (UTF-8 com fallback Latin-1)."""
        if not xml_b64:
            return None
        try:
            raw = base64.b64decode(xml_b64)
        except Exception:
            return None
        for enc in ("utf-8", "latin-1"):
            try:
                return raw.decode(enc)
            except UnicodeDecodeError:
                continue
        return None

    @staticmethod
    def _cursor_do_link(link):
        if not link:
            return None
        valores = parse_qs(urlparse(link).query).get("cursor")
        return valores[0].strip() if valores and valores[0].strip() else None

    @staticmethod
    def _somente_digitos(valor):
        return "".join(c for c in str(valor) if c.isdigit())
