#!/usr/bin/env python3

from models import db, Activity, Camper, Signup
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask import Flask, make_response, jsonify, request
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

@app.route('/')
def home():
    return ''

class Campers(Resource):
    def get(self):
        try:
            campers = [camper.to_dict(only=("id", "name", "age")) for camper in Camper.query.all()]

            return make_response(campers, 200)
        except:
            raise make_response('bad request', 400)
        
    def post(self):
        try:
            new_camper = {
                "name" : request.form['name'],
                "age" : request.form['age']
            }

            db.session.add(new_camper)
            db.session.commit()

            return make_response(new_camper.to_dict(only=("id", "name", "age")), 201)
        except:
            return { "error": "400: Validation error"}, 400
    
api.add_resource(Campers, '/campers')

class CamperByID(Resource):
    def get(self, id):
        try:
            camper = Camper.query.filter_by(id=id).first()
            
            return make_response(camper.to_dict(), 200)
        except:
            return make_response({"error": "Camper not found"}, 400)
        
    def patch(self, id):
        try:
            camper = Camper.query.filter_by(id=id).first()

            print(request.form)
            for attr in request.form:
                print(attr)
                setattr(camper, attr, request.form[attr])

            db.session.add(camper)
            db.session.commit()

            return make_response(camper.to_dict(only=("id", "name", "age")), 200)
        except:
            return make_response({"error": "Camper not found"}, 400)
            
class Activities(Resource):
    def get(self):
        activities = [activity.to_dict(only=("id", "name", "difficulty")) for activity in Activity.query.all()]

        return make_response(activities, 200)
    
api.add_resource(Activities, '/activities')

class ActivityByID(Resource):
    def delete(self, id):
        try:
            activity = Activity.query.filter_by(id=id).first()

            db.session.delete(activity)
            db.session.commit()
            
            return make_response("", 202)
        except:
            return make_response({"error": "Activity not found"}, 400)

api.add_resource(ActivityByID, '/activities/<int:id>')


api.add_resource(CamperByID, '/campers/<int:id>')
if __name__ == '__main__':
    app.run(port=5555, debug=True)
