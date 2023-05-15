import flask
from flask import Flask
from flask_restful import Resource, Api

from scrapper import Scrapper
class Cars(Resource):
    def get(self):
        scrp = Scrapper()
        cars = scrp.get_cars()
        return cars
    
app = Flask(__name__)
api = Api(app)
api.add_resource(Cars, '/cars')
if __name__ == '__main__':
    app.run()  # run our Flask app