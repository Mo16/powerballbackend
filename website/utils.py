import csv
import os.path
from io import StringIO
from typing import Dict
from botocore.retries import bucket
from django.contrib import messages
from django.db.models import query
import requests
from requests.api import head
from . import models
import random
import boto3
import pandas as pd


# access_key = "AKIAW3D7YLFFNOJCLIMO"
# secret_key = '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'
csv_buf = StringIO()

client = boto3.client("s3", aws_access_key_id="AKIAW3D7YLFFNOJCLIMO",aws_secret_access_key='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' )

bucket_name = "powerballbsc"

object_key = "entries/normal_entries.csv"

csv_obj = client.get_object(Bucket=bucket_name,Key=object_key)


def read_csv(name,address):
    url = f'https://api.bscscan.com/api?module=account&action=tokenbalance&contractaddress=0x07C0755c5c8Ac1243DEb7498f27EdEDF9b01C5B2&address={address}&tag=latest&apikey=WR57G6APH9W3YV5KXXRB1MNFN3YRWZAZCJ'
    address_list = []
    client.download_file(bucket_name,"entries/normal_entries.csv","normal_entries.csv")
    client.download_file(bucket_name,"entries/higher_entries.csv","higher_entries.csv")
    client.download_file(bucket_name,"entries/middle_entries.csv","middle_entries.csv")
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
                        write_to_csv(name,address,"higher_entries", "entries")
                        write_to_csv(name,address,"middle_entries", "entries")
                        write_to_csv(name,address,"normal_entries", "entries")
                        return True
                    elif 3656342574926225508 <= int(jsonResponse["result"]) <= 7645209056761735661:
                        print(int(jsonResponse["result"]))
                        write_to_csv(name,address,"middle_entries", "entries")
                        write_to_csv(name,address,"normal_entries", "entries")
                        return True
                    elif 824126792052201968 <= int(jsonResponse["result"]) <= 3656342574926225507:
                        print(int(jsonResponse["result"]))
                        write_to_csv(name,address,"normal_entries", "entries")
                        return True
    return False


def write_to_csv(name,address,filename,s3_folder ):

    field_names = ["Name", "Address"]
    file_exists = os.path.isfile(f"{filename}.csv")
    with open(f"{filename}.csv", "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=field_names)
        if not file_exists:
            writer.writeheader()
        writer.writerow({"Name": name,"Address":address })

    upload_to_aws(filename,s3_folder)



def lottery_winner(filename, winner_file,s3_folder):
    address_list = []
    client.download_file(bucket_name,object_key,"normal_entries.csv")
    with open(f"{filename}.csv", "r") as f:
        r = csv.reader(f)
        for row in r:
            address_list.append(row[1])

    winner  = random.choice(address_list)
    winner2  = random.choice(address_list)
    winner3  = random.choice(address_list)

    with open(f"{winner_file}.csv", "w") as f:
        writer = csv.writer(f)
        print(winner2)
        print(winner3)
        writer.writerow({winner,winner2,winner3})

    upload_to_aws(winner_file,s3_folder)
    return winner


def read_winner(winner_file):
    client.download_file(bucket_name,f"winners/{winner_file}.csv",f"{winner_file}.csv")
    winner_list = []
    with open(f"{winner_file}.csv", "r") as f:
        writer = csv.reader(f)
        for name in writer:
            winner_list.append(name)
    print(winner_list)
    return name



    
def reset_winners(filename, winner_file,s3_folder):
    address_list = []
    winner  = "[Coming Soon]"
    winner2  = "[Coming  Soon]"
    winner3  = "[Coming   Soon]"

    with open(f"{winner_file}.csv", "w") as f:
        writer = csv.writer(f)
        print(winner2)
        print(winner3)
        writer.writerow({winner,winner2,winner3})
    
    upload_to_aws(winner_file,s3_folder)
    return winner


def get_list_total(filename):
    client.download_file(bucket_name,f"entries/{filename}.csv",f"{filename}.csv")
    with open(f"{filename}.csv", "r") as f:
        r = csv.reader(f)
        return sum(1 for row in r)
            

def get_all_entries(filename):
    client.download_file(bucket_name,f"entries/{filename}.csv",f"{filename}.csv")

    with open(f"{filename}.csv", "r") as f:
        r = csv.reader(f)
        return list(r)


def upload_to_aws(filename, s3_folder):
    file = pd.read_csv(f"{filename}.csv")
    file.to_csv(csv_buf,header=True,index=False)
    csv_buf.seek(0)
    client.put_object(Bucket=bucket_name, Key=f"{s3_folder}/{filename}.csv", Body=csv_buf.getvalue())