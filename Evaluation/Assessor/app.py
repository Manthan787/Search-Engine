from flask import Flask, render_template, request, Response
from flask.json import jsonify
from app.Utils.ESClient import ESClient
from app.Utils.Writer import GradesWriter
from app.config import TEMPLATE_DIR, STATIC_DIR
import json

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)


@app.route('/')
def getIndex():
    return render_template('index.html')


@app.route('/search')
def search():
    query = request.args.get('q')
    client = ESClient()
    results = client.search(query)
    return Response(json.dumps(results),  mimetype='application/json')


@app.route('/store', methods=['POST'])
def store():
    data = request.get_json(force=True)
    print data
    queryID = data['queryID']
    grades = data['grades']
    print "Received Grades: %s" %(len(grades))
    writer = GradesWriter(grades)
    filename = "queryID-{}".format(queryID)
    writer.write(filename, queryID)
    return jsonify(success=True)


if __name__ == '__main__':
    app.run()
