from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
import os
import markdown

#Classes
from resources.schedule import Schedule

api_v1_cors_config = {
  "origins": '*',
  "allow_headers": ["Username", "Password", "SchoolId", "Type"]
}

app = Flask(__name__)
cors = CORS(app, resources={r"*": api_v1_cors_config})

api = Api(app)

@app.route("/")
def index():
	#Default site
	with open("./docs/main.md", "r") as markdown_file:
		content = markdown_file.read()

		return markdown.markdown(content, extensions=['fenced_code', 'tables', 'nl2br'])


api.add_resource(Schedule, '/schedule')

if __name__ == "__main__":
	app.run(debug=True)