from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import pandas as pd
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)

with open ('model_pickle','rb') as f:
    mp = pickle.load(f)

@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')

@app.route("/predict", methods=['POST'])
def predict():
    ##Fuel_Type_Diesel=0
    if request.method == 'POST':
        Year = int(request.form['Year'])
        Present_Price=float(request.form['Present_Price'])
        Kms_Driven=int(request.form['Kms_Driven'])
        Owner=int(request.form['Owner'])
        Fuel_Type=request.form['Fuel_Type']
        if(Fuel_Type=='Petrol'):
                Fuel_Type_Petrol=1
                Fuel_Type_Diesel=0
        elif (Fuel_Type=='Diesel'):
            Fuel_Type_Petrol=0
            Fuel_Type_Diesel=1
        else:
            Fuel_Type_Petrol=0
            Fuel_Type_Diesel=0
        Years_Old=pd.datetime.now().year-Year
        Seller_Type=request.form['Seller_Type']
        if(Seller_Type=='Individual'):
            Seller_Type_Individual=1
        else:
            Seller_Type_Individual=0
        Transmission=request.form['Transmission']
        if(Transmission=='Manual'):
            Transmission_Manual=1
        else:
            Transmission_Manual=0
        prediction=mp.predict([[Present_Price,Kms_Driven,Owner,Years_Old,Fuel_Type_Diesel,Fuel_Type_Petrol,Seller_Type_Individual,Transmission_Manual]])
        output=round(prediction[0],2)
        if output<0:
            return render_template('index.html',prediction_text="Sorry you cannot sell this car")
        else:
            return render_template('index.html',prediction_text="You Can Sell The Car for {} Lakhs".format(output))
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)
