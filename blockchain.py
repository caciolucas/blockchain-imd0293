import hashlib
import json
from time import time
import copy
import random
import bitcoinlib # pip install bitcoin
from math import ceil, floor

DIFFICULTY = 4 # Quantidade de zeros (em hex) iniciais no hash valido.

class Blockchain(object):

    def __init__(self):
        self.chain = []
        self.memPool = []
        self.nodes = set() # Conjunto para armazenar os nós registrados.
        self.createGenesisBlock()

    def createGenesisBlock(self):
        # Cria o bloco genêsis
        self.createBlock(previousHash='0'*64, nonce=0)
        self.mineProofOfWork(self.prevBlock) 

    def createBlock(self, nonce=0, previousHash=None):
        # Retorna um novo bloco criado e adicionado ao blockchain (ainda não minerado).
        if (previousHash == None):
            previousBlock = self.chain[-1]
            previousBlockCopy = copy.copy(previousBlock)
            previousBlockCopy.pop("transactions", None)

        block = {
            'index': len(self.chain) + 1,
            'timestamp': int(time()),
            'transactions': self.memPool,
            'merkleRoot': self.generateMerkleRoot(self.memPool),
            'nonce': nonce,
            'previousHash': previousHash or self.generateHash(previousBlockCopy),
        }

        self.memPool = []
        self.chain.append(block)
        return block

    def mineProofOfWork(self, prevBlock):
        # Retorna o nonce que satisfaz a dificuldade atual para o bloco passado como argumento.
        nonce = 0
        while self.isValidProof(prevBlock, nonce) is False:
            nonce += 1

        return nonce

    def createTransaction(self, sender, recipient, amount, timestamp, privWifKey):
        # Cria uma nova transação, assinada pela chave privada WIF do remetente
        # e inclua no memory pool
        transaction = {
            "sender": sender,
            "recipient": recipient,
            "amount": amount,
            "timestamp": timestamp,
        }
        signature = Blockchain.sign(privWifKey, json.dumps(transaction, sort_keys=True))
        transaction['signature']=signature
        self.memPool.append(transaction)
        pass
        

    @staticmethod
    def generateMerkleRoot(transactions):
        # Gera a Merkle Root de um bloco com as respectivas transações.
        # Retorne a string referente a merkle root.

        n_steps = ceil(len(transactions)/2)
        # print(f'Numero de steps: {n_steps}')
        steps = [[Blockchain.generateHash(transaction) for transaction in transactions]]
        # print(json.dumps(steps,indent=2))
        for i in range(0,n_steps):
            n_hashs=ceil(len(steps[-1])/2)
            # print(f"Prox numero de hashs: {n_hashs}")
            step=[]
            for x in range(0,len(steps[-1]),2):
                y=x+1
                if(y<len(steps[-1])):
                    # print(f"Calculando hash do proximo step com ({x} e {y}): {steps[-1][x]} e {steps[-1][y]}")
                    step.append(Blockchain.generateHash([steps[-1][x],steps[-1][y]]))
                    # print(f"Adicionando hash calculada: {Blockchain.generateHash([steps[-1][x],steps[-1][y]])}")

            if (len(steps[-1])%2!=0):
                # print(f"Quantidade ímpar, repassando o último pra o próximo step: {steps[-1][-1]}")
                step.append(steps[-1][-1])
            # print("Step a seguir adicionado")
            # print(json.dumps(step,indent=2))
            # print(f'N Step correto? {"Sim" if n_hashs+1==len(step) else "Não"}')
            steps.append(step)
        # print("Steps atualizados ============================")
        # print(json.dumps(steps,indent=2))
        # print(f'N Steps corretos? {"Sim" if n_steps+1==len(steps) else "Não"}')
        
        if not len(steps[-1]):
            return "0"*64
        return steps[-1][-1]

    @staticmethod
    def isValidProof(block, nonce):
        # Retorna True caso o nonce satisfaça a dificuldade atual para o bloco passado como argumento.
        block['nonce'] = nonce
        guessHash = Blockchain.getBlockID(block)
        return guessHash[:DIFFICULTY] == '0' * DIFFICULTY 

    @staticmethod
    def generateHash(data):
        # Retorna o SHA256 do argumento passado.
        blkSerial = json.dumps(data, sort_keys=True).encode()
        return hashlib.sha256(blkSerial).hexdigest()

    @staticmethod
    def getBlockID(block):
        # Retorna o ID (hash do cabeçalho) do bloco passado como argumento.
        blockCopy = copy.copy(block)
        blockCopy.pop("transactions", None)
        return Blockchain.generateHash(blockCopy)

    def printChain(self,short=False, color=False, expanded=False):
        # Mantenha seu método de impressão do blockchain feito na prática passada.

        
        # Implemente aqui um método para imprimir de maneira verbosa e intuitiva o blockchain atual.
        if color:
            print('                                       \x1b[6;36;49m....\x1b[0m')
            for block in self.chain[::-1]:
                print(f"                                        \x1b[6;36;49m^^\x1b[0m")
                print(f"                                        \x1b[6;36;49m||\x1b[0m")
                print(f"                                        \x1b[6;36;49m||\x1b[0m")
                print(f"        \x1b[1;36;49m+------------------------------------------------------------------+")
                print(f"        \x1b[1;36;49m|\x1b[0m \x1b[1;36;49m{Blockchain.getBlockID(block)}\x1b[0m \x1b[1;36;49m|\x1b[0m")
                print(f"        \x1b[1;36;49m+------------------------------------------------------------------+")
                print(f"        \x1b[1;36;49m|\x1b[0m \x1b[1;30;46mÍndice:\x1b[0m         \x1b[1;30;46mTimestamp:\x1b[0m              \x1b[1;30;46mNonce:\x1b[0m                   \x1b[1;36;49m|\x1b[0m")
                print(f"        \x1b[1;36;49m|\x1b[0m \x1b[1;36;49m{block['index']:06}\x1b[0m          \x1b[1;36;49m{int(block['timestamp'])}\x1b[0m              \x1b[1;36;49m{block['nonce']:015}\x1b[0m          \x1b[1;36;49m|\x1b[0m")
                if not short:
                    print(f"        \x1b[1;36;49m|\x1b[0m                                                                  \x1b[1;36;49m|\x1b[0m")
                    print(f"        \x1b[1;36;49m|\x1b[0m \x1b[1;30;46mMerkle Root:\x1b[0m                                                     \x1b[1;36;49m|\x1b[0m")
                    print(f"        \x1b[1;36;49m|\x1b[0m \x1b[1;36;49m{block['merkleRoot']}\x1b[0m \x1b[1;36;49m|\x1b[0m")
                    print(f"        \x1b[1;36;49m|\x1b[0m                                                                  \x1b[1;36;49m|\x1b[0m")
                    print(f"        \x1b[1;36;49m|\x1b[0m \x1b[1;30;46mTransações:\x1b[0m                                                      \x1b[1;36;49m|\x1b[0m")
                    print(f"        \x1b[1;36;49m|\x1b[0m \x1b[1;36;49m{len(block['transactions']):05}\x1b[0m                                                            \x1b[1;36;49m|\x1b[0m")
                    print(f"        \x1b[1;36;49m|\x1b[0m                                                                  \x1b[1;36;49m|\x1b[0m")
                print(f"        \x1b[1;36;49m+------------------------------------------------------------------+")
                if expanded:
                    if len(block['transactions']):
                        print(f"        \x1b[1;36;49m|   ---------------======**\x1b[0m  \x1b[1;30;46mTransações\x1b[0m\x1b[1;36;49m  **=====----------------   |\x1b[0m")
                    for transaction in block['transactions']:
                        print(f"        \x1b[1;36;49m|\x1b[0m \x1b[1;30;46mRemetente:\x1b[0m                              \x1b[1;30;46mTimestamp:\x1b[0m               \x1b[1;36;49m|\x1b[0m")
                        print(f"        \x1b[1;36;49m|\x1b[0m \x1b[1;36;49m{transaction['sender']}\x1b[0m      \x1b[1;36;49m{transaction['timestamp']}\x1b[0m               \x1b[1;36;49m|\x1b[0m")
                        print(f"        \x1b[1;36;49m|\x1b[0m                                                                  \x1b[1;36;49m|\x1b[0m")
                        print(f"        \x1b[1;36;49m|\x1b[0m \x1b[1;30;46mDestinatario:\x1b[0m                           \x1b[1;30;46mQuantidade:\x1b[0m              \x1b[1;36;49m|\x1b[0m")
                        print(f"        \x1b[1;36;49m|\x1b[0m \x1b[1;36;49m{transaction['recipient']}\x1b[0m      \x1b[1;36;49m{transaction['amount']:018.14f}\x1b[0m       \x1b[1;36;49m|\x1b[0m")
                        if(not transaction==block['transactions'][-1]):
                            print(f"        \x1b[1;36;49m|        -----------------======****=====-----------------         |\x1b[0m")
                        # print(f"        |                             --==--                               |")
                    if len(block['transactions']):
                        print(f"        \x1b[1;36;49m+------------------------------------------------------------------+\x1b[0m")
                print(f"        \x1b[1;36;49m|\x1b[0m \x1b[1;30;46mHash do último bloco:\x1b[0m                                            \x1b[1;36;49m|\x1b[0m")
                print(f"        \x1b[1;36;49m|\x1b[0m \x1b[1;36;49m{block['previousHash']}\x1b[0m \x1b[1;36;49m|\x1b[0m")
                print(f"        \x1b[1;36;49m+------------------------------------------------------------------+")
        else:
            print('                                       ....')
            for block in self.chain[::-1]:
                print(f"                                        ^^")
                print(f"                                        ||")
                print(f"                                        ||")
                print(f"        +------------------------------------------------------------------+")
                print(f"        | {Blockchain.getBlockID(block)} |")
                print(f"        +------------------------------------------------------------------+")
                print(f"        | Índice:         Timestamp:              Nonce:                   |")
                print(f"        | {block['index']:06}          {int(block['timestamp'])}              {block['nonce']:015}          |")
                if not short:
                    print(f"        |                                                                  |")
                    print(f"        | Merkle Root:                                                     |")
                    print(f"        | {block['merkleRoot']} |")
                    print(f"        |                                                                  |")
                    print(f"        | Transações:                                                      |")
                    print(f"        | {len(block['transactions']):05}                                                            |")
                    print(f"        |                                                                  |")
                print(f"        +------------------------------------------------------------------+")
                if expanded:
                    if len(block['transactions']):
                        print(f"        |   ---------------======**  Transações  **=====----------------   |")
                    for transaction in block['transactions']:
                        print(f"        | Remetente:                              Timestamp:               |")
                        print(f"        | {transaction['sender']}      {transaction['timestamp']}               |")
                        print(f"        |                                                                  |")
                        print(f"        | Destinatario:                           Quantidade:              |")
                        print(f"        | {transaction['recipient']}      {transaction['amount']:018.14f}       |")
                        if(not transaction==block['transactions'][-1]):
                            print(f"        |        -----------------======****=====-----------------         |")
                        # print(f"        |                             --==--                               |")
                    if len(block['transactions']):
                        print(f"        +------------------------------------------------------------------+")
                print(f"        | Hash do último bloco:                                            |")
                print(f"        | {block['previousHash']} |")
                print(f"        +------------------------------------------------------------------+")
        pass 

    @property
    def prevBlock(self):
        # Retorna o último bloco incluído no blockchain.
        return self.chain[-1]

    @staticmethod
    def getWifCompressedPrivateKey(private_key=None):
        # Retorna a chave privada no formato WIF-compressed da chave privada hex.
        if private_key is None:
            private_key = bitcoinlib.random_key()
        return bitcoinlib.encode_privkey(bitcoinlib.decode_privkey((private_key + '01'), 'hex'), 'wif')
        
    @staticmethod
    def getBitcoinAddressFromWifCompressed(wif_pkey):
        # Retorna o endereço Bitcoin da chave privada WIF-compressed.
        return bitcoinlib.pubtoaddr(bitcoinlib.privkey_to_pubkey(wif_pkey))

    @staticmethod
    def sign(wifCompressedPrivKey, message):
        # Retorna a assinatura digital da mensagem e a respectiva chave privada WIF-compressed.
        return bitcoinlib.ecdsa_sign(message, wifCompressedPrivKey)

    @staticmethod
    def verifySignature(address, signature, message):
        # Verifica se a assinatura é correspondente a mensagem e o endereço BTC.
        # Você pode verificar aqui também: https://tools.bitcoin.com/verify-message/
        return bitcoinlib.ecdsa_verify(message, signature, address)


# Implemente sua API com os end-points indicados no GitHub Classroom.
# Implemente um teste com ao menos 2 nós simultaneos.

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


if __name__ == '__main__':
    app.run(port=5000)