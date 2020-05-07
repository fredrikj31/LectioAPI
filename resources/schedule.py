from flask import Flask
from flask_restful import Resource, Api, reqparse
import os
import markdown

class Schedule(Resource):
	def get(self):
		parser = reqparse.RequestParser()
		parser.add_argument('testKey', location='header')
		args = parser.parse_args()


		if args['testKey'] is None:
			return {'message': 'Error', 'data': "Unauthorized. Please enter login details"}, 401
		else:
			return {'message': 'Success', 'data': "Here is where the data is going" + args['testKey']}, 200