import requests, json, random
from time import time

BASE_URL = 'http://127.0.0.1:5000/'

print('Chain:')
print(json.dumps(requests.get(BASE_URL+'/chain').json(),indent=2))

print('Transactions na mempoll')
print(json.dumps(requests.get(BASE_URL+'/transactions/mempool').json(),indent=2))

sender = '19sXoSbfcQD9K66f5hwP5vLwsaRyKLPgXF' # Você pode gerar novos endereços BTC em https://www.bitaddress.org/
recipient = '1MxTkeEP2PmHSMze5tUZ1hAV3YTKu2Gh1N' # Você pode gerar novos endereços BTC em https://www.bitaddress.org/

for y in range(0, random.randint(1,7)): 
    timestamp = int(time())
    amount = random.uniform(0.00000001, 100)
    payload = {
                'sender':sender, # remetente da transação;
                'recipient':recipient, # destinatário da transação;
                'amount':amount, # valor a ser transferido do endereço do sender para o endereço do recipient;
                'timestamp':timestamp, # data (formato unix) de criação da transação;
                'privWifKey':'L1US57sChKZeyXrev9q7tFm2dgA2ktJe2NP3xzXRv6wizom5MN1U' # chave privada WIF de quem envia
    }
    print(json.dumps(requests.post(BASE_URL+'/transactions/create',payload).json()))


print('Minerando novo bloco')
print(json.dumps(requests.get(BASE_URL+'/mine').json(),indent=2))

print('Chain:')
print(json.dumps(requests.get(BASE_URL+'/chain').json(),indent=2))

print('Transactions na mempoll')
print(json.dumps(requests.get(BASE_URL+'/transactions/mempool').json(),indent=2))

