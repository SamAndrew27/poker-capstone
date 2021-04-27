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
    with open('models/final_model.pickle', 'rb') as f:
        model = pickle.load(f)

        position = int(request.form['position_num']) / int(request.form['num_players']) # use position_num divided by total players to get 'position' variable
        BB_in_stack = float(request.form['stack']) / float(request.form['BB'])  # use stack divided by BB to get BB_in_stack
        suited = suited_to_int(request.form['suited']) # converts input 'yes/no' to 1/0


        first_card = request.form['first_card_value']
        second_card = request.form['second_card_value']

        
        rank, low_card, high_card = construct_cards(first_card, second_card, suited=suited) # uses card values and suited to get rank, low card, highcard
        
        

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

            <tr><td><font size=4>First Card</font></td><td><b><font size=4>{first_card.capitalize()}</font><b></td></tr>
            <tr><td><font size=4>Low Card:</font></td><td><b><font size=4>{second_card.capitalize()}</font><b></td></tr>
            <tr><td><font size=4>Suited:</font></td><td><b><font size=4>{request.form['suited'].capitalize()}</font><b></td></tr>
            <tr><td><font size=4>Card Rank:</font></td><td><b><font size=4>{X['card_rank'].iloc[0]}</font><b></td></tr>
            <tr><td><font size=4>Limpers:</font></td><td><b><font size=4>{X['limpers'].iloc[0]}</font><b></td></tr>
            <tr><td><font size=4>Raises & Reraises:</font></td><td><b><font size=4>{X['raises&reraises'].iloc[0]}</font><b></td></tr>
            <tr><td><font size=4>Number of Players Having Entered Pot:</font></td><td><b><font size=4>{X['num_players_before'].iloc[0]}</font><b></td></tr>
            <tr><td><font size=4>Number of Players Yet to Act:</font></td><td><b><font size=4>{X['num_players_after'].iloc[0]}</font><b></td></tr>
            <tr><td><font size=4>Position:</font></td><td><b><font size=4>{request.form['position_num']}/{request.form['num_players']}</font><b></td></tr>
            <tr><td><font size=4>BB in Stack:</font></td><td><b><font size=4>{round(X['BB_in_stack'].iloc[0], 2)}</font><b></td></tr>
        <table>
        <form action="/" method='GET' >        
            <button type='submit'>Make New Prediction</button>
        </form>

        '''
    if prediction < 0.62 and prediction > .53:
        page = f'''
        <table>
            <tr><td><font size=6>Predicted Outcome:</font></td><td><font size =6, color="orange">{result}</font></td></tr> 
            <tr><td></td></tr>

            <tr><td><font size=5>Input Data:</font></td><td></td></tr>
            <tr><td></td></tr>

            <tr><td><font size=4>High Card:</font></td><td><b><font size=4>{first_card.capitalize()}</font><b></td></tr>
            <tr><td><font size=4>Low Card:</font></td><td><b><font size=4>{second_card.capitalize()}</font><b></td></tr>
            <tr><td><font size=4>Suited:</font></td><td><b><font size=4>{request.form['suited'].capitalize()}</font><b></td></tr>
            <tr><td><font size=4>Card Rank:</font></td><td><b><font size=4>{X['card_rank'].iloc[0]}</font><b></td></tr>
            <tr><td><font size=4>Limpers:</font></td><td><b><font size=4>{X['limpers'].iloc[0]}</font><b></td></tr>
            <tr><td><font size=4>Raises & Reraises:</font></td><td><b><font size=4>{X['raises&reraises'].iloc[0]}</font><b></td></tr>
            <tr><td><font size=4>Number of Players Having Entered Pot:</font></td><td><b><font size=4>{X['num_players_before'].iloc[0]}</font><b></td></tr>
            <tr><td><font size=4>Number of Players Yet to Act:</font></td><td><b><font size=4>{X['num_players_after'].iloc[0]}</font><b></td></tr>
            <tr><td><font size=4>Position:</font></td><td><b><font size=4>{request.form['position_num']}/{request.form['num_players']}</font><b></td></tr>
            <tr><td><font size=4>BB in Stack:</font></td><td><b><font size=4>{round(X['BB_in_stack'].iloc[0], 2)}</font><b></td></tr>
        <table>
        <form action="/" method='GET' >        
            <button type='submit'>Make New Prediction</button>
        </form>
        '''
    if prediction <= 0.53:
        page = f'''
        <table>
            <tr><td><font size=6>Predicted Outcome:</font></td><td><font size =6, color="red">{result}</font></td></tr> 
            <tr><td></td></tr>

            <tr><td><font size=5>Input Data:</font></td><td></td></tr>
            <tr><td></td></tr>

            <tr><td><font size=4>High Card:</font></td><td><b><font size=4>{first_card.capitalize()}</font><b></td></tr>
            <tr><td><font size=4>Low Card:</font></td><td><b><font size=4>{second_card.capitalize()}</font><b></td></tr>
            <tr><td><font size=4>Suited:</font></td><td><b><font size=4>{request.form['suited'].capitalize()}</font><b></td></tr>
            <tr><td><font size=4>Card Rank:</font></td><td><b><font size=4>{X['card_rank'].iloc[0]}</font><b></td></tr>
            <tr><td><font size=4>Limpers:</font></td><td><b><font size=4>{X['limpers'].iloc[0]}</font><b></td></tr>
            <tr><td><font size=4>Raises & Reraises:</font></td><td><b><font size=4>{X['raises&reraises'].iloc[0]}</font><b></td></tr>
            <tr><td><font size=4>Number of Players Having Entered Pot:</font></td><td><b><font size=4>{X['num_players_before'].iloc[0]}</font><b></td></tr>
            <tr><td><font size=4>Number of Players Yet to Act:</font></td><td><b><font size=4>{X['num_players_after'].iloc[0]}</font><b></td></tr>
            <tr><td><font size=4>Position:</font></td><td><b><font size=4>{request.form['position_num']}/{request.form['num_players']}</font><b></td></tr>
            <tr><td><font size=4>BB in Stack:</font></td><td><b><font size=4>{round(X['BB_in_stack'].iloc[0], 2)}</font><b></td></tr>
        <table>
        <form action="/" method='GET' >        
            <button type='submit'>Make New Prediction</button>
        </form>
        '''




    return page 








if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, threaded=True, debug=False)
