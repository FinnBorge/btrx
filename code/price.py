import requests
import json
import csv

# Get MarketSummary
get_markets = "https://bittrex.com/api/v1.1/public/getmarketsummaries"
market = requests.get(get_markets).text
x = json.loads(market)["result"]

# USDT
usdt_results = []
for coin in x:
    if "USDT-" in coin["MarketName"]:
        usdt_results.append(coin)

# Build CSV #
f = csv.writer(open("../summaries.csv", "w"))
name_list = []
f.writerow(x[0].keys())
for coin in usdt_results:
    f.writerow(coin.values())
    for each in coin["MarketName"].split("-"):
        name_list.append(each)

# Unique List #
name_set = set(name_list)

# Coin Ids #
get_coin_ids = "https://www.cryptocompare.com/api/data/coinlist/"
coin_ids_response = requests.get(get_coin_ids).text
coin_ids_json = json.loads(coin_ids_response)["Data"]
coin_ids = []
for market in name_set:
    if market in coin_ids_json.keys():
        coin_ids.append(coin_ids_json[market]["Id"])
print(coin_ids)

for comparable_id in coin_ids:
    url = "https://www.cryptocompare.com/api/data/socialstats/?id=" + comparable_id
    social_request = requests.get(url).text
    social_json = json.loads(social_request)["Data"]
    filename = "../data/" + comparable_id + ".txt"
    thefile = open(filename, 'w')
    thefile.write("%s" % social_json)

# TODO: with open('file') as sth:
#    write.....
