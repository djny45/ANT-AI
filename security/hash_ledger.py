"""ANT AI hash chain audit ledger."""

from ant_common import sha256_hex

class HashLedger:
    def __init__(self):
        self.chain = []

    def add_action(self, action):
        previous = self.chain[-1]["hash"] if self.chain else "GENESIS"
        block = {
            "action": action,
            "previous": previous,
            "hash": sha256_hex(previous + str(action))
        }
        self.chain.append(block)
        return block
