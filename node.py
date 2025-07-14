from flask import Flask, jsonify, request, render_template
from blockchain import Blockchain
import requests
from uuid import uuid4
from urllib.parse import urlparse

# Unique address for this node
node_address = str(uuid4()).replace('-', '')

# Create a blockchain instance
blockchain = Blockchain()

# Flask app
app = Flask(__name__)

# ------------------- ROUTES -----------------------

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/mine', methods=['GET'])
def mine_block():
    last_block = blockchain.get_last_block()
    proof = blockchain.proof_of_work(last_block['proof'])
    blockchain.add_transaction(sender="0", receiver=node_address, amount=1)
    block = blockchain.create_block(proof, blockchain.hash(last_block))
    return jsonify({'message': 'Block mined', 'block': block}), 200

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    tx_data = request.get_json()
    required = ['sender', 'receiver', 'amount']
    if not all(k in tx_data for k in required):
        return 'Missing transaction values', 400
    index = blockchain.add_transaction(tx_data['sender'], tx_data['receiver'], tx_data['amount'])
    return jsonify({'message': f'Transaction will be added to Block {index}'}), 201

@app.route('/get_chain', methods=['GET'])
def get_chain():
    return jsonify({'chain': blockchain.chain, 'length': len(blockchain.chain)}), 200

@app.route('/register_node', methods=['POST'])
def register_node():
    node_data = request.get_json()
    nodes = node_data.get('nodes')
    if nodes is None:
        return "No nodes to add", 400
    for node in nodes:
        blockchain.add_node(node)
    return jsonify({'message': 'Nodes added', 'total_nodes': list(blockchain.nodes)}), 201

@app.route('/replace_chain', methods=['GET'])
def replace_chain():
    def fetch_chain(node):
        try:
            response = requests.get(f'{node}/get_chain')
            if response.status_code == 200:
                return response.json()['chain']
        except:
            return None

    updated = blockchain.replace_chain(fetch_chain)
    if updated:
        return jsonify({'message': 'Chain replaced', 'chain': blockchain.chain}), 200
    return jsonify({'message': 'No replacement needed', 'chain': blockchain.chain}), 200

# ------------------- MAIN -------------------------

if __name__ == '__main__':
    from sys import argv
    port = 5000 if len(argv) < 2 else int(argv[1])
    app.run(host='127.0.0.1', port=port)
