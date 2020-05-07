from flask import Flask
from flask_restful import Resource, Api, reqparse
import os
import markdown

#Classes
from resources.schedule import Schedule

app = Flask(__name__)

api = Api(app)

@app.route("/")
def index():
	#Default site
	with open("./docs/main.md", "r") as markdown_file:
		content = markdown_file.read()

		return markdown.markdown(content, extensions=['fenced_code', 'tables', 'nl2br'])


api.add_resource(Schedule, '/schedule')

app.run(host="", port="", debug=True)