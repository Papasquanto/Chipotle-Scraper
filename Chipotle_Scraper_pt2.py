###################################################################################
#         Developed by Xavier Klvacek 3.19.24                                     #
#       Purpose is to scrape menu information from Chipotle to compare pricing.   #
#                                                                                 #
###################################################################################


import csv
import json
import requests
import time
import random

url_base_onlinemeals = "https://services.chipotle.com/menuinnovation/v1/restaurants/{store_id}/onlinemeals?includeUnavailableItems=true"

with open("Stores_we_care_about.json", 'r', encoding='utf-8') as json_file:
    stores_data = json.load(json_file)

headers = {
    'sec-ch-ua': 'Chromium;v=122, Not(A:Brand";v=24, "Google Chrome";v=122"'
    ,'sec-ch-ua-mobile': '?0'
    ,'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    ,'Ocp-Apim-Subscription-Key': 'b4d9f36380184a3788857063bce25d6a'
    ,'Accept': 'application/json, text/plain, */*'
    ,'Chipotle-CorrelationId': 'OrderWeb-6b6fea78-55ab-4bca-8597-dcf7d450b3b1'
    ,'Referer': 'https://www.chipotle.com/'
    ,'sec-ch-ua-platform': 'Windows'
}

print('Starting Job 2.')

with open('Chipotle_Menu_Pt_2.csv', 'w', encoding='utf-8', newline='') as CSVFile:
    writer = csv.writer(CSVFile, delimiter=",")
    writer.writerow([
        "Address"
        ,"restaurantNumber"
        ,"restaurantName"
        ,"Meal Name"
        ,"Meal Price"
        ,"Meal Delivery Price"
    ])

    for store in stores_data['data']:
        store_id = store["restaurantNumber"]
        store_name = store["restaurantName"]
        address = store["addresses"][0]["addressLine1"]

        online_menu_url = url_base_onlinemeals.format(store_id=store_id)
        payload_onlinemeals = {
            "calories": "850"
            ,"mealTags": []
            ,"dietaryTags": []
        }
        online_meals_response = requests.get(online_menu_url, headers=headers, params=payload_onlinemeals)
        online_meals_data = online_meals_response.json()

        for content in online_meals_data:
            meal_name = content.get("mealName", "")
            meal_price = content.get("mealPrice", "")
            meal_delivery_price = content.get("mealDeliveryPrice", "")

            row = [
                address
                ,store_id
                ,store_name
                ,meal_name
                ,meal_price
                ,meal_delivery_price
            ]

            writer.writerow(row)
            print(f'Store {store_id}, Meal: {meal_name} completed.')

        time.sleep(random.randint(1,5))

print('Job 2 Complete.')
