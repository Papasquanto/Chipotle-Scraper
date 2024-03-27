###################################################################################
#       Developed by Xavier Klvacek 3.19.24                                       #
#       Purpose is to scrape menu information from Chipotle to compare pricing.   #
#                                                                                 #
###################################################################################
import importlib
import subprocess

def install_package(package):
    subprocess.check_call(["pip", "install", package])

required_libraries = ['csv', 'json', 'requests', 'time', 'subprocess', 'random']

print('Checking for required libraries.')
for lib in required_libraries:
    try:
        importlib.import_module(lib)
    except ImportError:
        print(f"{lib} is not installed. Installing...")
        install_package(lib)
        print(f"{lib} has been successfully installed.")
print('All libraries present.')

import csv
import json
import requests
import time
import subprocess
import random

url_base_onlinemenu = "https://services.chipotle.com/menuinnovation/v1/restaurants/{store_id}/onlinemenu"

print('Job 1 starting.')

with open("Stores_we_care_about.json", 'r', encoding='utf-8') as json_file:
    stores_data = json.load(json_file)

headers = {
    "sec-ch-ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122""'
    ,"sec-ch-ua-mobile": "?0"
    ,"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    ,"Ocp-Apim-Subscription-Key": "b4d9f36380184a3788857063bce25d6a"
    ,"Accept": "application/json, text/plain, */*"
    ,"Chipotle-CorrelationId": "OrderWeb-8b447947-ad0d-45d5-ae97-9dd1301dd742"
    ,"Referer": "https://www.chipotle.com/"
    ,"sec-ch-ua-platform": '"Windows"'
}

with open('Chipotle_Menu_Pt_1.csv', 'w', encoding='utf-8', newline='') as CSVFile:
    writer = csv.writer(CSVFile, delimiter=",")
    writer.writerow([
        "Address"
        ,"restaurantNumber"
        ,"restaurantName"
        ,"Item Name"
        ,"Item Type"
        ,"Item Price"
        ,"Item Delivery Price"
        ,"Protein"
    ])

    for store in stores_data['data']:
        store_id = store["restaurantNumber"]
        store_name = store["restaurantName"]
        address = store["addresses"][0]["addressLine1"]

        online_menu_url = url_base_onlinemenu.format(store_id=store_id)
        payload_onlinemenu = {
            "channelId": "web"
            ,"includeUnavailableItems": True
        }

        online_menu_response = requests.get(online_menu_url, headers=headers, params=payload_onlinemenu)
        if online_menu_response.status_code == 200:
            online_menu_data = online_menu_response.json()
            entrees = online_menu_data.get("entrees", [])
            for item in entrees:
                item_name = item.get("itemName", "")
                item_type = item.get("itemType", "")
                item_price = item.get("unitPrice", "")
                item_delivery_price = item.get("unitDeliveryPrice", "")
                protein = item.get("primaryFillingName", "")

                row = [
                    address
                    ,store_id
                    ,store_name
                    ,item_name
                    ,item_type
                    ,item_price
                    ,item_delivery_price
                    ,protein
                ]
                writer.writerow(row)
                print(f'Store {store_id}, Item: {item_name} completed.')
        else:
            print(f"Error retrieving data for store {store_id}. Status code: {online_menu_response.status_code}")

        time.sleep(random.randint(0,5))

print('Job 1 Complete.')

subprocess.run(["python", "Chipotle_Scraper_pt2.py"], check=True)

print('All Jobs Complete.')