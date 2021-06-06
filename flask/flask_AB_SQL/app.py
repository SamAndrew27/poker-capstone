import psycopg2 as pg2
from sqlalchemy import create_engine

from flask import Flask, render_template, request, session, redirect
import pickle
import numpy as np 
import pandas as pd 
from poker_funcs import construct_cards, suited_to_int

app = Flask(__name__)
app.secret_key = 'dev'


conn = pg2.connect(database="hand_results", user="postgres", password="galvanize", host="localhost", port="5432")
engine = create_engine("postgresql://postgres:galvanize@localhost:5432/hand_results")
cur = conn.cursor()

@app.route('/')
def index():

    cur.execute('DROP TABLE IF EXISTS "session_logs";')
    cur.execute('''CREATE TABLE session_logs(
            session_name VARCHAR, 
            hands_logged INT);
            ''')
    conn.commit()

    cur.execute("""SELECT table_name FROM information_schema.tables
       WHERE table_schema = 'public'""")
    tables = []
    hands = []
    for table in cur.fetchall():
        tables.append(table[0])

    for table in tables:
        cur.execute(f'''SELECT COUNT(*)
                        FROM {table}''')
        for hand_count in cur.fetchall():
            hands.append(hand_count[0])

    insert_query = 'INSERT INTO session_logs (session_name, hands_logged) VALUES(%s, %s);'

    for table, hand_count in zip(tables, hands):
        data = (table, hand_count)
        cur.execute(insert_query, data)
        conn.commit()


    cur.execute('SELECT * FROM session_logs')
    results = cur.fetchall()
    
    return render_template('index2.html', events = results)

    # page = f'''
    # <form action="/save_percent_filename" method='POST' >
    #             Enter percent of hands to be directed to model and filepath for results:<br/>
    #             <input type="text" name="percent_predict"> %</input><br/>
    #             <input type="text" name="session_name"> session name </input><br/>

    #             <input type="submit" />
    # </form>
    # <body>
    #     <p><b> Existing Databases:</b></p>
    #     <p><b> {tables}</b></p>
    # <body>
    # '''
    # return page 


@app.route('/save_percent_filename', methods=['POST', 'GET'])
def save_percent_filename():
    session['duplicate'] = False
    session['percent_model'] = float(request.form['percent_predict']) / 100
    session['session_name'] =  request.form['session_name']
    cur.execute("""SELECT table_name FROM information_schema.tables
       WHERE table_schema = 'public'""")
    for table in cur.fetchall():
        if session['session_name'] == table[0]:
            session['duplicate'] = True
            break




    if session['duplicate']:
        page = f'''
        <body>
            <p><b> DUPLICATE FILENAME!</b></p>
        <body>
        <form action='/input' method='POST' >        
            <button type='submit'>Proceed Using the Same Database</button>
        </form>
        <form action='/input' method='POST' >        
            <input type="text" name="new_session_name" > Input New Session Name</input><br/>
            <input type="submit" />
        </form>
        '''    
        return page
    else:
        cur.execute(
            f'''CREATE TABLE {session['session_name']}(
                hand_id INT, 
                suited INT,
                high_card INT,
                low_card INT,
                position FLOAT,
                card_rank FLOAT,
                limpers INT,
                raises_reraises INT,
                num_players_before INT,
                num_players_after INT,
                bb_in_stack INT,
                starting_stack FLOAT,
                end_stack FLOAT,
                prediction_value FLOAT,
                prediction_displayed VARCHAR);
            ''')
        conn.commit()

        return redirect('/input') 





# Input Page
@app.route('/input', methods=['POST', 'GET'])

def input():

    return render_template('input2.html')





@app.route('/prediction', methods=['POST'] )
def predict():
    cards = request.form.getlist('card')
    s = ''
    for c in cards:
        s += c
    return s 
# def predict():
#     """makes prediction using user input data 

#     Returns:
#         html page: shows variables used to make prediction & prediction 
#     """    
#     with open('models/final_model.pickle', 'rb') as f:
#         model = pickle.load(f)

#         position = int(request.form['position_num']) / int(request.form['num_players']) # use position_num divided by total players to get 'position' variable
#         BB_in_stack = float(request.form['stack']) / float(request.form['BB'])  # use stack divided by BB to get BB_in_stack
#         suited = suited_to_int(request.form['suited']) # converts input 'yes/no' to 1/0


