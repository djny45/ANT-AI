from security.hash_ledger import HashLedger


def test_chain_links_to_genesis_and_grows_in_order():
    ledger = HashLedger()

    first = ledger.add_action({"action": "login"})
    second = ledger.add_action({"action": "read"})

    assert first["previous"] == "GENESIS"
    assert second["previous"] == first["hash"]
    assert ledger.chain == [first, second]


def test_same_actions_have_deterministic_hashes_and_different_actions_do_not():
    left = HashLedger()
    right = HashLedger()
    different = HashLedger()

    left.add_action("approve")
    right.add_action("approve")
    different.add_action("deny")

    assert left.chain[0]["hash"] == right.chain[0]["hash"]
    assert left.chain[0]["hash"] != different.chain[0]["hash"]
