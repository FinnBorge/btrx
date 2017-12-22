import requests
import json
import csv
from time import gmtime, strftime

# TODO: requests has json -- requests.get(..).json

datestamp = strftime("%Y-%m-%d", gmtime())

# Get MarketSummary
get_markets = "https://bittrex.com/api/v1.1/public/getmarketsummaries"
market = requests.get(get_markets).text
x = json.loads(market)["result"]

# USDT
btc_results = []
for coin in x:
    if "BTC-" in coin["MarketName"]:
        btc_results.append(coin)

# Build CSV #
summary_filename = "summaries-" + datestamp + ".csv"
with open(summary_filename, "w") as summaries_csv:
    f = csv.writer(summaries_csv)
    name_list = []
    f.writerow(x[0].keys())
    for coin in btc_results:
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

# Get & Write Social Data Individual TXT
social_data_dictionary = []
for comparable_id in coin_ids:
    url = "https://www.cryptocompare.com/api/data/socialstats/?id=" + comparable_id
    social_request = requests.get(url).text
    social_json = json.loads(social_request)["Data"]
    filename = datestamp + "-" + comparable_id + ".txt"
    social_data_dictionary.append(social_json)
    with open(filename, 'w') as social_txt:
        social_txt.write("%s" % social_json)

# Use Social Data Dictionary to write CSV
social_filename = "socialdata-" + datestamp + ".csv"
with open(social_filename, "w") as social_csv:
    wr = csv.writer(social_csv)
    wr.writerow(social_data_dictionary[0].keys())
    for coin in social_data_dictionary:
        wr.writerow(coin.values())
        
# Market Cap
mktcap_request = requests.get('https://api.coinmarketcap.com/v1/ticker/?start=0&limit=1000')
mktcap_text = mktcap_request.text
mktcap_json = json.loads(mktcap_text)
mktcap_filename = "mktcap-" + datestamp + ".csv"
with open(mktcap_filename, "w") as mktcap_csv:
    f = csv.writer(mktcap_csv)
    f.writerow(x[0].keys())
    for coin in mktcap_json:
        f.writerow(coin.values())
