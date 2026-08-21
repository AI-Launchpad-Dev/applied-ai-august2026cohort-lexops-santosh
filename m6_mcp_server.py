"""Milestone 6, part 1: MCP server exposing the contract repository /
e-signature mock API.

Wraps data/lexops/mock_api/*.csv as MCP tools so agents query contracts and
counterparties, and create signature-request envelopes, over the MCP
protocol rather than reading/writing the CSV files directly.

This file is not meant to be run standalone in normal use -- it's launched
as a subprocess by the MCP client in m6_multi_agent.py, communicating over
stdio. You can still run it directly to sanity-check that it starts without
errors: python m6_mcp_server.py (it will just sit waiting for a client).
"""

from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from mcp.server import MCPServer

mcp = MCPServer("lexops-contract-repository")

MOCK_API_DIR = Path("data/lexops/mock_api")

def _read_csv(name: str) -> list[dict[str, Any]]:
    path = MOCK_API_DIR / f"{name}.csv"
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


@mcp.tool()
def get_contract(contract_id: str) -> dict[str, Any]:
    """Look up one contract by its contract_id from the mock contract repository."""
    for row in _read_csv("contracts"):
        if row.get("contract_id") == contract_id:
            return row
    return {"error": f"No contract found with id {contract_id}"}


@mcp.tool()
def get_counterparty(counterparty_id: str) -> dict[str, Any]:
    """Look up one counterparty by id, including negotiation posture history."""
    for row in _read_csv("counterparties"):
        if row.get("counterparty_id") == counterparty_id:
            return row
    return {"error": f"No counterparty found with id {counterparty_id}"}


@mcp.tool()
def list_signature_requests(contract_id: str) -> list[dict[str, Any]]:
    """List all e-signature envelopes associated with a contract_id."""
    return [r for r in _read_csv("signature_requests") if r.get("contract_id") == contract_id]


@mcp.tool()
def create_signature_request(contract_id: str, signer_email: str) -> dict[str, Any]:
    """Create a new e-signature envelope for a contract and append it to the
    mock repository (writes both the .csv and .json mirrors)."""
    rows = _read_csv("signature_requests")
    new_id = f"NW-SIG-{len(rows):05d}"
    new_row = {
        "envelope_id": new_id,
        "contract_id": contract_id,
        "status": "sent",
        "sent_at": datetime.now(timezone.utc).isoformat(timespec="minutes"),
        "signer_email": signer_email,
    }
    rows.append(new_row)

    MOCK_API_DIR.mkdir(parents=True, exist_ok=True)
    csv_path = MOCK_API_DIR / "signature_requests.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(new_row.keys()))
        writer.writeheader()
        writer.writerows(rows)

    json_path = MOCK_API_DIR / "signature_requests.json"
    json_path.write_text(json.dumps(rows, indent=2), encoding="utf-8")

    return new_row


if __name__ == "__main__":
    mcp.run()
