from flask import Flask, render_template, request, redirect, url_for
import requests
import json
from bson.objectid import ObjectId
from pymongo import MongoClient
import os

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/Clothes')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()
clothes = db.clothes

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('index.html', clothes=clothes.find())


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))
    
