from flask import Flask, render_template, request, url_for
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
from amazons import process_product_url
from mls import predict_reviews


app = Flask(__name__)

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

    #result = process_product_url(product_url)
   # return f"Quantity of real review from : {ml_link}. Prediction: {prediction_result}"
    return f"Quantity of real review.{prediction_result}"

        
        # Process the URL as needed (e.g., store it in a database, perform some action)
        #return f'The URL you submitted is: {url}'
        #Header to set the requests as a browser requests
        #return jsonify({"response": f'The URL you submitted is: {url}'})
    #return render_template('index.html')




#return render_template('index.html')
if __name__ == '__main__':
    #webbrowser.open('http://127.0.0.1:5000')
    app.run(debug=False)