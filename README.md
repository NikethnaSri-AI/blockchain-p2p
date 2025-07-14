P2P Blockchain Network Simulation

This project simulates a peer-to-peer (P2P) blockchain network with multiple nodes, each running independently and capable of mining blocks, adding transactions, and syncing their blockchains using a consensus algorithm.

How to Run:

Requirements
- Python 3.x
- Flask
- Requests

Start Nodes:
# Terminal 1
python node.py 5000

# Terminal 2
python node.py 5001

# Terminal 3
python node.py 5002


Dashboard UI:
Each node has a dashboard you can access in a browser:

http://127.0.0.1:5000/
http://127.0.0.1:5001/
http://127.0.0.1:5002/

The UI lets you:

- View the chain
- Mine a new block
- Replace chain


Interacting with Nodes (via curl or browser):
1. Register Peers
bash
Copy
Edit
curl -X POST http://127.0.0.1:5000/register_node \
-H "Content-Type: application/json" \
-d '{"nodes": ["http://127.0.0.1:5001", "http://127.0.0.1:5002"]}'

2. Mine a Block
Click Mine Block on the UI or run:

bash
Copy
Edit
curl http://127.0.0.1:5000/mine

3. Replace Chain
Click Replace Chain on another node (e.g., port 5001) to sync it with the longest chain.
