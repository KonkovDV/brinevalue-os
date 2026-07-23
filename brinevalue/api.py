"""Local FastAPI service. On-prem, no outbound traffic.
uvicorn brinevalue.api:app --host 127.0.0.1 --port 8000
"""
try:
    from fastapi import FastAPI
    from pydantic import BaseModel
except Exception:
    FastAPI = None

if FastAPI is not None:
    from .chemistry import Brine
    from .pipeline import analyze
    app = FastAPI(title="BrineValue OS", version="0.1.0")

    class StreamIn(BaseModel):
        ions: dict
        flow: float = 1000.0
        temp: float = 25.0
        ph: float = 6.5
        name: str = "stream"

    @app.get("/health")
    def health():
        return {"status": "ok", "advisory_only": True, "on_prem": True}

    @app.post("/analyze")
    def do(s: StreamIn):
        b = Brine(ions=s.ions, flow=s.flow, temp=s.temp, ph=s.ph, name=s.name,
                  unc={"Li": 0.3, "Mg": 0.25, "Br": 0.3, "Sr": 0.3, "flow": 0.2})
        return analyze(b)
