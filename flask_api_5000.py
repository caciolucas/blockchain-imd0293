from blockchain import Blockchain
import json

blockchain = Blockchain()


from flask import Flask, request
app = Flask(__name__)

@app.route('/chain', methods=['GET'])
def chain():
    return json.dumps(blockchain.chain)

@app.route('/transactions/mempool', methods=['GET'])
def transactions_mempool():
    return json.dumps(blockchain.memPool)

@app.route('/transactions/create', methods=['POST'])
def transactions_create():
    data = request.form
    blockchain.createTransaction(data['sender'], data['recipient'], data['amount'], data['timestamp'], data['privWifKey'])
    return json.dumps(blockchain.memPool[-1])

@app.route('/mine', methods=['GET'])
def mine():
    blockchain.createBlock(previousHash=blockchain.getBlockID(blockchain.prevBlock))
    blockchain.mineProofOfWork(blockchain.prevBlock)
    return json.dumps(blockchain.prevBlock)

@app.route('/node/register', methods=['POST'])
def node_register():
    data = request.form
    if 'node_address' in data:
        blockchain.nodes.add(data['node_address'])
    
    return json.dumps(list(blockchain.nodes))

@app.route('/node/resolve', methods=['GET'])
def node_resolve():
    changed = blockchain.resolveConflicts()
    return json.dumps({'changed':changed,'chain':blockchain.chain})

if __name__ == '__main__':
    app.run(port=5000)