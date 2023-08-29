from flask import Flask, Response
import random


app = Flask(__name__)

@app.route("/")
def home():
    file_id = random.randrange(3) + 1
    file_name = f'resp{file_id}.xml'
    with open(file_name, 'r') as fh:
        lines = fh.readlines()
        return Response(lines, mimetype="text/xml")
