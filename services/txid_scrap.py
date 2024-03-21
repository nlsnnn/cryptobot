import requests


def check_txid(txid) -> bool:
    url = 'https://apilist.tronscanapi.com/api/transaction-info?hash'
    response = requests.get(f'{url}={txid}')

    data = response.json()
    req_address = data['tokenTransferInfo']['to_address']
    req_amount = int(int(data['tokenTransferInfo']['amount_str']) / 1000000)

    if req_address == 'TAxpEcVN4a9iu3JYUJeb7VShmHayRLo2n8':
            return req_amount
    return False
