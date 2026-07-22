from __future__ import annotations

import tomllib
from pathlib import Path

import pytest


def test_pyproject_exposes_ahaocode_command() -> None:
    data = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))

    assert data["project"]["name"] == "ahaocode"
    assert data["project"]["scripts"]["ahaocode"] == "ahaocode.__main__:main"
    assert "mewcode" not in data["project"]["scripts"]
    assert data["tool"]["hatch"]["build"]["targets"]["wheel"]["packages"] == ["ahaocode"]


def test_load_config_uses_ahaocode_directory(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    from ahaocode.config import load_config

    monkeypatch.chdir(tmp_path)
    config_dir = tmp_path / ".ahaocode"
    config_dir.mkdir()
    (config_dir / "config.yaml").write_text(
        """
providers:
  - name: test
    protocol: openai
    base_url: https://example.test/v1
    model: test-model
    api_key: test-key
""".strip(),
        encoding="utf-8",
    )

    config = load_config()

    assert config.providers[0].name == "test"


def test_startup_banner_matches_ahaocode_claude_style() -> None:
    from ahaocode.app import AhaocodeApp

    banner = AhaocodeApp._make_banner("claude-3-5-sonnet", r"D:\GitHubProgram\AHaoCode")
    text = banner.plain

    assert "Ahaocode v0.2.0" in text
    assert "Welcome back!" in text
    assert "Tips for getting started" in text
    assert "/init" in text
    assert "What's new" in text
    assert r"D:\GitHubProgram\AHaoCode" in text
    assert "MewCode" not in text
