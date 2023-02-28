import flask
import flask_cors
import os
import sys
from main import main
from database.DbHandler import DbHandler


app = flask.Flask(__name__)
flask_cors.CORS(app)

main()

@app.route("/")
def index():
    return "Hello World!"

@app.route("/api/receipts")
def get_receipts():
    db_handler = DbHandler()
    receipts = db_handler.get_receipts()
    return [receipt.toJSON() for receipt in receipts]