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

PROJECTS_DIR = 'dsls/'

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

DIR_NOT_DEFINED_JSON_RESPONSE = {'info': 'Project is not found', 'error': -1}

@app.after_request
def after_request(response):
    response.headers["Access-Control-Allow-Credentials"] = "true"
    # response.headers["Access-Control-Request-Headers"] = response.headers["Access-Control-Request-Headers"] + ",project"

    return response

@app.before_request
def before_request():
    request.username = request.headers.get('Username')
    print('Username: ' + str(request.username))
    request.project_name = request.headers.get('Project')
    print('Project name: ' + str(request.project_name))

    request.is_dir_defined = request.username and request.project_name

    request.user_dir = os.path.join(PROJECTS_DIR + str(request.username))
    request.dir = os.path.join(PROJECTS_DIR + str(request.username), str(request.project_name))


@app.route("/check-grammar", methods=['POST'])
def check_grammar():
    if not request.is_dir_defined:
        return DIR_NOT_DEFINED_JSON_RESPONSE

    source = request.json['source']
    syntax = request.json['syntax']

    info, x, _ = buildGrammar(source, syntax, request.dir)
    return jsonify({'info': info if x != -1 else 0, 'error': 0 if x != -1 else info})

@app.route("/syntax-diagram", methods=['POST'])
def syntax_diagram():
    if not request.is_dir_defined:
        return jsonify(DIR_NOT_DEFINED_JSON_RESPONSE)

    syntax = request.json['syntax']
    if syntax == '':
        return jsonify({'info': 'Syntax not found', 'error': -1})
    (info, x) = buildSyntaxDiagram(syntax, request.dir)
    return jsonify({'info': info, 'error': x})

@app.route("/ast", methods=['POST'])
def ast():
    if not request.is_dir_defined:
        return jsonify(DIR_NOT_DEFINED_JSON_RESPONSE)

    source = request.json['source']
    syntax = request.json['syntax']
    if source == '':
        return jsonify({'info': 'Source not found', 'error': -1})
    if syntax == '':
        return jsonify({'info': 'Syntax not found', 'error': -1})
    (info, x) = buildAST(source, syntax, request.dir)
    return jsonify({'info': info, 'error': x})


@app.route("/interpreter", methods=['POST'])
def interpreter():
    if not request.is_dir_defined:
        return jsonify(DIR_NOT_DEFINED_JSON_RESPONSE)

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
    if not request.is_dir_defined:
        return jsonify(DIR_NOT_DEFINED_JSON_RESPONSE)

    symantic = request.json['symantic']
    if symantic == '':
        return jsonify({'info': 'Symantic not found', 'error': -1})

    with open('symantic.txt', 'w', encoding='utf-8') as file:
        file.write(symantic)

    (info, x) = buildCode(symantic, request.dir)
    return jsonify({'info': info, 'error': x})


@app.route("/diagram", methods=['POST'])
def diagram():
    if not request.is_dir_defined:
        return jsonify(DIR_NOT_DEFINED_JSON_RESPONSE)

    symantic = request.json['symantic']
    if symantic == '':
        return jsonify({'info': 'Symantic not found', 'error': -1})
    (info, x) = buildDiagram(symantic, request.dir)
    return jsonify({'info': info, 'error': x})

@app.route('/files/<path:path>')
def get_file(path):
    # if not request.is_dir_defined:
    #     return jsonify(DIR_NOT_DEFINED_JSON_RESPONSE)

    return send_from_directory('', path)


@app.route('/get-user-projects')
def get_user_projects():
    print('Get user project received for: ' + request.username)

    rootdir = PROJECTS_DIR + request.username

    projects = []
    if not os.path.exists(rootdir):
        return jsonify({'projects': projects})
    for it in os.scandir(rootdir):
        if it.is_dir():
           projects.append(it.name)
    return jsonify({'projects': projects})


@app.route('/save', methods=['POST'])
def save_project():
    if not request.is_dir_defined:
        return jsonify(DIR_NOT_DEFINED_JSON_RESPONSE)

    source = request.json['source']
    syntax = request.json['syntax']
    symantic = request.json['symantic']

    with open(os.path.join(request.dir, 'source.txt'), 'wb') as temp_file:
        temp_file.write(source.encode('UTF-8'))
    with open(os.path.join(request.dir, 'syntax.txt'), 'wb') as temp_file:
        temp_file.write(syntax.encode('UTF-8'))
    with open(os.path.join(request.dir, 'symantic.txt'), 'wb') as temp_file:
        temp_file.write(symantic.encode('UTF-8'))

    return jsonify({'info': 'ok', 'error': ''})

@app.route('/get-sources')
def get_project():
    if not request.is_dir_defined:
        return jsonify(DIR_NOT_DEFINED_JSON_RESPONSE)
    source_path = os.path.join(request.dir, 'source.txt')
    syntax_path = os.path.join(request.dir, 'syntax.txt')
    symantic_path = os.path.join(request.dir, 'symantic.txt')

    source = ''
    syntax = 'grammar **Grammar name**;\n' \
             '**parser rules**\n' \
             '\n' \
             '**lexer rules**'
    symantic = '**Object name**\n' \
               'VAR\n' \
               'REQUIRED\n' \
               'PROVIDED\n' \
               'STATE'

    if (os.path.exists(source_path)):
        with open(source_path, 'r', encoding='UTF-8') as temp_file:
            source = temp_file.read()

    if (os.path.exists(syntax_path)):
        with open(syntax_path, 'r', encoding='UTF-8') as temp_file:
            syntax = temp_file.read()

    if (os.path.exists(symantic_path)):
        with open(symantic_path, 'r', encoding='UTF-8') as temp_file:
            symantic = temp_file.read()

    return jsonify({'info': 'ok', 'error': '', 'source': source, 'syntax': syntax, 'symantic': symantic})


@app.route('/create-project', methods=['POST'])
def create_project():
    print('Create  received for: ' + request.username + ',project name: ' + request.project_name)

    os.makedirs(request.user_dir, exist_ok=True)
    os.makedirs(request.dir, exist_ok=True)

    return jsonify({'status': 'Project created'})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8083)