#         first_card = request.form['first_card_value']
#         second_card = request.form['second_card_value']

        
#         rank, low_card, high_card = construct_cards(first_card, second_card, suited=suited) # uses card values and suited to get rank, low card, highcard
        
        

#         X = pd.DataFrame({'suited': [suited], # putting variables into dataframe
#                           'low_card': [low_card],
#                           'position': [position], 
#                           'high_card': [high_card], 
#                           'card_rank': [rank],
#                           'limpers': [int(request.form['limpers'])], 
#                           'raises&reraises': [int(request.form['raises&reraises'])], 
#                           'num_players_before': [int(request.form['num_players_before'])], 
#                           'num_players_after': [int(request.form['num_players_after'])],
#                           'BB_in_stack': [BB_in_stack]})



#         prediction = model.predict_proba(X)[0][1] # get prediction, below we are assigning result based on prediction proba
#         if prediction >= 0.62:
#             prediction_str = 'Play It!'
#         if prediction < 0.62 and prediction > 0.53:
#             prediction_str = 'Caution'
#         if prediction <= .53:
#             prediction_str = "Don't Do It!"

#     fork = np.random.choice(['displayed', 'not displayed'], p=[session['percent_model'], 1 - session['percent_model']])

#     session['suited'] = suited
#     session['low_card'] = low_card
#     session['high_card'] = high_card
#     session['card_rank'] = rank
#     session['position'] = position 
#     session['limpers'] = int(request.form['limpers'])
#     session['raises&reraises'] = int(request.form['raises&reraises'])
#     session['num_players_before'] = int(request.form['num_players_before'])
#     session['num_players_after'] = int(request.form['num_players_after'])
#     session['BB_in_stack'] = BB_in_stack
#     session['stack'] = float(request.form['stack'])
#     # session['end_stack'] = None
#     session['prediction_value'] = prediction
#     session['prediction_displayed'] = fork

#     table = f'''
#                 <tr><td></td></tr>

#                 <tr><td><font size=5>Input Data:</font></td><td></td></tr>
#                 <tr><td></td></tr>

#                 <tr><td><font size=4>First Card</font></td><td><b><font size=4>{first_card.capitalize()}</font><b></td></tr>
#                 <tr><td><font size=4>Low Card:</font></td><td><b><font size=4>{second_card.capitalize()}</font><b></td></tr>
#                 <tr><td><font size=4>Suited:</font></td><td><b><font size=4>{request.form['suited'].capitalize()}</font><b></td></tr>
#                 <tr><td><font size=4>Card Rank:</font></td><td><b><font size=4>{X['card_rank'].iloc[0]}</font><b></td></tr>
#                 <tr><td><font size=4>Limpers:</font></td><td><b><font size=4>{X['limpers'].iloc[0]}</font><b></td></tr>
#                 <tr><td><font size=4>Raises & Reraises:</font></td><td><b><font size=4>{X['raises&reraises'].iloc[0]}</font><b></td></tr>
#                 <tr><td><font size=4>Number of Players Having Entered Pot:</font></td><td><b><font size=4>{X['num_players_before'].iloc[0]}</font><b></td></tr>
#                 <tr><td><font size=4>Number of Players Yet to Act:</font></td><td><b><font size=4>{X['num_players_after'].iloc[0]}</font><b></td></tr>
#                 <tr><td><font size=4>Position:</font></td><td><b><font size=4>{request.form['position_num']}/{request.form['num_players']}</font><b></td></tr>
#                 <tr><td><font size=4>BB in Stack:</font></td><td><b><font size=4>{round(X['BB_in_stack'].iloc[0], 2)}</font><b></td></tr>

#             <table>'''

#     if fork == 'model':
#         if prediction >= 0.62:
#             page = f'''
#             <table>
#                 <tr><td><font size=6>Predicted Outcome:</font></td><td><font size =6, color="green">{prediction_str}</font></td></tr> 
#                 {table}

#             <form action="/save_hand" method='POST' >
#                         <input type="text" name="chips_left"> Enter the size of your stack after playing</input><br/>
#                         <input type="submit" />
#             </form>
#             '''
#         if prediction < 0.62 and prediction > .53:
#             page = f'''
#             <table>
#                 <tr><td><font size=6>Predicted Outcome:</font></td><td><font size =6, color="orange">{prediction_str}</font></td></tr> 
#                 {table}

