import requests

resposta = requests.get("https://pypi.org/pypi/flask/json", timeout=5)
info = resposta.json()["info"]

print(info["name"])
print(info["version"])
print(info["summary"])