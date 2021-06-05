import csv
import os.path
from typing import Dict
from django.contrib import messages
from django.db.models import query
import requests
from . import models
import random


def read_csv(name,address):
    url = f'https://api.bscscan.com/api?module=account&action=tokenbalance&contractaddress=0x742eabb2538b3fdd79825eeb3b0e2a51863f456f&address={address}&tag=latest&apikey=WR57G6APH9W3YV5KXXRB1MNFN3YRWZAZCJ'
    address_list = []
    with open("normal_entries.csv", "r") as f:
        r = csv.reader(f)
        for row in r:
            address_list.append(row[1])
        if address.startswith("0x"):
            if len(address) == 42:
                if address not in address_list:
                    response = requests.get(url)
                    jsonResponse = response.json()
                    if  8963113495914575851 <= int(jsonResponse["result"]) <= 913563103851792183721:
                        print(int(jsonResponse["result"]))
                        write_to_csv(name,address,"higher_entries")
                        write_to_csv(name,address,"normal_entries")
                        return True
                    elif 6850772581124411325 <= int(jsonResponse["result"]) <= 8963113495914575850:
                        print(int(jsonResponse["result"]))
                        write_to_csv(name,address,"normal_entries")
                        return True
        
    return False


def write_to_csv(name,address,filename):
    field_names = ["Name", "Address"]
    file_exists = os.path.isfile(f"{filename}.csv")
    with open(f"{filename}.csv", "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=field_names)
        if not file_exists:
            writer.writeheader()
        writer.writerow({"Name": name,"Address":address })
    

def lottery_winner():
    address_list = [] 
    with open("normal_entries.csv", "r") as f:
        r = csv.reader(f)
        for row in r:
            address_list.append(row[1])
    winner = random.choice(address_list)

    with open("winner.csv", "w") as f:
        writer = csv.writer(f)
        print(winner)
        writer.writerow({winner})
    return winner


def read_winner():
    winner_list = []
    with open("winner.csv", "r") as f:
        writer = csv.reader(f)  
        for name in writer:
            winner_list.clear()
            winner_list.append(name[0])
    winner = random.choice(winner_list)
    return winner




