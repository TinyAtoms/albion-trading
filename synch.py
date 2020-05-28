import json
import requests
from datetime import datetime
from rich.console import Console
from rich.table import Column, Table


with open("items.json", "r") as itfile:
    itemnames = json.load(itfile)

qualities = {
    1 : " normal",
    2 : " good",
    3 : " outstanding",
    4 : " excellent",
    5 : " masterpiece"

}

def fetch_data():
    step = 200
    responses = []
    for i in range(0,5850,step):
        print(i)
        items = ",".join(list(itemnames.keys())[i:i+step])
        url = "https://www.albion-online-data.com/api/v2/stats/prices/{}?locations=3005,3003".format(items)
        content = requests.get(url).content
        toolong = b'<html>\r\n<head><title>414 Request-URI Too Large</title></head>\r\n<body>\r\n<center><h1>414 Request-URI Too Large</h1></center>\r\n<hr><center>nginx/1.16.1</center>\r\n</body>\r\n</html>\r\n'
        if content == toolong:
            print("TOOOOO LONG")
        else:
            responses.append(content)
    black = {}
    caer = {}
    for j in responses:
        j = json.loads(j)
        for item in j:
            name = itemnames[item["item_id"]] + qualities[item["quality"]]
            if item["city"] == "Black Market":
                black[name] = item["buy_price_max"]
            else:
                caer[name] = item["sell_price_min"]
    
    profits = []
    for k in black.keys():
        if not black[k] or not caer[k]:
            continue
        if black[k] < caer[k]:
            continue
        profit = black[k] * 0.94 - caer[k]
        profits.append((profit, black[k] * 0.94, caer[k], k))
    profits = sorted(profits)
    return profits


def print_data(items):
    #list of (blackmarketprice, caer price, itemname)
    console = Console()
    table = Table(show_header=True, header_style="bold green")
    table.add_column("Item")
    table.add_column("Profit(tax removed)")
    table.add_column("Caer price")
    table.add_column("Black market price")
    for i in items:
        if i[0] < 500:
            continue
        row = [i[3], str(i[0]/1000) + "k",str(i[2]/1000) + "k", str(i[1]/1000) + "k"]
        table.add_row(*row)
    console.print(table)
    


print_data(fetch_data())