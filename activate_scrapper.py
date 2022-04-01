from rightmove_webscraper import RightmoveData
from discord import Webhook, AsyncWebhookAdapter
import aiohttp
import asyncio
import time


async def send_message_to_discord(data):
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(
            'https://discord.com/api/webhooks/959581742719721502/OZTFE2jTyF_cR7J-Rh15aT2RvU_8RCcpQ3nVvhhWFTau--Ni-5_bd8Gy20d5oodX1Lq7', adapter=AsyncWebhookAdapter(session))
        await webhook.send(data)
        print("message sent!")


def get_right_move_data():
    url = "https://www.rightmove.co.uk/property-to-rent/find.html?locationIdentifier=REGION%5E91992&radius=1.0&propertyTypes=&includeLetAgreed=false&mustHave=&dontShow=&furnishTypes=&keywords="
    rm = RightmoveData(url)

    results = rm.get_results
    results["price_per_person"] = results["price"] / results["number_bedrooms"]
    sorted = results.sort_values("price_per_person")
    dictionary = sorted.to_dict("records")
    message = f"""
    {dictionary[0]["address"]}
    Price: £{int(dictionary[0]["price_per_person"] / 31 * 7)} / week
    Location: {dictionary[0]["address"]}
    Rooms: {dictionary[0]["number_bedrooms"]}

    {dictionary[1]["address"]}
    Price: £{int(dictionary[1]["price_per_person"] / 31 * 7)} / week
    Location: {dictionary[1]["address"]}
    Rooms: {dictionary[1]["number_bedrooms"]}

    {dictionary[2]["address"]}
    Price: £{int(dictionary[2]["price_per_person"] / 31 * 7)} / week
    Location: {dictionary[2]["address"]}
    Rooms: {dictionary[2]["number_bedrooms"]}
    """
    print(message)
    return message


def get_data_and_send(previous_message):
    cheapest_flat = get_right_move_data()
    if previous_message != cheapest_flat:
        asyncio.run(send_message_to_discord(cheapest_flat))
    print(previous_message == cheapest_flat)
    return cheapest_flat


# get_data_and_send()

if __name__ == "__main__":
    # imagine you would like to start work in 1 minute first time
    time.sleep(5)
    previous_message = ""
    while True:
        new_message = get_data_and_send(previous_message)
        previous_message = new_message
        time.sleep(60)  # do work every one hour
