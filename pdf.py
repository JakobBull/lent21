import requests
url = "https://api.mathpix.com/v3/pdf-file"
payload = {}
files = [
  ('file', open('FULL-PATH-TO-YOUR-FILE','rb'))
]
headers = {
  'app_id': 'YOUR_APP_ID',
  'app_key': 'YOUR_APP_KEY'
}
response = requests.request("POST", url, headers=headers, data = payload, files = files)
print(response.text.encode('utf8'))