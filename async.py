import aiohttp
import asyncio
import json


with open("items.json", "r") as jfile:
    items = json.load(jfile)

qualities = {
    1: " normal",
    2: " good",
    3: " outstanding",
    4: " excellent",
    5: " masterpiece"
}

def gen_urls():
    its = sorted(items.keys())
    urls = []
    for i in range(0, 5850, 200):
        curritems = ",".join(its[i:i+200])
        url = f"https://www.albion-online-data.com/api/v2/stats/prices/{curritems}@2?locations=3005,3003"
        urls.append(url)
    return urls


async def fetch(session, url):
    """Execute an http call async
    Args:
        session: contexte for making the http call
        url: URL to call
    Return:
        responses: A dict like object containing http response
    """
    async with session.get(url) as response:
        resp = await response.json()
        return resp

async def fetch_all(urls):
    """ Gather many HTTP call made async
    Args:
        cities: a list of string
    Return:
        responses: A list of dict like object containing http response
    """
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            tasks.append(
                fetch(
                    session,
                    url,
                )
            )
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        return responses


def run(urls):
    responses = asyncio.run(fetch_all(urls))
    return responses


def parser(itemdata):
    caer = {}
    black = {}
    for kindajson in itemdata:
        thing = json.loads(kindajson)
        for item in thing:
            name = items[item["item_id"]] + qualities[item["quality"]]
            if item["city"] == "Black Market":
                black[name] = item["buy_price_max"]
            else:
                caer[name] = item["sell_price_min"]
    profits = []
    for k in black.keys():
        sell = black[k]
        buy = caer[k]
        profit = sell * 0.94 - buy
        if profit > 0:
            row = {
                "black" : sell,
                "caer" : buy,
                "profit" : profit,
                "name" : k
            }
            profits.append(row)
    return profits




links=gen_urls()
responses = run(links)
print(parser(responses))

with open("res.json", "w") as jfile:
    json.dump(responses, jfile)