#             <form action="/save_hand" method='POST' >
#                         <input type="text" name="chips_left"> Enter the size of your stack after playing</input><br/>
#                         <input type="submit" />
#             </form>
#             <form action='/save_hand' method='POST' >        
#                 <button type='submit'>Did Not Play Hand</button>
#             </form>
#             '''
#         if prediction <= 0.53:
#             page = f'''
#             <table>
#                 <tr><td><font size=6>Predicted Outcome:</font></td><td><font size =6, color="red">{prediction_str}</font></td></tr> 
#                 {table}

#             <form action='/save_hand' method='POST' >        
#                 <button type='submit'>Continue</button>
#             </form>
#             '''
#     else:
#         page = f'''
#         <table>
#             <tr><td><font size=6>Predicted Outcome:</font></td><td><font size =6, color="blue">Up to You</font></td></tr> 
#             {table}

#         <form action='/save_hand' method='POST' >
#                 <input type="text" name="chips_left"> Enter the size of your stack after playing</input><br/>
#                 <input type="submit" />
#         </form>
#         <form action='/save_hand' method='POST' >        
#             <button type='submit'>Did Not Play Hand</button>
#         </form>
#         '''
#     return page 




@app.route('/save_hand', methods=['POST'])
def save_hand():
    chips_left = request.form.get('chips_left') or 'Did Not Play'
    if chips_left != 'Did Not Play':
        chips_left = float(chips_left)

    string = []
    cur.execute(f'''SELECT COUNT(*)
                    FROM {session['session_name']}''')
    for value in cur.fetchall():
        hand_id = value[0]
        break 
    
    insert_query = f'''INSERT INTO {session['session_name']} (hand_id, suited, high_card, low_card, position, card_rank, limpers, raises_reraises, num_players_before, 
                                               num_players_after, bb_in_stack, starting_stack, end_stack, prediction_value, prediction_displayed) 
                                               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                    '''
    

    data = (hand_id, 
            session['suited'], 
            session['high_card'], 
            session['low_card'], 
            session['position'], 
            session['card_rank'],
            session['limpers'],
            session['raises&reraises'], 
            session['num_players_before'],
            session['num_players_after'],
            session['BB_in_stack'],
            session['stack'],
            chips_left,   
            session['prediction_value'],
            session['prediction_displayed'])

    cur.execute(insert_query, data)

    conn.commit()




    page = f'''
    <form action='/input' method='POST' >        
        <button type='submit'>Make New Prediction!</button>
    </form>
    <form action='/' method='GET' >        
        <button type='submit'>Change Percent A/B or Filename</button>
    </form>
    '''
    return page 




# @app.route('/save_hand_null', methods=['POST'])
# def save_hand_null():
#     df = pd.read_csv(f'hand_results/{session["session_name"]}.csv')
#     df = df.drop(df.columns[0], axis=1)
#     temp_df = pd.DataFrame({'suited': [session['suited']], 
#                         'low_card': [session['low_card']],
#                         'position': [session['position']], 
#                         'high_card': [session['high_card']], 
#                         'card_rank': [session['card_rank']],
#                         'limpers': [session['limpers']], 
#                         'raises&reraises': [session['raises&reraises']], 
#                         'num_players_before': [session['num_players_before']], 
#                         'num_players_after': [session['num_players_after']],
#                         'BB_in_stack': [session['BB_in_stack']],
#                         'stack': [session['stack']],
#                         'end_stack': [session['stack']],
#                         'model': [session['model']],
#                         'prediction': [session['prediction']]})
#     df = pd.concat([df, temp_df], ignore_index=True)
#     df.to_csv(f'hand_results/{session["session_name"]}.csv')
#     page = f'''
#     <form action='/input' method='POST' >        
#         <button type='submit'>Make New Prediction!</button>
#     </form>
#     <form action='/' method='GET' >        
#         <button type='submit'>Change Percent A/B or Filename</button>
#     </form>
#     ''' 
#     return page 


# hand results
# @app.route('/results', methods=['POST'])
# def results():
#     page = f'''

#     <form action='/save_hand' method='POST' >     
#         <input type="text" name="chips_left"> Final Amount of Chips</input><br/>

#         <button type='submit'>Save Hand</button>
#     </form>
#     '''
#     return page 
# return request.form.get('session_name') or 'No Session Name! dingus'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, threaded=True, debug=False)




