"""Packaging smoke: editable install must not discover data/ as a package."""
from pathlib import Path


def test_pyproject_excludes_data_package():
    text = Path("pyproject.toml").read_text(encoding="utf-8")
    assert 'include = ["brinevalue*"]' in text
    assert "exclude" in text and "data*" in text


def test_setuptools_find_only_brinevalue():
    from setuptools import find_packages

    pkgs = find_packages(include=["brinevalue*"], exclude=["data*", "tests*", "benchmark*", "docs*"])
    assert pkgs == ["brinevalue"]


def test_import_version():
    import brinevalue

    assert brinevalue.__version__ == "0.5.2"
