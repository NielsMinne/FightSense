import os
from wsgiref.headers import Headers
from supabase import create_client, Client
import requests
import json
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_HEADERS = {
    'apikey' : os.getenv('SUPABASE_API_KEY'),
    'Authorization' : "Bearer " + os.getenv('SUPABASE_API_KEY')
}

def createPlayer(uid,username):
    data= {"uid": uid, "username":username,"owned_characters": "1" ,"coins": 0}
    response = requests.post(f'{SUPABASE_URL}/rest/v1/Users', headers=SUPABASE_HEADERS, data = data)
    return response


def signup(username, password):
    url: str = os.getenv("SUPABASE_URL")
    key: str = os.getenv("SUPABASE_AUTH_KEY")
    supabase: Client = create_client(url, key)

    random_email: str = username + "@fightsense.com"
    random_password: str = password

    user = supabase.auth.sign_up(email=random_email, password=random_password)
    returnedUser = user.user
    createPlayer(user.user.id,username)
    return returnedUser

def login(username,password):
    url: str = os.getenv("SUPABASE_URL")
    key: str = os.getenv("SUPABASE_AUTH_KEY")
    supabase: Client = create_client(url, key)

    random_email: str = username + "@fightsense.com"
    random_password: str = password

    user = supabase.auth.sign_in(email=random_email, password=random_password)
    returnedUser = user.user
    return returnedUser

def signUpOrLogin(username,password):
    try:
        return signup(username,password)
    except:
        try:
            return login(username,password)
        except:
            print("credentials not correct or user already exists")
    


    


def getCharacters():
    url: str = os.getenv("SUPABASE_URL")
    key: str = os.getenv("SUPABASE_AUTH_KEY")
    supabase: Client = create_client(url, key)
    data = supabase.table("Characters").select("*").order('id').execute()
    # Assert we pulled real data.
    characters = data.data
    return characters


def getUserDetails(uid):
    response = requests.get(f'{SUPABASE_URL}/rest/v1/Users?uid=eq.{uid}&select=*', headers=SUPABASE_HEADERS)
    jsonResponse = json.loads(response.text)
    user = jsonResponse
    return user

def getOwnedCharacters(uid):
    response = requests.get(f'{SUPABASE_URL}/rest/v1/Users?uid=eq.{uid}&select=*', headers=SUPABASE_HEADERS)
    jsonResponse = json.loads(response.text)
    characters = jsonResponse[0]['owned_characters']
    return characters

def getCharacterCoins(uid):
    response = requests.get(f'{SUPABASE_URL}/rest/v1/Users?uid=eq.{uid}&select=*', headers=SUPABASE_HEADERS)
    jsonResponse = json.loads(response.text)
    coins = jsonResponse[0]['coins']
    return coins


def buyCharacter(number, uid):
    # SUPABASE_HEADERS['Content-Type'] = 'application/json'
    # SUPABASE_HEADERS['Prefer'] = 'return=representation'
    allCharacters = getCharacters()
    coins = getCharacterCoins(uid)
    
    characterCost = allCharacters[number-1]['cost']
    characters = getOwnedCharacters(uid)

    newCharacters = characters + "," + str(number)
    
    if coins - characterCost > 0:
        newCoins = coins - characterCost
        coinData = {"coins" : newCoins}
        response = response = requests.patch(f'{SUPABASE_URL}/rest/v1/Users?uid=eq.{uid}',headers=SUPABASE_HEADERS, json=coinData)
    else:
        text ="error"
        return text

    data = {"owned_characters" : newCharacters}
    response = requests.patch(f'{SUPABASE_URL}/rest/v1/Users?uid=eq.{uid}',headers=SUPABASE_HEADERS, json=data)
    return ""

def addCoins(uid,coins):
    userCoins = getCharacterCoins(uid)
    newCoins = userCoins + coins
    data = {"coins" : newCoins}
    response = requests.patch(f'{SUPABASE_URL}/rest/v1/Users?uid=eq.{uid}',headers=SUPABASE_HEADERS, json=data)
    return response.text

def setHighscores(username,floor,enemy):
    data = {"username": username, "floor": floor , "enemy": enemy}
    response = requests.post(f'{SUPABASE_URL}/rest/v1/Highscores', headers=SUPABASE_HEADERS, data = data)
    return response.text

def setActiveCharacter(number):
    data = {"activeCharacter" : number}
    response = requests.patch(f'{SUPABASE_URL}/rest/v1/Users?uid=eq.489b22ac-bedf-4750-b5c4-ef5121d1bd8b',headers=SUPABASE_HEADERS, json=data)
    return response.text

def getHighscores():
    url: str = os.getenv("SUPABASE_URL")
    key: str = os.getenv("SUPABASE_AUTH_KEY")
    supabase: Client = create_client(url, key)
    data = supabase.table("Highscores").select("*").limit(10).order('floor',desc=True).execute()
    # Assert we pulled real data.
    scores = data.data
    return scores


