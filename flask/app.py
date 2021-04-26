# Demonstrates Bootstrap version 3.3 Starter Template
# available here: https://getbootstrap.com/docs/3.3/getting-started/#examples

from flask import Flask, render_template, request
import pickle
import numpy as np 
import pandas as pd 
from app_funcs import construct_cards, suited_to_int
app = Flask(__name__)

# home page
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/prediction', methods=['POST'] )
def predict():
    """makes prediction using user input data 

    Returns:
        html page: shows variables used to make prediction & prediction 
    """    
    with open('gradient_boost_cap3.pickle', 'rb') as f:
        model = pickle.load(f)

        position = int(request.form['position_num']) / int(request.form['num_players']) # use position_num divided by total players to get 'position' variable
        BB_in_stack = float(request.form['stack']) / float(request.form['BB'])  # use stack divided by BB to get BB_in_stack
        suited = suited_to_int(request.form['suited']) # converts input 'yes/no' to 1/0


        first_val = request.form['first_card_value']
        second_val = request.form['second_card_value']

        
        rank, low_card, high_card = construct_cards(first_val, second_val, suited=suited) # uses card values and suited to get rank, low card, highcard
        
        

        X = pd.DataFrame({'suited': [suited], # putting variables into dataframe
                          'low_card': [low_card],
                          'position': [position], 
                          'high_card': [high_card], 
                          'card_rank': [rank],
                          'limpers': [int(request.form['limpers'])], 
                          'raises&reraises': [int(request.form['raises&reraises'])], 
                          'num_players_before': [int(request.form['num_players_before'])], 
                          'num_players_after': [int(request.form['num_players_after'])],
                          'BB_in_stack': [BB_in_stack]})

        prediction = model.predict_proba(X)[0][1] # get prediction, below we are assigning result based on prediction proba
        if prediction >= 0.62:
            result = 'Play That Hand!'
        if prediction < 0.62 and prediction > 0.53:
            result = 'Caution Zone'
        if prediction <= .53:
            result = "Don't Play It!"

        # X['BB_in_stack'] = X['BB_in_stack'].apply(lambda x: round(x, 2))
    
    if prediction >= 0.62:
        page = f'''
        <table>
            <tr><td><font size=6>Predicted Outcome:</font></td><td><font size =6, color="green">{result}</font></td></tr> 
            <tr><td></td></tr>

            <tr><td><font size=5>Input Data:</font></td><td></td></tr>
            <tr><td></td></tr>

            <tr><td>Card 1 value:</td><td>{request.form['first_card_value']}</td></tr>
            <tr><td>Card 2 value:</td><td>{request.form['second_card_value']}</td></tr>
            <tr><td>Suited:</td><td>{request.form['suited']}</td></tr>
            <tr><td>Card Rank:</td><td>{X['card_rank'].iloc[0]}</td></tr>
            <tr><td>Limpers:</td><td>{X['limpers'].iloc[0]}</td></tr>
            <tr><td>Raises & Reraises:</td><td>{X['raises&reraises'].iloc[0]}</td></tr>
            <tr><td>Number of Players Having Entered Pot:</td><td>{X['num_players_before'].iloc[0]}</td></tr>
            <tr><td>Number of Players Yet to Act:</td><td>{X['num_players_after'].iloc[0]}</td></tr>
            <tr><td>Position:</td><td>{request.form['position_num']}/{request.form['num_players']}</td></tr>
            <tr><td>BB in Stack:</td><td>{round(X['BB_in_stack'].iloc[0], 2)}</td></tr>
        <table>
        <form action="/" method='POST' >        </form>

        '''
    if prediction < 0.62 and prediction > .53:
        page = f'''
        <table>
            <tr><td><font size=6>Predicted Outcome:</font></td><td><font size =6, color="orange">{result}</font></td></tr> 
            <tr><td></td></tr>

            <tr><td><font size=5>Input Data:</font></td><td></td></tr>
            <tr><td></td></tr>

            <tr><td>High Card:</td><td>{X['high_card'].iloc[0]}</td></tr>
            <tr><td>Low Card:</td><td>{X['low_card'].iloc[0]}</td></tr>
            <tr><td>Suited:</td><td>{request.form['suited']}</td></tr>
            <tr><td>Card Rank:</td><td>{X['card_rank'].iloc[0]}</td></tr>
            <tr><td>Limpers:</td><td>{X['limpers'].iloc[0]}</td></tr>
            <tr><td>Raises & Reraises:</td><td>{X['raises&reraises'].iloc[0]}</td></tr>
            <tr><td>Number of Players Having Entered Pot:</td><td>{X['num_players_before'].iloc[0]}</td></tr>
            <tr><td>Number of Players Yet to Act:</td><td>{X['num_players_after'].iloc[0]}</td></tr>
            <tr><td>Position:</td><td>{request.form['position_num']}/{request.form['num_players']}</td></tr>
            <tr><td>BB in Stack:</td><td>{round(X['BB_in_stack'].iloc[0], 2)}</td></tr>
        <table>'''
    if prediction <= 0.53:
        page = f'''
        <table>
            <tr><td><font size=6>Predicted Outcome:</font></td><td><font size =6, color="red">{result}</font></td></tr> 
            <tr><td></td></tr>

            <tr><td><font size=5>Input Data:</font></td><td></td></tr>
            <tr><td></td></tr>

            <tr><td>High Card:</td><td>{X['high_card'].iloc[0]}</td></tr>
            <tr><td>Low Card:</td><td>{X['low_card'].iloc[0]}</td></tr>
            <tr><td>Suited:</td><td>{request.form['suited']}</td></tr>
            <tr><td>Card Rank:</td><td>{X['card_rank'].iloc[0]}</td></tr>
            <tr><td>Limpers:</td><td>{X['limpers'].iloc[0]}</td></tr>
            <tr><td>Raises & Reraises:</td><td>{X['raises&reraises'].iloc[0]}</td></tr>
            <tr><td>Number of Players Having Entered Pot:</td><td>{X['num_players_before'].iloc[0]}</td></tr>
            <tr><td>Number of Players Yet to Act:</td><td>{X['num_players_after'].iloc[0]}</td></tr>
            <tr><td>Position:</td><td>{request.form['position_num']}/{request.form['num_players']}</td></tr>
            <tr><td>BB in Stack:</td><td>{round(X['BB_in_stack'].iloc[0], 2)}</td></tr>
        <table>'''




    return page 








if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, threaded=True, debug=False)
