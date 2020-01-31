from flask import Flask
from flask_restful import Resource, Api
import datetime
from epl_scrape import scrape

app = Flask(__name__)
api = Api(app)

class ScrapeScores(Resource):
    def get(self, date_str):
        # Validate date input
        try:
            date = datetime.datetime.strptime(date_str, '%Y%m%d')
        except ValueError:
            return {'Error': 'Invalid date'}, 400

        return scrape(date_str, date)

api.add_resource(ScrapeScores, '/<string:date_str>')

if __name__ == '__main__':
    app.run(debug=True)
