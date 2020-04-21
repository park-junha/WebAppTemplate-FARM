# Modules
from flask import Flask, request, render_template
from flask_restful import Resource, Api
from flask_cors import CORS
from werkzeug.exceptions import BadRequest, NotFound
import pymysql

# Non-serializable data types
from decimal import Decimal
from datetime import datetime, date

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

# API internal status codes
API_CODES = {
    'SUCCESS_READ': 280
    , 'SUCCESS_WRITE': 281
    , 'ERROR_MYSQL_METHOD': 480
    , 'ERROR_BAD_SQL_TYPE': 481
    , 'ERROR_MYSQL_EXECUTE': 490
}

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

# Make JSON serializable
# Decimals / Date / Datetime
def makeSerializable(response):
    try:
        for row in response:
            for key in row:
                if type(row[key]) is Decimal:
                    row[key] = float(row[key])
                elif type(row[key]) is date:
                    row[key] = row[key].strftime("%Y-%m-%d")
                elif type(row[key]) is datetime:
                    row[key] = row[key].strftime("%Y-%m-%d %H:%M:%S")
        return response
    except:
        raise Exception("Cannot make JSON serializable")

# Execute an SQL command
# Set cmd parameter to 'get' or 'post'
# Set conn parameter to connection object
# Optional parameters for additional options
def execute(sql, cmd, conn, options = None):
    response = {}
    try:
        with conn.cursor() as cur:
            # Execute one SQL command
            if type(sql) == str:
                cur.execute(sql)
            # Execute multiple SQL commands without committing
            elif type(sql) == list:
                for eachSql in sql:
                    cur.execute(eachSql)
            else:
                response['message'] = 'Request failed. Unknown or ambiguous parameter sql in execute().'
                response['code'] = API_CODES['ERROR_BAD_SQL_TYPE']
            if cmd is 'read':
                result = cur.fetchall()
                response['message'] = 'Successfully executed SQL query.'
                response['result'] = makeSerializable(result)
                response['code'] = API_CODES['SUCCESS_READ']
            elif cmd in 'write':
                conn.commit()
                response['message'] = 'Successfully committed SQL command.'
                response['code'] = API_CODES['SUCCESS_WRITE']
            else:
                response['message'] = 'Request failed. Unknown or ambiguous instruction given for MySQL command.'
                response['code'] = API_CODES['ERROR_MYSQL_METHOD']
    except:
        response['message'] = 'Request failed, could not execute MySQL command.'
        response['code'] = API_CODES['ERROR_MYSQL_EXECUTE']
    finally:
        print(response['message'], response['code'])
        return response

# REST API Templates for Flask / MySQL stack
# Connect to database, communicate with it, and return a response
# Raise an exception if things go wrong
# Disconnect from database when the process is complete

# All resources API template
class Items(Resource):
    # Use GET to fetch data
    def get(self):
        try:
            response = {}
            conn = connect()
            sql = """
                SELECT
                    item_uid
                    , item_name
                    , quantity
                FROM
                    Inventory
                ;"""

            # Returns list of JSONs
            # Each JSON represents a single row
            sql_response = execute(sql, 'read', conn)

            # Rearrange response to JSON with key by uid
            # This makes state management on UI easier
            items = {}
            for row in sql_response['result']:
                items[row['item_uid']] = row

            if sql_response['code'] == API_CODES['SUCCESS_READ']:
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

    # Use POST to add new data
    def post(self):
        try:
            data = request.get_json(force=True)

            response = {}
            conn = connect()

            if data.get('item_name') == None:
                response['message'] = 'Request failed, please provide item_name.'
                return response, 400
            if data.get('quantity') == None:
                response['message'] = 'Request failed, please provide quantity.'
                return response, 400

            sql = """
                INSERT INTO Inventory
                (
                    item_name
                    , quantity
                )
                VALUES
                (
                    \'""" + data['item_name'] + """\'
                    , """ + str(data['quantity']) + """
                )
                ;"""

            sql_response = execute(sql, 'write', conn)

            if sql_response['code'] == API_CODES['SUCCESS_WRITE']:
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

    # Use PATCH to make a non-idempotent update
    def patch(self):
        try:
            data = request.get_json(force=True)

            response = {}
            conn = connect()

            sql = []
            for uid_data in data:
                if data.get(uid_data) == None:
                    response['message'] = 'Request failed, insufficient data for item_uid: ' + str(uid_data) + '.'
                    return response, 400

                sql.append("""
                    UPDATE Inventory
                    SET
                        item_name = \'""" + data[uid_data]['item_name'] + """\'
                        , quantity = """ + str(data[uid_data]['quantity']) + """
                    WHERE
                        item_uid = \'""" + str(uid_data) + """\'
                    ;""")

            sql_response = execute(sql, 'write', conn)

            if sql_response['code'] == API_CODES['SUCCESS_WRITE']:
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

# Single item API template
class Item(Resource):
    # Use PUT to make an idempotent update
    def put(self, item_uid):
        try:
            data = request.get_json(force=True)

            response = {}
            conn = connect()

            if data.get('item_name') == None:
                response['message'] = 'Request failed, please provide item_name.'
                return response, 400
            if data.get('quantity') == None:
                response['message'] = 'Request failed, please provide quantity.'
                return response, 400

            sql = """
                UPDATE Inventory
                SET
                    item_name = \'""" + data['item_name'] + """\'
                    , quantity = """ + str(data['quantity']) + """
                WHERE
                    item_uid = \'""" + str(item_uid) + """\'
                ;"""

            sql_response = execute(sql, 'write', conn)

            if sql_response['code'] == API_CODES['SUCCESS_WRITE']:
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

    # Use DELETE to delete existing data
    def delete(self, item_uid):
        try:
            data = request.get_json(force=True)

            response = {}
            conn = connect()

            sql = """
                DELETE FROM Inventory
                WHERE
                    item_uid = \'""" + str(item_uid) + """\'
                ;"""

            sql_response = execute(sql, 'write', conn)

            if sql_response['code'] == API_CODES['SUCCESS_WRITE']:
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
api.add_resource(Items, '/api/v1/items')
api.add_resource(Item, '/api/v1/item/<string:item_uid>')

# Run the app
if __name__ == '__main__':
    app.run(host='localhost', port=8080)
