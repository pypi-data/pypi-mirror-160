import requests
import json 

url = "https://api-testnet.dragonglass.me/hedera/api/accounts/0.0.47728252/files"

payload = {}
headers = {
    'X-API-KEY': '7c68843c-bcc4-3b7b-92d9-ad1937294a91',
    'accept': 'application/json'
}

response = requests.request("GET", url, headers=headers, data = payload, verify=False)
json_response = response.json()
print(json_response)