from __future__ import annotations

from openexecutive.integrations.email_poller import _workspace_auth_configured


def _clear_workspace_auth(monkeypatch) -> None:
    for key in (
        "GWORKSPACE_AUTH_MODE",
        "GOOGLE_OAUTH_CLIENT_ID",
        "GOOGLE_OAUTH_CLIENT_SECRET",
        "GOOGLE_SERVICE_ACCOUNT_KEY_JSON",
        "GOOGLE_SERVICE_ACCOUNT_KEY_FILE",
        "USER_GOOGLE_EMAIL",
    ):
        monkeypatch.delenv(key, raising=False)


def test_workspace_oauth_requires_both_client_values(monkeypatch) -> None:
    _clear_workspace_auth(monkeypatch)
    monkeypatch.setenv("GWORKSPACE_AUTH_MODE", "oauth")
    monkeypatch.setenv("GOOGLE_OAUTH_CLIENT_ID", "client-id")

    assert not _workspace_auth_configured()

    monkeypatch.setenv("GOOGLE_OAUTH_CLIENT_SECRET", "client-secret")
    assert _workspace_auth_configured()


def test_workspace_service_account_requires_key_and_user(monkeypatch) -> None:
    _clear_workspace_auth(monkeypatch)
    monkeypatch.setenv("GWORKSPACE_AUTH_MODE", "service_account")
    monkeypatch.setenv("GOOGLE_SERVICE_ACCOUNT_KEY_FILE", "/data/google-key.json")

    assert not _workspace_auth_configured()

    monkeypatch.setenv("USER_GOOGLE_EMAIL", "executive@example.com")
    assert _workspace_auth_configured()


def test_unknown_workspace_auth_mode_is_not_ready(monkeypatch) -> None:
    _clear_workspace_auth(monkeypatch)
    monkeypatch.setenv("GWORKSPACE_AUTH_MODE", "unexpected")

    assert not _workspace_auth_configured()
