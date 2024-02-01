from flask import Flask, render_template, request, url_for,jsonify
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
from amazons import process_product_url
from mls import predict_reviews
from flask_cors import CORS


app = Flask(__name__)

CORS(app, resources={r"/ml_process": {"origins": "chrome-extension://kbhlmcneelkjopmohhppfaafgoiiaaco"}})
#CORS(app, resources={r"/ml_process": {"origins": "chrome-extension://kbhlmcneelkjopmohhppfaafgoiiaaco"}})
# id : kbhlmcneelkjopmohhppfaafgoiiaaco
@app.route('/')
def main():
    return render_template('index.html')

    
@app.route('/ml_process',methods=['POST','GET'])
def ml_process():
    '''if request.method == 'POST':
        resp_json = request.get_json()
        f =  resp_json['text'] #link
        print(f)
       # time.sleep(2)
        #r.parse2(f)
       # new_rating = n.get_nr()

     #   return json.dumps({"response": new_rating}), 200
       '''
    if request.method == 'POST':
        #url = request.form['url']
        ml_link = request.form['url']
       # product_url = ml_link
        df_reviews = process_product_url(ml_link)
        
    prediction_result = predict_reviews(df_reviews)

   
   # return f"Quantity of real review from : {ml_link}. Prediction: {prediction_result}"
    
    #return  render_template("result.html", reviews=df_reviews, preds=prediction_result)
    response_data = {
        'reviews': df_reviews.to_dict(orient='records'),
        'predictions': prediction_result
    }

    # Check the 'Accept' header to determine the response format
    accept_header = request.headers.get('Accept')
    
    if 'application/json' in accept_header:
        # If the request prefers JSON, return JSON
        return jsonify(response_data), 200, {'Content-Type': 'application/json'}
    else:
        # If the request prefers HTML, return the HTML template
        return render_template("result.html", reviews=df_reviews, preds=prediction_result)
    #return render_template('result.html')

        
        # Process the URL as needed (e.g., store it in a database, perform some action)
        #return f'The URL you submitted is: {url}'
        #Header to set the requests as a browser requests
        #return jsonify({"response": f'The URL you submitted is: {url}'})
    #return render_template('index.html')




#return render_template('index.html')
if __name__ == '__main__':
    #webbrowser.open('http://127.0.0.1:5000')
    app.run(debug=True)