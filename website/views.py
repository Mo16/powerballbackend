import csv
from django import contrib
from django.shortcuts import render
from . import utils
import random
import json
from django.contrib import messages
import time

# Create your views here.
def index(request):
    
    winner = utils.read_winner()
 
    
    return render(request, 'index.html', {"winner":winner})


def lottery(request):
    if request.method == "POST":
        entry_name = request.POST["name"]
        entry_address = request.POST["address"]
        if utils.read_csv(entry_name,entry_address) == True:
            messages.success(request, "Successfully entered for the lottery!")
        elif utils.read_csv(entry_name,entry_address) == False:
            messages.error(request, "Wallet already in the lottery! Please try another")
    return render(request, 'index.html')

def get_winner(request):
    winner = "[Coming Soon]"
    if request.user.is_superuser:
        if request.POST:
            winner = utils.lottery_winner()
        return render(request, 'get_winner.html', {"winner": winner} )
    return render(request, 'index.html' )
    