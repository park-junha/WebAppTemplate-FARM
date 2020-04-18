# Modules
from flask import Flask, request, render_template
from flask_restful import Resource, Api
from flask_cors import CORS
from werkzeug.exceptions import BadRequest, NotFound
import pymysql

# Your database credentials file
from dbcreds import db_credentials as dbc

# Initialize Flask app
app = Flask(__name__)

# Allow cross-origin resource sharing
cors = CORS(app, resources={r'/api/*': {'origins': '*'}})

# Set to False when deploying to a live service
app.config['DEBUG'] = True

# Setup Flask app as REST API
api = Api(app)

# Connect to MySQL database
# Returns a connection object
def connect():
    global dbc
    try:
        conn = pymysql.connect( dbc['host'],
                                user=dbc['user'],
                                port=dbc['port'],
                                passwd=dbc['password'],
                                db=dbc['schema'],
                                charset=dbc['charset'],
                                cursorclass=pymysql.cursors.DictCursor)
        print("Successfully established a connection to MySQL database.")
        return conn
    except:
        print("Failed to establish a connection to MySQL database.")
        raise Exception("Failure connecting to MySQL database")

# Disconnect from MySQL database
def disconnect(conn):
    try:
        conn.close()
        print("Successfully disconnected from MySQL database.")
    except:
        print("Could not properly disconnect from MySQL database.")
        raise Exception("Failure disconnecting from MySQL database")

# Execute an SQL command
# Set cmd parameter to 'get' or 'post'
# Set conn parameter to connection object
def execute(sql, cmd, conn):
    response = {}
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            if cmd is 'get':
                result = cur.fetchall()
                response['message'] = 'Successfully executed SQL query.'
                response['result'] = result
                response['code'] = 280
            elif cmd in 'post':
                conn.commit()
                response['message'] = 'Successfully committed SQL command.'
                response['code'] = 281
            else:
                response['message'] = 'Request failed. Unknown or ambiguous instruction given for MySQL command.'
                response['code'] = 490
    except:
        response['message'] = 'Request failed, could not execute MySQL command.'
        response['code'] = 491
    finally:
        print(response['message'])
        return response

# REST API for Flask / MySQL stack
# Connect to database, communicate with it, and return a response
# Raise an exception if things go wrong
# Disconnect from database when the process is complete
class FlaskMySQL(Resource):
    # HTTP method GET
    def get(self):
        try:
            response = {}
            conn = connect()
            sql = """   SELECT
                            \'SampleValue\'
                        AS SampleColumn;"""

            sql_response = execute(sql, 'get', conn)

            if sql_response['code'] == 280:
                response['message'] = 'Request successful.'
                response['result'] = items
                response['code'] = sql_response['code']
                return response, 200
            else:
                response['message'] = sql_response['message']
                response['code'] = sql_response['code']
                return response, 400

        except:
            raise BadRequest('Request failed, please try again later.')
        finally:
            disconnect(conn)

    # HTTP method POST
    def post(self):
        try:
            data = request.get_json(force=True)

            if data.get('Value1') == None:
                raise BadRequest('Request failed, please provide Value1.')
            if data.get('Value2') == None:
                raise BadRequest('Request failed, please provide Value2.')

            response = {}
            conn = connect()

            sql = """   INSERT INTO SampleTable
                        (
                            SampleColumn1,
                            SampleColumn2
                        )
                        VALUES
                        (
                            \'""" + data['Value1'] + """\',
                            \'""" + data['Value2'] + """\'
                        );"""

            sql_response = execute(sql, 'post', conn)

            if sql_response['code'] == 281:
                response['message'] = 'Request successful.'
                response['result'] = data
                response['code'] = sql_response['code']
                return response, 200
            else:
                response['message'] = sql_response['message']
                response['result'] = data
                response['code'] = sql_response['code']
                return response, 400
        except:
            raise BadRequest('Request failed, please try again later.')
        finally:
            disconnect(conn)

# Define routes for each API
api.add_resource(FlaskMySQL, '/api/v1/flaskmysql')

# Run the app
if __name__ == '__main__':
    app.run(host='localhost', port=8080)
