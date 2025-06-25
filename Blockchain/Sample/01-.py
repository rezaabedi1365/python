import hashlib
import json
from time import time

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        # ایجاد بلاک جنسیس (اولین بلاک)
        self.new_block(previous_hash='1', proof=100)

    def new_block(self, proof, previous_hash=None):
        """
        ایجاد بلاک جدید و افزودن به زنجیره
        """
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        # پاک کردن لیست تراکنش‌ها پس از اضافه شدن به بلاک
        self.current_transactions = []
        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        """
        افزودن تراکنش جدید به لیست تراکنش‌ها
        """
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
        return self.last_block['index'] + 1

    @staticmethod
    def hash(block):
        """
        ایجاد هش SHA-256 از بلاک
        """
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, last_proof):
        """
        الگوریتم اثبات کار ساده: پیدا کردن عددی که هش آن با 4 صفر شروع شود
        """
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

# استفاده از بلاکچین
blockchain = Blockchain()

# افزودن تراکنش
blockchain.new_transaction(sender="Alice", recipient="Bob", amount=50)

# انجام اثبات کار و ایجاد بلاک جدید
last_proof = blockchain.last_block['proof']
proof = blockchain.proof_of_work(last_proof)
block = blockchain.new_block(proof)

print("بلاک جدید ساخته شد:")
print(block)
