from flask import Flask, jsonify, request
import os
from flask_cors import CORS
import pymongo
from dotenv import load_dotenv
load_dotenv()
import jwt
import datetime
from werkzeug.utils import secure_filename
import boto3
import uuid

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

CORS(app)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024

mongo_user = os.getenv('MONGO_USER')
mongo_password = os.getenv('MONGO_PASSWORD')
mongo_connection_string = f'mongodb+srv://{mongo_user}:{mongo_password}@myowdatabase.zzqvy.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
mongoClient = pymongo.MongoClient(mongo_connection_string)
mongoDB = mongoClient["WeatherApp"]

@app.route('/', methods=['GET'] )
def index():
    return 'Greetings from Weather App API!'

@app.route('/atractions/<country>', methods=['GET'] )
def get_atractions(country):
    print('Searching for atractions in ' + country)
    try:
        mongoCollection = mongoDB["countries"]
        result = mongoCollection.find_one({'key': country.lower()})
        print(result)
        return jsonify({
            'atractions': result['attractions'],
            'id': result['_id'].__str__()
        }), 200
    except Exception as e:
        print(e)
        return jsonify({
            'atractions': [],
        }), 200

@app.route('/countries/<name>', methods=['GET'] )
def get_country(name):
    #Find all countries that contain the name
    print('Searching for country ' + name)
    mongoCollection = mongoDB["countries"]
    result = mongoCollection.find({'key': {'$regex': name}})
    response = []
    for country in result:
        response.append({
            'name': country['name'],
            'key': country['key'],
            'id': country['_id'].__str__()
        })
    return jsonify({
        'countries': response
    }), 200

@app.route('/upload', methods=['POST'] )
def upload_file():
    try:
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            client = boto3.client('s3', aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))
            new_filename = str(uuid.uuid4()) + '.' + filename.split('.')[-1]
            client.upload_fileobj(file, os.getenv('AWS_BUCKET'), 'places/' + new_filename, ExtraArgs={'ACL': 'public-read'})
            return jsonify({
                "message": "Successfully uploaded image",
                "filename": new_filename,
                "success": True
            }), 200
        else:
            return jsonify({
                "message": "No file uploaded"
            }), 400
    except Exception as e:
            print(e)
            return jsonify({
                "message": "Error uploading image"
            }), 400

@app.route('/update', methods=['POST'] )
def update_country():
    #get data from request
    data = request.get_json()
    #Check if country exists
    mongoCollection = mongoDB["countries"]
    result = mongoCollection.find_one({'key': data['atraction']['country'].lower()})
    try:
        if result:
            #Append new atraction to country
            mongoCollection.update_one({'key': data['atraction']['country'].lower()}, {'$push': {'attractions': data['atraction']}})
            return jsonify({
                'message': 'Country updated successfully',
                'success': True
            }), 200
        else:
            #Create new country
            mongoCollection.insert_one({
                'name': data['atraction']['country'].capitalize(),
                'key': data['atraction']['country'].lower(),
                'attractions': [data['atraction']],
            })
            return jsonify({
                'message': 'Country created successfully',
                'success': True
            }), 200
    except Exception as e:
        print(e)
        return jsonify({
            'message': 'Error updating country',
            'success': False
        }), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.getenv('PORT'), debug=True)