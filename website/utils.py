import csv
import os.path
from typing import Dict
from django.contrib import messages
from django.db.models import query
import requests
from . import models
import random


def read_csv(name,address):
    url = f'https://api.bscscan.com/api?module=account&action=tokenbalance&contractaddress=0x07C0755c5c8Ac1243DEb7498f27EdEDF9b01C5B2&address={address}&tag=latest&apikey=WR57G6APH9W3YV5KXXRB1MNFN3YRWZAZCJ'
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
                    print(jsonResponse)
                    if  7645209056761735667 <= int(jsonResponse["result"]) <= 53408275893513070169:
                        print(int(jsonResponse["result"]))
                        write_to_csv(name,address,"higher_entries")
                        write_to_csv(name,address,"middle_entries")
                        write_to_csv(name,address,"normal_entries")
                        return True
                    elif 3656342574926225508 <= int(jsonResponse["result"]) <= 7645209056761735661:
                        print(int(jsonResponse["result"]))
                        write_to_csv(name,address,"middle_entries")
                        write_to_csv(name,address,"normal_entries")
                        return True
                    elif 824126792052201968 <= int(jsonResponse["result"]) <= 3656342574926225507:
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
    

def lottery_winner(filename, winner_file):
    address_list = []
    with open(f"{filename}.csv", "r") as f:
        r = csv.reader(f)
        for row in r:
            address_list.append(row[1])
    winner  = random.choice(address_list)
    winner2  = random.choice(address_list)
    winner3  = random.choice(address_list)
    print(winner)

    with open(f"{winner_file}.csv", "w") as f:
        writer = csv.writer(f)
        print(winner2)
        print(winner3)
        writer.writerow({winner,winner2,winner3})
    return winner


def read_winner(winner_file):
    winner_list = []
    with open(f"{winner_file}.csv", "r") as f:
        writer = csv.reader(f)
        for name in writer:

            winner_list.append(name)
    print(winner_list)
    return name



    
def reset_winners(filename, winner_file):
    address_list = []

    winner  = "[Coming Soon]"
    winner2  = "[Coming  Soon]"
    winner3  = "[Coming   Soon]"
    print(winner)

    with open(f"{winner_file}.csv", "w") as f:
        writer = csv.writer(f)
        print(winner2)
        print(winner3)
        writer.writerow({winner,winner2,winner3})
    return winner
