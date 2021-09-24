# coding: utf-8
import requests_random_user_agent, requests
from pyzbar.pyzbar import decode
from bs4 import BeautifulSoup
from urllib import parse
import json
import random
import cv2

url = 'https://www.epicurious.com'

def get_recipes_api(search:str, items:int = 9):
    ''' It search for recipes in the epicurious.com using it api, it return an array with {items} number or [recipies] '''
    search = parse.quote(search)
    api_url = f'https://origin-services.epicurious.com/api/search/v1/query?q={search}&size=1000&special-consideration=vegetarian&include=&exclude='
    image_url = 'https://assets.epicurious.com/photos/5f9b242994e855aa19462124/6:4/w_352,h_417,c_limit/Brad-Grilling-Mushroom-Antipasto-Salad_V1_test.jpg'
    req = requests.get(api_url)
    data = json.loads(req.text)
    if data['numFound'] == 0:
        return f'Sorry we did not find any recipe with the term {search}'

    # Whe get just the recipes from data and the ones with nice pictures
    recipes_from_api = [ rec for rec in data['items'] if rec['type'] == 'recipe' and (rec['photoData']['filename'].startswith('no-recipe') == False)]

    if len(recipes_from_api) >= items:
        recipes_from_api = random.sample(recipes_from_api, items)

    recipes = []
    for item in recipes_from_api:
        recipe = {}
        item['photoData']
        img_url = f"https://assets.epicurious.com/photos/{item['photoData']['id']}/6:4/w_352,h_417,c_limit/{item['photoData']['filename']}"
        if item['author']:
            recipe['author'] = item['author'][0]['name']
        else:
            recipe['author'] = ''
        recipe['title'] = item['hed']
        recipe['description'] = item['dek']
        recipe['url'] = url + item['url']
        recipe['picture'] = [img_url, item['photoData']['caption']]
        recipes.append(recipe)
    return recipes

def get_recipes(search):
    ''' it search recipes from https://epicurious.com web site using scrapping tools to get the data,
    it lacks for pictures, use the get_recipes_api function instead '''

    # Variables for the request 
    search = parse.quote(search)
    options = '?special-consideration=vegetarian'
    url = 'https://www.epicurious.com'
    url_search = 'https://www.epicurious.com/search/'
    r = requests.get(url_search+search+options)

    recipes = []

    #in case of a not succesful http request
    if r.status_code != 200:
        recipe = {} 
        recipe['error'] = 1
        recipe['description'] = f" Sorry there was a http {r.status_code} error code"
        return recipe
    
    soup = BeautifulSoup(r.text, 'html.parser')
    articles = soup.select('article')

    for article in articles:
        # breakpoint()
        recipe = {}
        if (article.select('header.summary>strong.tag')) and (article.select('header.summary>strong.tag')[0].text == 'recipe'):
            recipe['error'] = 0
            recipe['title'] = article.select('h4')[0].text
            recipe['description'] = article.select('p')[0].text
            recipe['url'] = url + article.select('a')[0]['href']
            recipes.append(recipe)

    return recipes 

def BarcodeReader(image):
    
    img = cv2.imread(image)
    detectedBarcode = decode(img)
    barcodes = []
    if not detectedBarcode:
        print('No se detectaron codigos')
    else:
        for barcode in detectedBarcode:
            (x,y,w,h) = barcode.rect
            cv2.rectangle(img, (x-10, y-10), (x + w+10, y + h+10), (255,0,0), 2)
            if barcode.data!='':
                barcodes.append((barcode.type, barcode.data))
                # print(barcode.data)
                # print(barcode.type)
    # cv2.imshow('Image', img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return barcodes

def open_food_api(query:str):
    apiUrl = 'https://world.openfoodfacts.org/api/v0/product/'
    query = str(query)

    response = requests.get(apiUrl + query + '.json')
    data = json.loads(response.text)
    ingredients = []

    if data['status'] == 1:
        if ('ingredients' not in data['product']) or (data['product'].get('ingredients') == []):
            data['status'] = 0 
            data['status_verbose'] = 'Oh Snap!, there are no ingredients in this product'
        else: 
            ingredients = data['product']['ingredients']
    return (data, ingredients)