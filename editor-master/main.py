from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS
from tree1.buildAST import buildAST, getInterpreter
from symantic.symantic import buildDiagram
from symantic.symantic import buildCode

app = Flask(__name__)
CORS(app)
# app.config['DEBUG'] = True
app.config['DEBUG'] = False


@app.route("/ast", methods=['POST'])
def hello():
    source = request.json['source']
    syntax = request.json['syntax']
    if source == '':
        return jsonify({'info': 'Source not found', 'error': -1})
    if syntax == '':
        return jsonify({'info': 'Syntax not found', 'error': -1})
    (info, x) = buildAST(source, syntax)
    return jsonify({'info': info, 'error': x})


@app.route("/interpreter", methods=['POST'])
def interpreter():
    source = request.json['source']
    syntax = request.json['syntax']
    if source == '':
        return jsonify({'info': 'Source not found', 'error': -1})
    if syntax == '':
        return jsonify({'info': 'Syntax not found', 'error': -1})
    (info, x) = getInterpreter(source, syntax)
    return jsonify({'info': info, 'error': x})


@app.route("/code", methods=['POST'])
def code():
    symantic = request.json['symantic']
    if symantic == '':
        return jsonify({'info': 'Symantic not found', 'error': -1})
    (info, x) = buildCode(symantic)
    return jsonify({'info': info, 'error': x})


@app.route("/diagram", methods=['POST'])
def diagram():
    symantic = request.json['symantic']
    if symantic == '':
        return jsonify({'info': 'Symantic not found', 'error': -1})
    (info, x) = buildDiagram(symantic)
    return jsonify({'info': info, 'error': x})


if __name__ == "__main__":
    app.run(port=8083)
