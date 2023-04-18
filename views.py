from flask import render_template, jsonify, request, redirect, url_for
import json
import api as api_bitrix
from main import app

data = list()

@app.route('/')
def home_page():
    data = [manager for manager in api_bitrix.all_managers_deals()]
    data.sort(key=lambda x: x[list(x.keys())[0]]['sum/WON'], reverse=True)
    with open('files/plan.json', 'r') as file:
        try:
            planer = json.load(file)
        except:
            planer = {}
    return render_template('home.html', data=data, planer=planer)
@app.route('/planer', methods=['POST'])
def planner():
    if request.method == 'POST':
        with open('files/plan.json', 'r') as file:
            try:
                plan = json.load(file)
            except:
                plan = request.form.to_dict(flat=False) 
        with open('files/plan.json', 'w') as file:
            update_plan = request.form.to_dict(flat=False) 
            for manager in update_plan.keys():
                if len(update_plan[manager]) == 2:
                    if update_plan[manager][0] != '':
                        plan.update({manager: update_plan[manager]})
                    if update_plan[manager][1] != '':
                        try:
                            plan.update({manager: [plan[manager][0], update_plan[manager][1]]})
                        except:
                            plan.update({manager, update_plan[manager]})

            json.dump(plan, file) 
        return redirect(url_for('home_page'))

@app.route('/form')
def form():
    data = [manager for manager in api_bitrix.all_managers_deals()]
    return render_template('form.html', data=data )

@app.route('/json')
def json_t():
    data = [manager for manager in api_bitrix.all_json()]
    return jsonify(data)
