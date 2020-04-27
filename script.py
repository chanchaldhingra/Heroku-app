#importing libraries
import os
import numpy as np
import flask
from sklearn.externals import joblib
import pickle
from flask import Flask, render_template, request
#from sklearn.preprocessing import StandardScaler
#from sklearn.svm import SVC

#creating instance of the class
app=Flask(__name__)

#to tell flask what url shoud trigger the function index()
@app.route('/')
@app.route('/index')
def index():
    return flask.render_template('index.html')


#Creating final list of input values
def Create(mydict):
    new = mydict["age"].split("-")

    mydict['age']=((int)(new[0])+(int)(new[1]))/2

    new = mydict["tumor-size"].split("-")
    mydict['tumor-size']=int(((int)(new[0])+(int)(new[1]))/2)

    new = mydict["inv-falsedes"].split("-")
    mydict['inv-falsedes']=int(((int)(new[0])+(int)(new[1]))/2)

    mydict['deg-malig']=int(mydict['deg-malig'])

    final_list=[]
    final_list.append(mydict['deg-malig'])
    final_list.append(mydict['age'])
    final_list.append(mydict['tumor-size'])
    final_list.append(mydict['inv-falsedes'])
    if mydict['mefalsepause']=='ge40':
        final_list.append(1)
        final_list.append(0)
        final_list.append(0)

    elif mydict['mefalsepause']=='It40':
        final_list.append(0)
        final_list.append(1)
        final_list.append(0)
    else:
        final_list.append(0)
        final_list.append(0)
        final_list.append(1)

    if mydict['falsedes-caps']=='false':
        final_list.append(1)
        final_list.append(0)
    else:
        final_list.append(0)
        final_list.append(1)

    if mydict['breast']=='left':
        final_list.append(1)
        final_list.append(0)
    else:
        final_list.append(0)
        final_list.append(1)

    if mydict['breast-quad']=='central':
        final_list.append(1)
        final_list.append(0)
        final_list.append(0)
        final_list.append(0)
        final_list.append(0)

    elif mydict['breast-quad']=='left_low':
        final_list.append(0)
        final_list.append(1)
        final_list.append(0)
        final_list.append(0)
        final_list.append(0)


    elif mydict['breast-quad']=='left_up':
        final_list.append(0)
        final_list.append(0)
        final_list.append(1)
        final_list.append(0)
        final_list.append(0)

    elif mydict['breast-quad']=='right_low':
        final_list.append(0)
        final_list.append(0)
        final_list.append(0)
        final_list.append(1)
        final_list.append(0)

    else:
        final_list.append(0)
        final_list.append(0)
        final_list.append(0)
        final_list.append(0)
        final_list.append(1)


    if mydict['irradiant']=='false':
        final_list.append(1)
        final_list.append(0)
    else:
        final_list.append(0)
        final_list.append(1)

    final_tuple=tuple(final_list)
    print(final_tuple)
    return final_tuple




#prediction function
def ValuePredictor(to_predict_tuple):
    #print(to_predict_tuple)
    to_predict = np.array(list(to_predict_tuple)).reshape(1,18)

    #Loading model through pickle
    loaded_model = pickle.load(open("model.pkl","rb"))

    #Loading Standard Scalar object
    scalerfile = 'scaler.sav'
    scaler = pickle.load(open(scalerfile, 'rb'))
    to_predict = scaler.transform(to_predict)

    result = loaded_model.predict(to_predict)
    
    #print(result[0])
    return result[0]


@app.route('/result',methods = ['POST'])
def result():
    if request.method == 'POST':
        to_predict_list = request.form.to_dict()
        
        to_predict_tuple=Create(to_predict_list)
        
        result = ValuePredictor(to_predict_tuple)
        
        if int(result)==1:
            prediction='Recurrence'
        else:
            prediction='No Recurrence'
         
        
        return render_template("index.html",prediction=prediction)
