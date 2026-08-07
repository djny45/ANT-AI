from security.permission_manager import PermissionManager


def test_grant_revoke_check():
    pm = PermissionManager()
    pm.grant("agent1", "deploy", "for testing")
    res = pm.check("agent1", "deploy")
    assert res["approved"] is True
    assert "deploy" in res["permissions"]

    pm.revoke("agent1", "deploy", "revoke test")
    res2 = pm.check("agent1", "deploy")
    assert res2["approved"] is False

    # audit log entries
    audit = pm.get_audit_log()
    assert any(entry["action"] == "GRANT" for entry in audit)
    assert any(entry["action"] == "REVOKE" for entry in audit)
