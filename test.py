import requests

BASE = "http://127.0.0.1:5000/"

response = requests.get(BASE + "allcompanies/ds/BOGOTÁ/6")
print(response.json())

x = input('')

response = requests.get(BASE + "bestfit/OLIMPIA/BOGOTÁ/8")
print(response.json())