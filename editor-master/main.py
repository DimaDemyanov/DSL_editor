import sys

from flask import Flask, send_from_directory
from flask import request
from flask import jsonify
from flask_cors import CORS
from tree.buildAST import buildGrammar, buildAST, getInterpreter
from symantic.symantic import buildDiagram
from symantic.symantic import buildCode
from healthcheck import HealthCheck, EnvironmentDump

import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="{asctime} {levelname:<8} {message}",
    style='{',
    handlers=[
        logging.FileHandler("main.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

app = Flask(__name__)
CORS(app)
# app.config['DEBUG'] = True
app.config['DEBUG'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

health = HealthCheck()
envdump = EnvironmentDump()
app.add_url_rule("/healthcheck", "healthcheck", view_func=lambda: health.run())
app.add_url_rule("/environment", "environment", view_func=lambda: envdump.run())

@app.route("/check-grammar", methods=['POST'])
def check_grammar():
    source = request.json['source']
    syntax = request.json['syntax']
    if source == '':
        return jsonify({'info': 'Source not found', 'error': -1})
    info, x, _ = buildGrammar(source, syntax)
    return jsonify({'info': info if x != -1 else 'Grammar is fine', 'error': 0 if x != -1 else info})

@app.route("/ast", methods=['POST'])
def ast():
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

@app.route('/files/<path:path>')
def get_file(path):
    return send_from_directory('public', path)

# @app.route('/files/AST/<path:path>')
# def get_ast_picture(path):
#     return send_from_directory('public', path)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8083)
