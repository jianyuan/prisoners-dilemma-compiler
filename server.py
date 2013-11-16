from check_source_code import check_source_code
from flask import Flask, request, jsonify
from subprocess2 import Popen, PIPE
from tempfile import NamedTemporaryFile
import json
import tourney.round_robin

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello world!'

@app.route('/verify', methods=['POST'])
def check():
    # sp = Popen(['python', 'check_source_code.py', '-c', request.form['source_code'], '-t', '5'], stdout=PIPE, stderr=PIPE)
    # out, err = sp.communicate(timeout=10)

    out = check_source_code(request.form['source_code'])

    resp = jsonify(out)
    resp.status_code = 200
    return resp

@app.route('/round_robin', methods=['POST'])
def round_robin():
    source_codes_in_json = request.form.get('source_codes')
    source_codes = json.loads(source_codes_in_json)

    players = []
    for player_id, source_code in source_codes.iteritems():
        players.append([int(player_id), source_code])

    out = tourney.round_robin.round_robin(iterations=request.form.get('iterations', type=int), players=players)

    resp = jsonify(out)
    resp.status_code = 200
    return resp

if __name__ == '__main__':
    app.run(debug=True)
