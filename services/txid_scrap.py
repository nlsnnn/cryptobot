import requests


def check_txid(txid, address) -> bool:
    url = 'https://apilist.tronscanapi.com/api/transaction-info?hash'
    response = requests.get(f'{url}={txid}')

    data = response.json()
    req_address = data['tokenTransferInfo']['to_address']
    req_amount = int(int(data['tokenTransferInfo']['amount_str']) / 1000000)
    flag = data['confirmed']

    if flag:
        if req_address == address:
            return req_amount
    return False
