from flask import Flask, redirect, url_for, request
from Queries import queryManager
import json
app = Flask(__name__)

@app.route('/')
def main_page():
    return redirect(url_for('how_to_use'))

@app.route('/country', methods=['GET', 'POST'])
def country_information():
    try:
        country = ''
        year_from = 0
        year_to = 0
        metric = ''
        human_index = ''
        
        if request.method == 'GET':
            country = request.args.get('country')
            year_from = request.args.get('year_from')
            year_to = request.args.get('year_to')
            metric = request.args.get('metric')
            human_index = request.args.get('human_index')
        else:
            country = request.form.get('country')
            year_from = request.form.get('year_from')
            year_to = request.form.get('year_to')
            metric = request.form.get('metric')
            human_index = request.form.get('human_index')
        
        result = queryManager(country, year_from, year_to, metric, human_index)
        
        return json.dumps(result)
    except Exception as e:
        return str(e)

@app.route('/how_to_use')
def how_to_use():
    return "Explanation"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8088)