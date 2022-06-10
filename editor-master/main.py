import sys
import os

from flask import Flask, send_from_directory, request, make_response
from flask import jsonify
from flask_cors import CORS
from tree.buildAST import buildGrammar, buildAST, getInterpreter, buildSyntaxDiagram
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

@app.route('/login', methods=['POST'])
def login_post():
    username = request.json['username']
    # password = request.json['password']
    # remember = True if request.json['remember'] else False

    # user = User.query.filter_by(email=email).first()
    #
    # # check if the user actually exists
    # # take the user-supplied password, hash it, and compare it to the hashed password in the database
    # if not user or not check_password_hash(user.password, password):
    #     flash('Please check your login details and try again.')
    #     return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page
    #
    # # if the above check passes, then we know the user has the right credentials
    # return redirect(url_for('main.profile'))

    resp = make_response(jsonify(request.json))
    resp.set_cookie('username', username, secure=True)
    # resp.headers["Access-Control-Allow-Origin"] = "*"
    # resp.headers["Access-Control-Allow-Credentials"] = "true"
    return resp

@app.after_request
def after_request(response):
    response.headers["Access-Control-Allow-Credentials"] = "true"
    return response

@app.before_request
def before_request():
    print('Cookies: ' + str(request.cookies))
    request.username = request.headers.get('Username')
    print('Username ' + str(request.username))

@app.route("/check-grammar", methods=['POST'])
def check_grammar():
    source = request.json['source']
    syntax = request.json['syntax']
    if source == '':
        return jsonify({'info': 'Source not found', 'error': -1})
    info, x, _ = buildGrammar(source, syntax)
    return jsonify({'info': info if x != -1 else 0, 'error': 0 if x != -1 else info})

@app.route("/syntax-diagram", methods=['POST'])
def syntax_diagram():
    syntax = request.json['syntax']
    if syntax == '':
        return jsonify({'info': 'Syntax not found', 'error': -1})
    (info, x) = buildSyntaxDiagram(syntax)
    return jsonify({'info': info, 'error': x})

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

    with open('symantic.txt', 'w', encoding='utf-8') as file:
        file.write(symantic)

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

@app.route('/get-user-projects')
def get_user_projects():
    print('Get user project received for: ' + request.username)

    rootdir = 'dsls/' + request.username

    projects = []
    if not os.path.exists(rootdir):
        return jsonify({'projects': projects})
    for it in os.scandir(rootdir):
        if it.is_dir():
           projects.append(it.name)
    return jsonify({'projects': projects})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8083)
