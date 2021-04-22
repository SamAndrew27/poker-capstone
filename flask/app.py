# Demonstrates Bootstrap version 3.3 Starter Template
# available here: https://getbootstrap.com/docs/3.3/getting-started/#examples

from flask import Flask, render_template, request
import pickle
import numpy as np 
import pandas as pd 
from app_funcs import construct_cards
app = Flask(__name__)

# home page
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/prediction', methods=['POST'] )
def predict():
    with open('gradient_boost_cap3.pickle', 'rb') as f:
        model = pickle.load(f)

        position = int(request.form['position_num']) / int(request.form['num_players'])


        first_val = request.form['first_card_value']
        first_suit = request.form['first_card_suit']
        second_val = request.form['second_card_value']
        second_suit = request.form['second_card_value_suit']
        
        rank, suited, low_card, high_card = construct_cards(first_val, second_val, first_suit, second_suit)
        
        

        X = pd.DataFrame({'suited': [suited], 
                          'low_card': [low_card],
                          'position': [position], 
                          'high_card': [high_card], 
                          'card_rank': [rank],
                          'limpers': [float(request.form['limpers'])], 
                          'raises&reraises': [float(request.form['raises&reraises'])], 
                          'num_players_before': [float(request.form['num_players_before'])], 
                          'num_players_after': [float(request.form['num_players_after'])],
                          'BB_in_stack': [float(request.form['BB_in_stack'])]})

        prediction = model.predict(X)[0]
        if prediction == 1:
            result = 'Play That Hand!'
        else:
            result = 'Skip This One!'

        prob = model.predict_proba(X)[0][1]
    page = f'''Predicted Outcome:
    <table>
        <tr><td>prediction</td><td>{result}</td></tr>
        <tr><td>prediction probability</td><td>{prob}</td></tr>
        <tr><td>rank</td><td>{rank}</td></tr>

    <table>'''

    return page 








if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, threaded=True, debug=False)
