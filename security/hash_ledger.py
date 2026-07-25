"""ANT AI hash chain audit ledger."""

import hashlib

class HashLedger:
    def __init__(self):
        self.chain = []

    def add_action(self, action):
        previous = self.chain[-1]["hash"] if self.chain else "GENESIS"
        data = previous + str(action)
        block_hash = hashlib.sha256(data.encode()).hexdigest()
        block = {
            "action": action,
            "previous": previous,
            "hash": block_hash
        }
        self.chain.append(block)
        return block
