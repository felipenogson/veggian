from webapp import app
from flask import render_template, flash, request, jsonify
import requests
import random
import json
import os

# Api url
apiUrl = 'https://world.openfoodfacts.org/api/v0/product/'

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/query', methods=['GET', 'POST'])
def query():
	if request.method == "POST":

		# Este codigo es para hacer pruebas, carga los tres archivos json, uno es correcto y los otros dos tienen errores,
		# carga y renderea uno aleatorio 
		jsones =[]
		ingredients = []
		for file in os.listdir():
			if file.endswith('json'):
				with open(file) as f:
					j = json.loads(f.read())
					jsones.append(j)
		data = random.choice(jsones)
		print('Data '+str(data['code'])+ str(data['status']))

		if ('ingredients' not in data['product']) or (data['product'].get('ingredients') == []):
			data['status'] = 0 
			data['status_verbose'] = 'Oh Snap!, there are no ingredients in this product'
		else: 
			ingredients = data['product']['ingredients']

		return render_template('table.html', data=data, ingredients=ingredients ) 

	else: 
		return 'error'
