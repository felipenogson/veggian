from webapp import app
from flask import render_template, flash, request, jsonify
import requests
import json

# Api url
apiUrl = 'https://world.openfoodfacts.org/api/v0/product/'

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/query', methods=['GET', 'POST'])
def query():
	if request.method == 'POST':
		response = requests.get(apiUrl + request.form['query'] + '.json')
		data = json.loads(response.text)
		ingredients = []

		if data['status'] == 1:
			if ('ingredients' not in data['product']) or (data['product'].get('ingredients') == []):
				data['status'] = 0 
				data['status_verbose'] = 'Oh Snap!, there are no ingredients in this product'
			else: 
				ingredients = data['product']['ingredients']

		return render_template('table.html', data=data, ingredients=ingredients ) 

	else: 
		return 'error', 505


@app.route('/scanner', methods=['GET', 'POST'])
def scanner():
	return render_template('scanner.html')