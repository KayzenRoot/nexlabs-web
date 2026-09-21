"""Bounded loopback transport probe for the CP-06 Blender MCP receipt."""
from __future__ import annotations

import argparse
import json
import os
import socket
from datetime import datetime, timezone


def parse_port(value: str | None) -> int:
    port = int(value or os.getenv("BLENDER_PORT", "9876"))
    if not 1 <= port <= 65535:
        raise ValueError("port must be between 1 and 65535")
    return port


def probe(host: str, port: int, timeout: float) -> dict[str, object]:
    started = datetime.now(timezone.utc).isoformat()
    try:
        with socket.create_connection((host, port), timeout=timeout):
            status = "PASS"
            error = None
    except OSError as exc:
        status = "FAIL"
        error = f"{type(exc).__name__}: {exc}"
    return {"status": status, "host": host, "port": port, "timeoutSeconds": timeout, "error": error, "capturedAt": started}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default=os.getenv("BLENDER_HOST", "127.0.0.1"))
    parser.add_argument("--port", default=None)
    parser.add_argument("--timeout", type=float, default=2.0)
    args = parser.parse_args()
    receipt = probe(args.host, parse_port(args.port), args.timeout)
    print(json.dumps(receipt, sort_keys=True))
    return 0 if receipt["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
