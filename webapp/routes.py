from webapp import app
from flask import render_template, flash, request, jsonify
from helpers import get_recipes_api
import requests
import json
import random

# Api url
apiUrl = 'https://world.openfoodfacts.org/api/v0/product/'

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/query', methods=['GET', 'POST'])
def query():
	if request.method == 'POST':
		query = request.form['query']
		response = requests.get(apiUrl + request.form['query'] + '.json')
		data = json.loads(response.text)
		ingredients = []
		stop_words = ['food', 'their', 'america', 'value', 'great', 'base', 'fabrique', 'dell', 'non-ue', 'nl-bio-01', 'sale', 'salee']
		word = ''

		if data['status'] == 1:
			if ('ingredients' not in data['product']) or (data['product'].get('ingredients') == []):
				data['status'] = 0 
				data['status_verbose'] = 'Oh Snap!, there are no ingredients in this product'
			else: 
				ingredients = data['product']['ingredients']
				word = random.choice( [word for word in data['product']['_keywords'] if (word not in stop_words) and ( len(word) > 3)])

		return render_template('table.html', data=data, ingredients=ingredients, word=word ) 

	else: 
		return 'error', 505


@app.route('/scanner', methods=['GET', 'POST'])
def scanner():
	return render_template('modal.html')

@app.route('/recipes/<ingredient>', methods=['GET', 'POST'])
def recipes(ingredient):
	print(ingredient)
	recipes = get_recipes_api(ingredient)
	return render_template('recipes.html', recipes=recipes )