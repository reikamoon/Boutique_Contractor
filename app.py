from flask import Flask, render_template, request, redirect, url_for
import requests
import json
from bson.objectid import ObjectId
from pymongo import MongoClient
import os

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/Clothes')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()
clothes = db.Clothes

app = Flask(__name__)

@app.route('/')
def homepage():
    #Homepage
    return render_template('homepage.html', clothes=clothes.find())

@app.route('/catalogue/')
def catalogue():
    #Catalogue, shows all Products (Product Grid)
    return render_template('catalogue.html', clothes=clothes.find())

@app.route('/catalogue/<clothes_id>', methods=['GET', 'POST'])
def show_product(clothes_id):
    #Shows a single Product
    product = clothes.find_one({'_id': ObjectId(clothes_id)})
    print(product)
    return render_template('product_display.html', clothes=product)

@app.route('/catalogue/new')
def new_entry():
    #Add a New Entry to Catalogue
    return render_template('new_entry.html', clothes={}, title='Add an Entry')

@app.route('/catalogue', methods=['POST'])
def product_submit():
    #Submit a new entry to the Clothes Database.
    new_product = {
    'name': request.form.get('name'),
    'price': request.form.get('price'),
    'image_url': request.form.get('image_url')
    }
    print(new_product)
    clothes_id = clothes.insert_one(new_product).inserted_id
    return redirect(url_for('show_product', clothes_id=clothes_id))

@app.route('/edit/<clothes_id>')
def clothes_edit(clothes_id):
    #Edit a product
    product = clothes.find_one({'_id': ObjectId(clothes_id)})
    return render_template('product_edit.html', clothes=product, title='Edit Product')

@app.route('/edit/<clothes_id>', methods=['POST'])
def clothes_update(clothes_id):
    #Save Edits to Product and Update entry in the database.
    updated_product = {
        'name': request.form.get('name'),
        'price': request.form.get('price'),
        'image_url': request.form.get('image_url')
    }
    clothes.update_one(
        {'_id': ObjectId(clothes_id)},
        {'$set': updated_product})
    return redirect(url_for('product_display', clothes_id=clothes_id))




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))
