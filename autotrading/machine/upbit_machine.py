import requests

url = "https://api.upbit.com/v1/ticker"
querystring = {"markets":"KRW-XRP"}

response = requests.request("GET", url, params=querystring)

print(response.json())

for k, v in response.json()[0].items():
    print("{} 는 {}".format(k, v))

print(response.json()[0]["trade_price"])

