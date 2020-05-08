from flask import Flask
from flask_restful import Resource, Api, reqparse
import os
import markdown

from library.lectio import Lectio

class Schedule(Resource):
	def get(self):
		
		parser = reqparse.RequestParser()
		#Setting auth parameter
		parser.add_argument('Username', location='headers')
		parser.add_argument('Password', location='headers')
		parser.add_argument('SchoolId', location='headers')
		parser.add_argument('Type', location='headers')

		args = parser.parse_args()

		if args['Username'] is None:
			return {'message': 'Error', 'data': "Unauthorized. Please enter the username. Please look into the documentation"}, 401
		elif args['Password'] is None:
			return {'message': 'Error', 'data': "Unauthorized. Please enter the password. Please look into the documentation"}, 401
		elif args['SchoolId'] is None:
			return {'message': 'Error', 'data': "Unauthorized. Please enter the school id. Please look into the documentation"}, 401
		elif args['Type'] is None:
			return {'message': 'Error', 'data': "Unauthorized. Please enter the type of person. Please look into the documentation"}, 401
		else:
			lec = Lectio(args['Username'], args['Password'], args['SchoolId'], args['Type'])

			result = lec.getSchedule()

			return {'message': 'Success', 'data': result}, 200