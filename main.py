from flask import Flask, jsonify, abort, request, render_template, redirect
from flask_cors import CORS
import pandas as pd
from json import loads

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
	df = pd.read_csv('urls.csv')
	return render_template('index.html', df=df, total_df=len(df))

@app.route('/<url_id>/')
def redirect_to_url(url_id):
	df = pd.read_csv('urls.csv')
	search = df[df['alias'] == url_id]
	if len(search) == 0:
		return abort(404, description="alias not registered")
	else:
		total_hits = int(loads(search.to_json(orient='records'))[0]['hits'])
		df.loc[df['alias'] == url_id, ['hits']] = total_hits + 1

		df.to_csv('urls.csv', index=False)
		search = loads(search.to_json(orient='records'))[0]['url']

		return redirect(search, '302')
	#return render_template('index.html')

@app.route('/records/')
def all_records():
	df = pd.read_csv('urls.csv')
	
	if len(df) == 0:
		data = {
			'entrys': 0,
			'total_hits': 0,
			'total': 0
		}
		return jsonify(data)

	else:
		data = {
			'entrys': loads(df.to_json(orient='records')),
			'total_hits': int(df.sum(axis = 0, numeric_only=True, skipna = True)[0]),
			'total': len(df)
		}
		return jsonify(data)

@app.route('/put/', methods=['POST'])
def register_url():
	data = request.args

	redirect_to = ''

	if data['redirect_to'].startswith('http'):
		redirect_to = data['redirect_to']
	else:
		redirect_to = 'https://' + data['redirect_to']

	df = pd.read_csv('urls.csv')

	if len(df[df['alias'] == data['alias']]) >= 1:
		status = {
			'status': 'fail',
			'message': 'Alias already registered'
		}
		return jsonify(status)

	else:
		df = df.append([{'alias': data['alias'], 'url': redirect_to, 'comment': data['comment'], 'hits': data['hits']}])

		df.to_csv('urls.csv', index=False)

		status = {
			'status': 'success',
			'message': f"{data['alias']} registered"
		}

		return jsonify(status)

@app.route('/del/', methods=['POST'])
def delete_url():
	data = request.args

	df = pd.read_csv('urls.csv')
	delete = df[df['alias'] == data['alias']].index

	df.drop(delete, inplace=True)

	df.to_csv('urls.csv', index=False)

	status = {
		'status': 'success',
		'message': f"{data['alias']} deleted"
	}

	return jsonify(status)
		


app.run(debug=True)