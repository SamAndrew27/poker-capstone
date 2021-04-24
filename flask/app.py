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
        BB_in_stack = float(request.form['stack']) / float(request.form['BB']) 

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
                          'BB_in_stack': [BB_in_stack]})

        prediction = model.predict_proba(X)[0][1]
        if prediction >= 0.655:
            result = 'Play That Hand!'
        if prediction < 0.655 and prediction > 0.595:
            result = 'Probable Win'
        if prediction <= 0.595 and prediction > 0.51:
            result = "Probable Loss"
        if prediction <= .51:
            result = "Don't Play It!"

        # X['BB_in_stack'] = X['BB_in_stack'].apply(lambda x: round(x, 2))

    page = f'''
    <table>
        <tr><td>Predicted Outcome:</td><td>{result}</td></tr>

        <tr><td>Input Data:</td><td></td></tr>
        <tr><td>High Card:</td><td>{X['high_card'].iloc[0]}</td></tr>
        <tr><td>Low Card:</td><td>{X['low_card'].iloc[0]}</td></tr>
        <tr><td>Suited:</td><td>{X['suited'].iloc[0]}</td></tr>
        <tr><td>Card Rank:</td><td>{X['card_rank'].iloc[0]}</td></tr>
        <tr><td>Limpers:</td><td>{X['limpers'].iloc[0]}</td></tr>
        <tr><td>Raises & Reraises:</td><td>{X['raises&reraises'].iloc[0]}</td></tr>
        <tr><td>Number of Players Having Entered Pot:</td><td>{X['num_players_before'].iloc[0]}</td></tr>
        <tr><td>Number of Players Yet to Act:</td><td>{X['num_players_after'].iloc[0]}</td></tr>
        <tr><td>Position:</td><td>{round(X['position'].iloc[0], 2)}</td></tr>
        <tr><td>BB in Stack:</td><td>{round(X['BB_in_stack'].iloc[0], 2)}</td></tr>



    <table>'''

    return page 








if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, threaded=True, debug=False)
