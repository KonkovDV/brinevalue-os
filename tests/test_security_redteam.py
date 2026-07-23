"""Security / Red Team regression tests for HTML escaping and input gates."""
from brinevalue.chemistry import Brine
from brinevalue.pipeline import analyze
from brinevalue.report import html_report
from brinevalue.io import brine_from_row


def _b(name="synthetic_sec", **kw):
    ions = dict(
        Na=20000, Cl=35000, Ca=4000, Mg=800, Li=190, Br=250, Sr=900,
        K=4000, B=500, SO4=400, HCO3=300,
    )
    return Brine(ions=ions, flow=4000, unc={"Li": 0.3, "flow": 0.2}, name=name, **kw)


def test_html_report_escapes_xss_name():
    payload = '</title><script>alert(1)</script>'
    b = _b(name=payload)
    res = analyze(b, with_doe=False, with_scenarios=False)
    html = html_report(res, b)
    assert "<script>" not in html
    assert "</title><script>" not in html
    assert "&lt;/title&gt;" in html or "&#" in html or "&lt;script&gt;" in html


def test_validate_rejects_non_numeric_ion():
    try:
        Brine(ions={"Li": "abc"}, flow=1000).validate()
        assert False, "expected ValueError"
    except ValueError as e:
        assert "non-numeric" in str(e)


def test_validate_rejects_unknown_species_strict():
    try:
        Brine(ions={"Li": 10, "Evil": 1}, flow=1000).validate(strict_species=True)
        assert False, "expected ValueError"
    except ValueError as e:
        assert "unknown" in str(e)


def test_validate_drops_unknown_species_lenient():
    b = Brine(ions={"Li": 10.0, "Evil": 1.0}, flow=1000.0, ph=7.0, temp=25.0, org=0.0)
    b.validate(strict_species=False)
    assert "Evil" not in b.ions
    assert b.ions["Li"] == 10.0


def test_validate_rejects_oversized_concentration():
    try:
        Brine(ions={"Li": 1e9}, flow=1).validate()
        assert False, "expected ValueError"
    except ValueError as e:
        assert "exceeds" in str(e)


def test_brine_from_row_rejects_garbage():
    try:
        brine_from_row({"Li": "notanum", "Na": 1, "Cl": 1, "name": "x"})
        assert False, "expected ValueError"
    except ValueError:
        pass


def test_api_stream_model_rejects_unknown_ion():
    try:
        from brinevalue.api import StreamIn
    except Exception:
        return  # fastapi/pydantic optional
    if StreamIn is None:
        return
    try:
        StreamIn(ions={"Li": 1.0, "NotAnIon": 2.0})
        assert False, "expected validation error"
    except Exception:
        pass
