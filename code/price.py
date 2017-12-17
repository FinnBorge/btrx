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
with open("summaries.csv", "w") as summaries_csv:
    f = csv.writer(summaries_csv)
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

# Get & Write Social Data Individual TXT
social_data_dictionary = []
for comparable_id in coin_ids:
    url = "https://www.cryptocompare.com/api/data/socialstats/?id=" + comparable_id
    social_request = requests.get(url).text
    social_json = json.loads(social_request)["Data"]
    filename = comparable_id + ".txt"
    social_data_dictionary.append(social_json)
    with open(filename, 'w') as social_txt:
        social_txt.write("%s" % social_json)

# Use Social Data Dictionary to write CSV
with open("socialdata.csv", "w") as social_csv:
    wr = csv.writer(social_csv)
    wr.writerow(social_data_dictionary[0].keys())
    for coin in social_data_dictionary:
        wr.writerow(coin.values())
