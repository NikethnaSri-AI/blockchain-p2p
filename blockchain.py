import hashlib, json, time
from uuid import uuid4

class Blockchain:
    def __init__(self):
        self.chain = []
        self.transactions = []
        self.nodes = set()
        self.create_block(proof=1, previous_hash='0')  # Genesis block

    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time.time(),
            'transactions': self.transactions,
            'proof': proof,
            'previous_hash': previous_hash
        }
        self.transactions = []
        self.chain.append(block)
        return block

    def get_last_block(self):
        return self.chain[-1]

    def add_transaction(self, sender, receiver, amount):
        self.transactions.append({'sender': sender, 'receiver': receiver, 'amount': amount})
        return self.get_last_block()['index'] + 1

    def proof_of_work(self, previous_proof):
        new_proof = 1
        while True:
            hash_val = hashlib.sha256(f'{new_proof**2 - previous_proof**2}'.encode()).hexdigest()
            if hash_val[:4] == '0000':
                return new_proof
            new_proof += 1

    def hash(self, block):
        encoded = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded).hexdigest()

    def is_chain_valid(self, chain):
        for i in range(1, len(chain)):
            prev = chain[i-1]
            curr = chain[i]
            if curr['previous_hash'] != self.hash(prev):
                return False
            if not self.valid_proof(prev['proof'], curr['proof']):
                return False
        return True

    def valid_proof(self, prev_proof, proof):
        guess = f'{proof**2 - prev_proof**2}'.encode()
        return hashlib.sha256(guess).hexdigest()[:4] == '0000'

    def add_node(self, address):
        self.nodes.add(address)

    def replace_chain(self, fetch_chain_func):
        original_chain = self.chain
        longest = self.chain
        for node in self.nodes:
            chain = fetch_chain_func(node)
            if chain and len(chain) > len(longest) and self.is_chain_valid(chain):
                longest = chain
        self.chain = longest
        return self.chain != original_chain
