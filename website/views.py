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
    normal_winner = utils.read_winner("winner")
    context = {"daily_winner_1":normal_winner[0],
                "daily_winner_2":normal_winner[1],
                "daily_winner_3":normal_winner[2],
    }
    return render(request, 'index.html', context )


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
    total = utils.get_list_total("normal_entries")
    view_csv = utils.get_all_entries("normal_entries")

    winner = "[Coming Soon]"
    normal_winner = [1,2,3]
    if request.user.is_superuser:
        if request.POST:
            winner = utils.lottery_winner("normal_entries","winner","winners")
            normal_winner = utils.read_winner("winner")
            
        return render(request, 'get_winner.html', {"daily_winner_1":normal_winner[0],
                                                    "daily_winner_2":normal_winner[1],
                                                    "daily_winner_3":normal_winner[2],
                                                    "total":total,
                                                    "view_csv":view_csv})
    return render(request, 'index.html' )


def get_higher_winner(request):
    winner = "[Coming Soon]"
    if request.user.is_superuser:
        if request.POST:
            winner = utils.lottery_winner("higher_entries","higher_winner","winners")
        return render(request, 'get_winner.html', {"winner": winner} )
    return render(request, 'index.html' )

    
def reset_winners(request):
    winner = "[Coming soon]"
    if request.user.is_superuser:
        if request.POST:
            winner = utils.reset_winners("normal_entries","winner","winners")
        return render(request, 'get_winner.html', {"winner": winner} )
    return render(request, 'index.html' )