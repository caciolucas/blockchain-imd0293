from blockchain import Blockchain
import json
from flask_cors import CORS, cross_origin
from time import time

blockchain = Blockchain()


from flask import Flask, request
app = Flask(__name__)
CORS(app)

@app.route('/chain', methods=['GET'])
def chain():
    return json.dumps([{'block':block, 'id':blockchain.getBlockID(block)}for block in blockchain.chain])

@app.route('/transactions/mempool', methods=['GET'])
def transactions_mempool():
    return json.dumps(blockchain.memPool)

@app.route('/transactions/create', methods=['POST'])
def transactions_create():
    data = request.get_json()
    if not data:
        data = request.form
    blockchain.createTransaction(data['sender'], data['recipient'], data['amount'],int(time()), data['privWifKey'])
    return json.dumps(blockchain.memPool)

@app.route('/mine', methods=['GET'])
def mine():
    blockchain.createBlock(previousHash=blockchain.getBlockID(blockchain.prevBlock))
    blockchain.mineProofOfWork(blockchain.prevBlock)
    return json.dumps(blockchain.prevBlock)

@app.route('/node/register', methods=['POST'])
def node_register():
    data = request.get_json()
    if not data:
        data = request.form
    blockchain.nodes.add(data['node_address'])
    
    return json.dumps(list(blockchain.nodes))

@app.route('/node/list', methods=['GET'])
def node_list():
    return json.dumps(list(blockchain.nodes))


@app.route('/node/resolve', methods=['GET'])
def node_resolve():
    changed = blockchain.resolveConflicts()
    response = {'changed':changed,'chain':blockchain.chain}
    return json.dumps(response)

if __name__ == '__main__':
    app.run(port=5001)