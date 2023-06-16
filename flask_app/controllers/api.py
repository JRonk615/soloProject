import requests

url = "https://pokedex2.p.rapidapi.com/pokedex/uk/charizard"

headers = {
	"X-RapidAPI-Key": "56c2bc8b30msh20ce65860904590p11203bjsn1ce9c783dc28",
	"X-RapidAPI-Host": "pokedex2.p.rapidapi.com"
}

response = requests.get(url, headers=headers)

print(response.json())
