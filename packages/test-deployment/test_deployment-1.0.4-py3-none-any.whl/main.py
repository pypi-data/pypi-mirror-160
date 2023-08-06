# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


from flask import Flask

from flask_restful import Resource, Api

app = Flask(__name__)

api = Api(app)

class Helloworld(Resource):

	def __init__(self):

		pass

	def get(self):

		return {

			"defaul":"hello"

		}

api.add_resource(Helloworld, '/')

if __name__ == '__main__':

	app.run(debug=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
