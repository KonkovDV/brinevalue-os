"""Local FastAPI service. Intended on-prem; default bind is loopback.

uvicorn brinevalue.api:app --host 127.0.0.1 --port 8000

Optional shared-secret gate: set BRINEVALUE_API_TOKEN and send header
X-API-Token (or Authorization: Bearer <token>). When unset, no auth
(local-only trust model — do not expose publicly).
"""
import hmac
import os
from typing import Dict, Optional

try:
    from fastapi import FastAPI, Header, HTTPException
    from pydantic import BaseModel, Field, field_validator
except Exception:
    FastAPI = None

if FastAPI is not None:
    from . import __version__
    from .chemistry import (
        Brine, KNOWN_SPECIES, MAX_FLOW_M3_DAY, MAX_ION_CONC_MG_L, MAX_NAME_LEN,
    )
    from .io import DEFAULT_REL_UNC
    from .pipeline import analyze

    app = FastAPI(
        title="BrineValue OS",
        version=__version__,
        description="On-prem advisory screening API. Not for public internet exposure.",
    )

    _API_TOKEN = os.environ.get("BRINEVALUE_API_TOKEN", "").strip()

    def _check_token(
        x_api_token: Optional[str] = Header(default=None, alias="X-API-Token"),
        authorization: Optional[str] = Header(default=None),
    ):
        if not _API_TOKEN:
            return
        bearer = None
        if authorization and authorization.lower().startswith("bearer "):
            bearer = authorization[7:].strip()
        provided = (x_api_token or bearer or "").strip()
        # Hash to fixed length so compare_digest never raises on length mismatch.
        def _digest(s: str) -> bytes:
            import hashlib
            return hashlib.sha256(s.encode("utf-8")).digest()
        if not hmac.compare_digest(_digest(provided), _digest(_API_TOKEN)):
            raise HTTPException(status_code=401, detail="invalid or missing API token")
    class StreamIn(BaseModel):
        ions: Dict[str, float] = Field(default_factory=dict, max_length=32)
        flow: float = Field(default=1000.0, ge=0.0, le=MAX_FLOW_M3_DAY)
        temp: float = Field(default=25.0, ge=-50.0, le=250.0)
        ph: float = Field(default=6.5, ge=0.0, le=14.0)
        org: float = Field(default=0.0, ge=0.0, le=MAX_ION_CONC_MG_L)
        name: str = Field(default="stream", min_length=1, max_length=MAX_NAME_LEN)

        @field_validator("ions")
        @classmethod
        def _ions_ok(cls, v):
            if not isinstance(v, dict):
                raise ValueError("ions must be an object")
            if len(v) > 32:
                raise ValueError("too many ion keys")
            unknown = [k for k in v if k not in KNOWN_SPECIES]
            if unknown:
                raise ValueError(f"unknown ion species: {unknown}")
            for k, val in v.items():
                try:
                    f = float(val)
                except (TypeError, ValueError) as exc:
                    raise ValueError(f"non-numeric concentration for {k}") from exc
                if f != f or f in (float("inf"), float("-inf")) or f < 0 or f > MAX_ION_CONC_MG_L:
                    raise ValueError(f"invalid concentration for {k}")
            return {k: float(val) for k, val in v.items()}

        @field_validator("name")
        @classmethod
        def _name_ok(cls, v):
            if not isinstance(v, str) or not v.strip():
                raise ValueError("name must be a non-empty string")
            # Strip control characters that break HTML/logs even after escaping.
            cleaned = "".join(ch for ch in v if ch.isprintable() or ch in "\t")
            return cleaned.strip()[:MAX_NAME_LEN]

    @app.get("/health")
    def health():
        return {
            "status": "ok",
            "version": __version__,
            "advisory_only": True,
            "intended_on_prem": True,
            "digital_twin": False,
            "auth_required": bool(_API_TOKEN),
        }

    @app.post("/analyze")
    def do(
        s: StreamIn,
        x_api_token: Optional[str] = Header(default=None, alias="X-API-Token"),
        authorization: Optional[str] = Header(default=None),
    ):
        _check_token(x_api_token=x_api_token, authorization=authorization)
        try:
            b = Brine(
                ions=s.ions, flow=s.flow, temp=s.temp, ph=s.ph, org=s.org, name=s.name,
                unc=dict(DEFAULT_REL_UNC),
            )
            b.validate(strict_species=True)
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc
        try:
            return analyze(b)
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail="analysis failed") from exc
