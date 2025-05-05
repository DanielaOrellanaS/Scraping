import requests

url = "https://api.alternative.me/fng/"
response = requests.get(url)
print(response.json())
