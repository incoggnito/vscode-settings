import requests

headers = { 'accept': 'application/json', 'X-AUTH-TOKEN': '8!%^ae8TNz5C', }
 response = requests.get('https://kimai.amitronics.net/api/activities', headers=headers)
 print(response.text)