import os
import yaml
import requests
import subprocess
from jinja2 import Environment, PackageLoader
from hedera import Client, AccountId, PrivateKey, Hbar, FileCreateTransaction, FileContentsQuery, FileId, FileAppendTransaction, FileInfoQuery

OPERATOR_ID= AccountId.fromString(os.environ["OPERATOR_ID"])
OPERATOR_PRIVATE_KEY= PrivateKey.fromString(os.environ["OPERATOR_PRIVATE_KEY"])

url = "https://api-testnet.dragonglass.me/hedera/api/accounts"
#url = f"https://api-testnet.dragonglass.me/hedera/api/accounts/{ OPERATOR_ID }/files"
payload = {}
headers = {
    'X-API-KEY': f'{ OPERATOR_PRIVATE_KEY }'
    }
response = requests.request("GET", url, headers=headers, data = payload)

print(response.text.encode('utf8'))