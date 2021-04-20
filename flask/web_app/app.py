# Demonstrates Bootstrap version 3.3 Starter Template
# available here: https://getbootstrap.com/docs/3.3/getting-started/#examples

from flask import Flask, render_template, request
import pickle
import numpy as np 
import pandas as pd 
app = Flask(__name__)

# home page
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/prediction', methods=['POST'] )
def predict():
    with open('gradient_boost_cap2.pickle', 'rb') as f:
        model = pickle.load(f)
        X = pd.DataFrame({'buyin': [float(request.form['buyin'])], 
                          'BB_in_stack': [float(request.form['BB_in_stack'])], 
                          'total_players': [float(request.form['total_players'])], 
                          'position': [float(request.form['position'])], 
                          'low_card': [float(request.form['low_card'])],
                          'high_card': [float(request.form['high_card'])], 
                          'suited': [float(request.form['suited'])], 
                          'pocket_pair': [float(request.form['pocket_pair'])], 
                          'card_rank': [float(request.form['card_rank'])]
                          })
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

    <table>'''

    return page 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, threaded=True, debug=False)
