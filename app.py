from distutils.command.config import config
from tkinter.tix import Tree
from attr import field
import requests
from flask import Flask, jsonify, request, abort, send_from_directory
from marshmallow import Schema, fields
from flask_swagger_ui import get_swaggerui_blueprint
from tasks import open_the_website, search_for, look_best_fit_company, look_for_companies


class CompanyQuerySchema(Schema):
    company = fields.String(required=True)
    location = fields.String(required=True)
    top_searchs = fields.Integer(required=True)




app = Flask(__name__, static_folder= 'images')
# api = Api(app, version= '1.0.0', title='API REST with Robot-framework for company consultation',
# description='Andres De la Hoz')

schema = CompanyQuerySchema()


@app.route('/static/<path:path>', methods=['GET'])
def send_static(path):
    return send_from_directory('static', path)



SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'API REST with Robot-framework for company consultation'
    }
)


app.register_blueprint(swaggerui_blueprint)


@app.route('/allCompanies', methods=['GET'], endpoint='/allCompanies')
# @api.doc(params={'company': 'Olimpia', 'departmen': 'BOGOTÁ', 'top_searchs': 3})
def get_all():
    errors = schema.validate(request.args)
    if not errors:
         abort(errors, 422)
    company = request.args.get('company')
    department = request.args.get('department')
    top_searchs = int(request.args.get('top_searchs'))
    open_the_website("https://www.einforma.co/buscador-empresas-empresarios")
    search_for(company, department)
    look_for_companies(top_searchs, company)
    results = look_for_companies(top_searchs, company)
    return jsonify(results)


@app.route('/bestFit', methods=['GET'], endpoint='/bestFit')
# @api.doc(params={'company': 'Olimpia', 'departmen': 'BOGOTÁ', 'top_searchs': 3})
def get_best():
    errors = schema.validate(request.args)
    if not errors:
         abort(errors, 422)
    company = request.args.get('company')
    department = request.args.get('department')
    top_searchs = int(request.args.get('top_searchs'))
    open_the_website("https://www.einforma.co/buscador-empresas-empresarios")
    search_for(company, department)
    look_for_companies(top_searchs, company)
    results = look_best_fit_company(top_searchs, company)
    return jsonify(results)




if __name__ == '__main__':
    app.run(debug=True, use_debugger=False, use_reloader=True)