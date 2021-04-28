# Demonstrates Bootstrap version 3.3 Starter Template
# available here: https://getbootstrap.com/docs/3.3/getting-started/#examples

from flask import Flask, render_template, request, session
import pickle
import numpy as np 
import pandas as pd 
from app_funcs import construct_cards, suited_to_int
app = Flask(__name__)
app.secret_key = 'dev'

# class saved_data():
#     def __init__(self):
#         self.percent_model  = .5
#         self.percent_non_model = .5 
#     def set_percents(self, percent):
#         self.percent_model = percent
#         self.percent_non_model = 1 - percent
# data = saved_data()

# home page
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save_percent_filename', methods=['POST', 'GET'])
def save_percent_filename():
    
    session['percent_model'] = float(request.form['percent_predict']) / 100
    session['percent_non_model'] = 1 - session['percent_model']
    session['filename'] = request.form['filename']
    starting_df = pd.DataFrame({'suited': [None], 
                        'low_card': [None],
                        'position': [None], 
                        'high_card': [None], 
                        'card_rank': [None],
                        'limpers': [None], 
                        'raises&reraises': [None], 
                        'num_players_before': [None], 
                        'num_players_after': [None],
                        'BB_in_stack': [None],
                        'stack': [None],
                        'end_stack': [None],
                        'model': [None],
                        'prediction': [None]})
    starting_df.to_csv(f'hand_results/{session["filename"]}.csv')
    page = f'''
    <table>
        <tr><td><font size=6>Percent Chosen:</font></td><td><font size =6, color="black">{request.form['percent_predict']}%</font></td></tr> 

        <tr><td><font size=6>Filename Chosen:</font></td><td><font size =6, color="black">{session['filename']}</font></td></tr> 
    <table>
    <form action='/input' method='POST' >        
        <button type='submit'>Start Predicting!</button>
    </form>
    '''
    return page 



# Input Page
@app.route('/input', methods=['POST'])

def input():
    return render_template('input.html')


# hand results
@app.route('/results', methods=['POST'])
def results():
    page = f'''

    <form action='/save_hand' method='POST' >     
        <input type="text" name="chips_left"> Final Amount of Chips</input><br/>

        <button type='submit'>Save Hand</button>
    </form>
    '''
    return page 

@app.route('/save_hand', methods=['POST'])
def save_hand():
    chips_left = float(request.form['chips_left'])
    df = pd.read_csv('results.csv')
    df = df.drop(df.columns[0], axis=1)
    temp_df = pd.DataFrame({'suited': [session['suited']], 
                        'low_card': [session['low_card']],
                        'position': [session['high_card']], 
                        'high_card': [None], 
                        'card_rank': [session['card_rank']],
                        'limpers': [session['limpers']], 
                        'raises&reraises': [session['raises&reraises']], 
                        'num_players_before': [session['num_players_before']], 
                        'num_players_after': [session['num_players_after']],
                        'BB_in_stack': [session['BB_in_stack']],
                        'stack': [session['stack']],
                        'end_stack': [chips_left],
                        'model': [session['model']],
                        'prediction': [session['prediction']]})
    df = pd.concat([df, temp_df], ignore_index=True)
    df.to_csv(f'hand_results/{session["filename"]}.csv')
    page = f'''
    <form action='/input' method='POST' >        
        <button type='submit'>Make New Prediction!</button>
    </form>
    <form action='/' method='GET' >        
        <button type='submit'>Change Percent A/B or Filename</button>
    </form>
    '''
    return page 




@app.route('/save_hand_null', methods=['POST'])
def save_hand_null():
    df = pd.read_csv(f'hand_results/{session["filename"]}.csv')
    df = df.drop(df.columns[0], axis=1)
    temp_df = pd.DataFrame({'suited': [session['suited']], 
                        'low_card': [session['low_card']],
                        'position': [session['high_card']], 
                        'high_card': [None], 
                        'card_rank': [session['card_rank']],
                        'limpers': [session['limpers']], 
                        'raises&reraises': [session['raises&reraises']], 
                        'num_players_before': [session['num_players_before']], 
                        'num_players_after': [session['num_players_after']],
                        'BB_in_stack': [session['BB_in_stack']],
                        'stack': [session['stack']],
                        'end_stack': [session['stack']],
                        'model': [session['model']],
                        'prediction': [session['prediction']]})
    df = pd.concat([df, temp_df], ignore_index=True)
    df.to_csv(f'hand_results/{session["filename"]}.csv')
    page = f'''
    <form action='/input' method='POST' >        
        <button type='submit'>Make New Prediction!</button>
    </form>
    <form action='/' method='GET' >        
        <button type='submit'>Change Percent A/B or Filename</button>
    </form>
    ''' 
    return page 




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
            result = 'Play It!'
        if prediction < 0.62 and prediction > 0.53:
            result = 'Caution'
        if prediction <= .53:
            result = "Don't Do It!"

    fork = np.random.choice(['model', 'non_model'], p=[session['percent_model'], session['percent_non_model']])
    session['suited'] = suited
    session['low_card'] = low_card
    session['high_card'] = high_card
    session['card_rank'] = rank
    session['limpers'] = int(request.form['limpers'])
    session['raises&reraises'] = int(request.form['raises&reraises'])
    session['num_players_before'] = int(request.form['num_players_before'])
    session['num_players_after'] = int(request.form['num_players_after'])
    session['BB_in_stack'] = BB_in_stack
    session['stack'] = float(request.form['stack'])
    session['end_stack'] = None
    session['model'] = fork
    session['prediction'] = result



    if fork == 'model':
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
            <form action='/results' method='POST' >        
                <button type='submit'>Input Hand Results</button>
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
            <form action='/results' method='POST' >        
                <button type='submit'>Played Hand</button>
            </form>
            <form action='/save_hand_null' method='POST' >        
                <button type='submit'>Did Not Play Hand</button>
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
            <form action='/save_hand_null' method='POST' >        
                <button type='submit'>Continue</button>
            </form>
            '''
    else:
        page = f'''
        <table>
            <tr><td><font size=6>Predicted Outcome:</font></td><td><font size =6, color="blue">Up to You</font></td></tr> 
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
        <form action='/results' method='POST' >        
            <button type='submit'>Played Hand</button>
        </form>
        <form action='/save_hand_null' method='POST' >        
            <button type='submit'>Did Not Play Hand</button>
        </form>
        '''



    return page 








if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, threaded=True, debug=False)
