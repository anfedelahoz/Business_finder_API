from tkinter.tix import Tree
from attr import field
from flask import Flask, jsonify, request, abort
from flask_restful import Resource, Api
from marshmallow import Schema, fields
from tasks import open_the_website, search_for, look_best_fit_company, look_for_companies


class CompanyQuerySchema(Schema):
    company = fields.String(required=True)
    location = fields.String(required=True)
    top_searchs = fields.Integer(required=True)


app = Flask(__name__)


schema = CompanyQuerySchema()

# spec = APISpec(
#     title= 'flask-api-swagger-doc',
#     version= '1.0.0',
#     openapi_version = '3.0.2'
#     plugins = [FlaskPuging(), MarshallowPlugin()]
# )



@app.route('/search_all_companies', methods=['GET'])
def get():
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


@app.route('/search_best_fit_company', methods=['GET'])
def get():
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