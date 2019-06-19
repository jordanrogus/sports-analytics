'''
astopa

'''
# create flask app

from flask import Flask, flash, redirect, render_template, request, session, abort

import json, csv, os

from api.dataCleansing import getNFLdata

import pandas as pd

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about/')
def about():
    return render_template('about.html')
    
@app.route('/get-nfl-reception-data', methods=['POST'])
def get_nfl_reception_data():
    testData_df = getNFLdata(int(request.get_data().decode('utf8')))
    return_str = '{"__data__":' + str(testData_df.to_json(orient='records')) + '}'
    return return_str

if __name__ == "__main__":
    app.run(debug=True)