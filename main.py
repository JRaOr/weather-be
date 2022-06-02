from flask import Flask, jsonify, request
import os
from flask_cors import CORS
import pymongo
from dotenv import load_dotenv
load_dotenv()
import jwt
import datetime
from user.user import user
from picture.picture import picture
from room.room import room

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
            'population': result['population'],
            'capital': result['capital'],
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.getenv('PORT'), debug=True)