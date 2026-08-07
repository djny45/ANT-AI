from security.zero_trust_engine import ZeroTrustEngine


def test_register_and_verify():
    z = ZeroTrustEngine()
    assert z.register_identity("id1", "secret")
    res = z.verify("id1", "do_something", "secret")
    assert res["identity_verified"] is True
    assert res["action_verified"] is True
    assert res["verified"] is True
