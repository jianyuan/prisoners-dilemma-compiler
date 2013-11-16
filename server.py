from flask import Flask, request, jsonify
from subprocess2 import Popen, PIPE
from tempfile import NamedTemporaryFile
import json

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello world!'

@app.route('/verify', methods=['POST'])
def check():
    sp = Popen(['python', '-c', request.form['source_code']], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    out, err = sp.communicate(request.form['input'] if 'input' in request.form else None, timeout=5)

    resp = jsonify({
      'stdout': out,
      'stderr': err
    })

    resp.status_code = 200

    return resp

@app.route('/round_robin', methods=['POST'])
def round_robin():
    source_codes = request.form.getlist('source_code[]')
    source_code_files = []

    for source_code in source_codes:
        tmp_file = NamedTemporaryFile()
        tmp_file.write(source_code)
        tmp_file.seek(0)
        source_code_files.append(tmp_file)

    for source_code_file in source_code_files:
        print source_code_file.name
        source_code_file.close()

    return jsonify({'ok': True})

if __name__ == '__main__':
    app.run(debug=True)
