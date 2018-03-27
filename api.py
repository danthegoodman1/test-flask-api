from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)


testdict = {"test1": "hello1", "test2": "hello2"}


# remember this is not persistent
managedict = {
    'key1': 'val1'
}


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


class test11(Resource):
    def get(self):
        return "This test worked!"

    def post(self):
        return 'worked?'


class testdict1(Resource):
    def get(self, test_id):
        return "{testid}: {dictitem}".format(testid=test_id, dictitem=testdict[test_id])


class dictmanage(Resource):
    def get(self):
        return managedict

    def post(self):
        args = parser.parse_args()
        managedict[args['addkey']] = args['addval']
        return "Added the following to the 'Manage' dictionary:{0}: {1}".format(args['addkey'], args['addval'])


class managedictitems(Resource):
    def get(self, keyToAdd, valueToAdd):
        managedict[keyToAdd] = valueToAdd
        return "Added the following to the 'Manage' dictionary:{0}: {1}".format(keyToAdd, valueToAdd)


# curl http://127.0.0.1:5000/
api.add_resource(HelloWorld, '/')


# curl http://127.0.0.1:5000/test11
api.add_resource(test11, '/test11')


# curl http://127.0.0.1:5000/testdict1/(key)
api.add_resource(testdict1, '/testdict1/<string:test_id>')


# curl http://localhost:5000/manage -d "addkey=key3" -d "addval=val3" -X POST -v
# see http://flask-restful.readthedocs.io/en/0.3.5/reqparse.html#required-arguments
api.add_resource(dictmanage, '/manage')
# this makes it so arguments can be passed in the url through a get request
api.add_resource(managedictitems, '/manageadd/<string:keyToAdd>/<string:valueToAdd>')

parser = reqparse.RequestParser()
# With required=True, it only requires it if it is used in the post function, see test11's post
# it doesn't require the arguments then but it requires then when used in the dictmanage post
parser.add_argument('addkey', required=True, help='Key cannot be blank!')
parser.add_argument('addval', required=True, help='Value cannot be blank!')


if __name__ == '__main__':
    app.run()
