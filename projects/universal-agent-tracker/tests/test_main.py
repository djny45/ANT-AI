from datetime import timezone

from app.main import github_headers, parse_datetime


def test_parse_datetime_normalizes_z_timezone():
    value = parse_datetime("2026-10-26T10:00:00Z")
    assert value is not None
    assert value.utcoffset().total_seconds() == 0
    assert value.tzinfo is not None


def test_parse_datetime_returns_none_for_missing_or_invalid_values():
    assert parse_datetime(None) is None
    assert parse_datetime("not-a-date") is None


def test_github_headers_include_api_version_and_user_agent():
    headers = github_headers()
    assert headers["Accept"] == "application/vnd.github+json"
    assert headers["X-GitHub-Api-Version"] == "2022-11-28"
    assert headers["User-Agent"] == "Universal-Agent-Tracker/0.1"
    assert "Authorization" not in headers
