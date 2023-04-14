from flask import render_template, jsonify
import api as api_bitrix
from main import app

@app.route('/')
def home_page():
    data = [manager for manager in api_bitrix.all_managers_deals()]
    data.sort(key=lambda x: x[list(x.keys())[0]]['sum/WON'], reverse=True)
    return render_template('home.html', data=data)
@app.route('/json')
def json():
    data = [manager for manager in api_bitrix.all_json()]
    return jsonify(data)
