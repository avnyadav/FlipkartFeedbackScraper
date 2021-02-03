# doing necessary imports
import sys

from flask import Flask, render_template, request,jsonify,json
# from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
from filpkartReview import feedback
from dbfile import getDataFromCollection


app = Flask(__name__)  # initialising the flask app with the name 'app'



@app.route('/',methods=['POST','GET']) # route with allowed methods as POST and GET
def index():
    if request.method == 'POST':
        searchString = request.form['content'].replace(" ","") # obtaining the search string entered in the form
        try:

            return render_template('results.html', reviews={'reviews':feedback(searchString),'msg':"OK"}) # showing the review to the user
        except Exception as e:
            return render_template('results.html', reviews={'reviews':feedback(searchString),'msg':str(e)})
    else:
        return render_template('index.html',reviews={'msg':None})


@app.route('/feedback',methods=['GET'])
def getFeedback():
    name=request.args.get("name")
    return jsonify(feedback(name))


if __name__ == "__main__":
    app.run(port=8000,debug=True) # running the app on the local machine on port 8000