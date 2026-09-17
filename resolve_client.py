"""Cliente local para el bridge de DaVinci Resolve (v3 con unwrap)."""
from __future__ import annotations
import hashlib
import hmac
import json
import secrets
import socket
import time
from typing import Any, Dict, List, Optional


CONFIG_PATH = r"C:\Users\noqui\Documents\Codex\2026-09-09\ve\work\resolve-connection\bridge.json"
PROTOCOL_VERSION = "1.0"


class BridgeError(RuntimeError):
    def __init__(self, code: str, message: str, details: Optional[dict] = None):
        super().__init__(f"[{code}] {message}")
        self.code = code
        self.message = message
        self.details = details or {}


def _canonical(payload: Dict[str, Any]) -> bytes:
    unsigned = {k: v for k, v in payload.items() if k != "signature"}
    return json.dumps(
        unsigned, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("utf-8")


def _sign(token: str, payload: Dict[str, Any]) -> str:
    return hmac.new(token.encode("utf-8"), _canonical(payload), hashlib.sha256).hexdigest()


def unwrap(result: Any) -> Any:
    """Desenvuelve respuestas del bridge.

    El bridge envuelve TODO en {'value': <contenido>}. Un PyRemoteObject
    se ve como {'value': {'__handle__': 'h:...', ...}} y los escalares como
    {'value': 42}. Este helper devuelve el contenido directo.
    """
    if isinstance(result, dict) and "value" in result and len(result) == 1:
        return result["value"]
    return result


def extract_handle(result: Any) -> Optional[str]:
    """Extrae el handle string si el resultado es un PyRemoteObject."""
    v = unwrap(result)
    if isinstance(v, dict):
        h = v.get("__handle__")
        if isinstance(h, str):
            return h
    return None


class BridgeClient:
    def __init__(self, host, port, token, skew=60, timeout=300.0):
        self.host = host
        self.port = port
        self.token = token
        self.skew = skew
        self.timeout = timeout
        self._counter = 0

    @classmethod
    def from_config(cls, path: str = CONFIG_PATH) -> "BridgeClient":
        with open(path, "r", encoding="utf-8") as fh:
            cfg = json.load(fh)
        return cls(
            host=cfg.get("host", "127.0.0.1"),
            port=cfg["port"],
            token=cfg["token"],
            skew=cfg.get("auth_clock_skew_seconds", 60),
        )

    def _next_id(self) -> str:
        self._counter += 1
        return f"local-{self._counter}-{secrets.token_hex(4)}"

    def _send(self, request: Dict[str, Any]) -> Dict[str, Any]:
        line = (json.dumps(request, separators=(",", ":")) + "\n").encode("utf-8")
        with socket.create_connection((self.host, self.port), timeout=self.timeout) as sock:
            sock.sendall(line)
            buf = bytearray()
            sock.settimeout(self.timeout)
            while True:
                chunk = sock.recv(65536)
                if not chunk:
                    break
                buf.extend(chunk)
                if b"\n" in chunk:
                    break
        if not buf:
            raise BridgeError("no_response", "el bridge no respondio")
        return json.loads(buf.split(b"\n", 1)[0].decode("utf-8"))

    def dispatch(self, operation: str, arguments: Optional[Dict[str, Any]] = None) -> Any:
        request = {
            "protocol": PROTOCOL_VERSION,
            "id": self._next_id(),
            "timestamp": int(time.time()),
            "nonce": secrets.token_urlsafe(24),
            "operation": operation,
            "arguments": arguments or {},
        }
        request["signature"] = _sign(self.token, request)
        response = self._send(request)
        if not response.get("ok"):
            err = response.get("error", {})
            raise BridgeError(
                err.get("code", "unknown"),
                err.get("message", "sin mensaje"),
                err.get("details"),
            )
        return response.get("result")

    # -- atajos -----------------------------------------------------------

    def health(self):
        return unwrap(self.dispatch("health"))

    def list_projects(self):
        return unwrap(self.dispatch("list_projects"))

    def list_timelines(self):
        return unwrap(self.dispatch("list_timelines"))

    def list_methods(self, target: Optional[str] = None) -> List[str]:
        args = {"target": target} if target else {}
        result = unwrap(self.dispatch("list_methods", args))
        if isinstance(result, list):
            return result
        if isinstance(result, dict):
            return result.get("methods", [])
        return []

    def get_attribute(self, name: str, target: Optional[str] = None) -> Any:
        args = {"name": name}
        if target:
            args["target"] = target
        return unwrap(self.dispatch("get_attribute", args))

    def call(self, method: str, *args: Any, target: Optional[str] = None) -> Any:
        """Invoca un metodo. Devuelve el valor ya desenvuelto."""
        payload: Dict[str, Any] = {"method": method, "args": list(args)}
        if target is not None:
            payload["target"] = target
        return unwrap(self.dispatch("call", payload))

    def call_raw(self, method: str, *args: Any, target: Optional[str] = None) -> Any:
        """Como call() pero sin desenvolver. Util para diagnosticar."""
        payload: Dict[str, Any] = {"method": method, "args": list(args)}
        if target is not None:
            payload["target"] = target
        return self.dispatch("call", payload)

    def call_handle(self, method: str, *args: Any, target: Optional[str] = None) -> Optional[str]:
        """Como call(), pero devuelve el handle si el resultado es un PyRemoteObject."""
        return extract_handle(self.dispatch("call", {
            "method": method, "args": list(args), **({"target": target} if target else {})
        }))


if __name__ == "__main__":
    client = BridgeClient.from_config()
    print(json.dumps(client.health(), indent=2, ensure_ascii=False))
