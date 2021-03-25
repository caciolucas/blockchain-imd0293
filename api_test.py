import requests, json, random
from time import time

NODE_A = 'http://127.0.0.1:5000/'
NODE_B = 'http://127.0.0.1:5001/'

def p(r):
    print(json.dumps(r.json(),indent=2))
sender = '19sXoSbfcQD9K66f5hwP5vLwsaRyKLPgXF' # Você pode gerar novos endereços BTC em https://www.bitaddress.org/
recipient = '1MxTkeEP2PmHSMze5tUZ1hAV3YTKu2Gh1N' # Você pode gerar novos endereços BTC em https://www.bitaddress.org/

# 1. Subir um nó, por exemplo porta 5000 (vou me referir a esse como nó A)

# 2. Subir outro nó, por exemplo porta 5001 (vou me referir a esse como nó B)

# 3. Crie duas transações em A
for y in range(0, 2): 
    timestamp = int(time())
    amount = random.uniform(0.00000001, 100)
    payload = {
                'sender':sender, # remetente da transação;
                'recipient':recipient, # destinatário da transação;
                'amount':amount, # valor a ser transferido do endereço do sender para o endereço do recipient;
                'timestamp':timestamp, # data (formato unix) de criação da transação;
                'privWifKey':'L1US57sChKZeyXrev9q7tFm2dgA2ktJe2NP3xzXRv6wizom5MN1U' # chave privada WIF de quem envia
    }
    print("Transaction Criada em A ".ljust(85,'='))
    p(requests.post(NODE_A+'/transactions/create',payload))
    

# 4. Minere um novo bloco em A
print('Minerando novo bloco em A '.ljust(85,'='))
print(json.dumps(requests.get(NODE_A+'/mine').json(),indent=2))

# 5. Registre em A a informação do nó B.
print('Registrando B em A '.ljust(85,'='))
print(json.dumps(requests.post(NODE_A+'/node/register',{'node_address':'http://127.0.0.1:5001/'}).json(),indent=2))

# 6. Faça a resolução de conflitos em A (/nodes/resolve). Não deve trocar o seu chain.
print('Resolvendo conflitos em A '.ljust(85,'='))
print(json.dumps(requests.get(NODE_A+'/node/resolve').json(),indent=2))

# 7. Crie uma transação em B
print("Transaction Criada em B ".ljust(85,'='))
timestamp = int(time())
amount = random.uniform(0.00000001, 100)
payload = {
            'sender':sender, # remetente da transação;
            'recipient':recipient, # destinatário da transação;
            'amount':amount, # valor a ser transferido do endereço do sender para o endereço do recipient;
            'timestamp':timestamp, # data (formato unix) de criação da transação;
            'privWifKey':'L1US57sChKZeyXrev9q7tFm2dgA2ktJe2NP3xzXRv6wizom5MN1U' # chave privada WIF de quem envia
}
print(json.dumps(requests.post(NODE_B+'/transactions/create',payload).json(),indent=2))

# 8. Minere um novo bloco em B
print('Minerando novo bloco em B'.ljust(85,'='))
print(json.dumps(requests.get(NODE_B+'/mine').json(),indent=2))

# 9. Repita 3x os passos 7 e 8
for y in range(0, 2): 
    # 7. Crie uma transação em B
    print("Transaction Criada em B ".ljust(85,'='))
    timestamp = int(time())
    amount = random.uniform(0.00000001, 100)
    payload = {
                'sender':sender, # remetente da transação;
                'recipient':recipient, # destinatário da transação;
                'amount':amount, # valor a ser transferido do endereço do sender para o endereço do recipient;
                'timestamp':timestamp, # data (formato unix) de criação da transação;
                'privWifKey':'L1US57sChKZeyXrev9q7tFm2dgA2ktJe2NP3xzXRv6wizom5MN1U' # chave privada WIF de quem envia
    }
    print(json.dumps(requests.post(NODE_B+'/transactions/create',payload).json(),indent=2))

    # 8. Minere um novo bloco em B
    print('Minerando novo bloco em B'.ljust(85,'='))
    print(json.dumps(requests.get(NODE_B+'/mine').json(),indent=2))
    
# 10. Faça a resolução de conflitos em A (/nodes/resolve). Deve trocar o seu chain.
print('Resolvendo conflitos em A '.ljust(85,'='))
print(json.dumps(requests.get(NODE_A+'/node/resolve').json(),indent=2))




# # print('Chain:')
# # print(json.dumps(requests.get(BASE_URL+'/chain').json(),indent=2))

# # print('Transactions na mempoll')
# # print(json.dumps(requests.get(BASE_URL+'/transactions/mempool').json(),indent=2))

