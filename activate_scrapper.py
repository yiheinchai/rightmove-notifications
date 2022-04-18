from rightmove_webscraper import RightmoveData
from discord import Webhook, AsyncWebhookAdapter
import aiohttp
import asyncio
import time
from datetime import datetime
import random

constants = {
    "urls": ["https://www.rightmove.co.uk/property-to-rent/find.html?searchType=RENT&locationIdentifier=REGION%5E91992&insId=1&radius=1.0&minPrice=&maxPrice=&minBedrooms=&maxBedrooms=&displayPropertyType=&maxDaysSinceAdded=&sortByPriceDescending=&_includeLetAgreed=on&primaryDisplayPropertyType=&secondaryDisplayPropertyType=&oldDisplayPropertyType=&oldPrimaryDisplayPropertyType=&letType=&letFurnishType=&houseFlatShare=", "https://www.rightmove.co.uk/property-to-rent/find.html?locationIdentifier=REGION%5E91991&insId=1&numberOfPropertiesPerPage=24&areaSizeUnit=sqft&googleAnalyticsChannel=renting", "https://www.rightmove.co.uk/property-to-rent/find.html?keywords=&sortType=2&viewType=LIST&channel=RENT&index=0&radius=0.0&locationIdentifier=USERDEFINEDAREA%5E%7B%22polylines%22%3A%22qwoyHp_Uo%7E%40dWeBfmBzPpmAxv%40zbCziBfkE%60%5BmCsk%40sqLe%40%7D%40SaDUcBcAaLkBw%5DeDoaAySdJqFuFkRyI_FeI_GbHkUzG%5EzH%22%7D"],
    'webhook':"https://discord.com/api/webhooks/959581742719721502/OZTFE2jTyF_cR7J-Rh15aT2RvU_8RCcpQ3nVvhhWFTau--Ni-5_bd8Gy20d5oodX1Lq7"
}

async def send_message_to_discord(data):
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(
            constants["webhook"], adapter=AsyncWebhookAdapter(session))
        await webhook.send(data)
        print("message sent!")
        return


def get_right_move_data(url, name):
    rm = RightmoveData(url)
    results = rm.get_results
    results["price_per_person"] = results["price"] / results["number_bedrooms"]
    sorted = results.sort_values(["price_per_person", "url"])
    # sorted.to_csv(f"{random.randint(1,100000000)}.csv")
    dictionary = sorted.to_dict("records")
    now = datetime.now()
    time_string = now.strftime("%H:%M:%S")
    print(time_string)
    message = f"======={name}========="
    for i in range(5):
        message += f"""
        {dictionary[i]["address"]}
        Price: £{int(dictionary[i]["price_per_person"] / 31 * 7)} / week
        Location: {dictionary[i]["address"]}
        Rooms: {dictionary[i]["number_bedrooms"]}
        Link: {dictionary[i]["url"]}
        """
    print(message)
    return message


def get_data_and_send(previous_message, url, name):
    cheapest_flat = get_right_move_data(url,name)
    if previous_message != cheapest_flat:
        asyncio.run(send_message_to_discord(cheapest_flat))
    print(previous_message == cheapest_flat)
    return cheapest_flat


# get_data_and_send()

if __name__ == "__main__":
    # imagine you would like to start work in 1 minute first time
    time.sleep(5)
    previous_message_1 = ""
    # previous_message_2 = ""
    while True:
        new_message_1 = get_data_and_send(previous_message_1, constants["urls"][0], "Bloomsbury")
        previous_message_1 = new_message_1
        # new_message_2 = get_data_and_send(previous_message_2, constants["urls"][1], "Marylebone")
        # previous_message_2 = new_message_2
        time.sleep(1800)  # do work every one hour
