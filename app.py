from distutils.command.config import config
from attr import field
import requests
from werkzeug.utils import cached_property
from flask import Flask, jsonify, request, send_from_directory, abort
from flask_restx import Api, Resource, fields
from marshmallow import Schema, fields
from flask_swagger_ui import get_swaggerui_blueprint
from tasks import open_the_website, search_for, look_best_fit_company, look_for_companies
from werkzeug.middleware.proxy_fix import ProxyFix

class CompanyQuerySchema(Schema):
    company = fields.String(required=True)
    location = fields.String(required=True)
    top_searchs = fields.Integer(required=True)



app = Flask(__name__, static_folder= 'images')
api = Api(app, version = '1.0', title='API REST with Robot-framework for company consultation', description='Andres De la Hoz')

# api = Api(app, version= '1.0.0', title='API REST with Robot-framework for company consultation',
# description='Andres De la Hoz')

# company_get_args = reqparse.RequestParser()
# company_get_args.add_argument("company", type=str, help="Name of the company", required=True)
# company_get_args.add_argument("department", type=str, help="Department/ubication of the company", required=True)
# company_get_args.add_argument("search_limit", type=int, help="Limit of searchs to perform", required=True)

model = api.model('Model', {
    "CIIU": fields.String,
    "Direccion_actual": fields.String,
    "Email": fields.String,
    "Fecha_constitucion": fields.String,
    "Fecha_ultimo_dato": fields.String,
    "Forma_juridica": fields.String,
    "ICI": fields.String,
    "Matricula_mercantil": fields.String,
    "NIT": fields.String,
    "Razon_social": fields.String,
    "Departamento": fields.String,
    "Score_similitud": fields.Integer,
    "Screenshot": fields.String,
    "Telefono": fields.String,
    "Ultimo_balance_einforma": fields.String
})

schema = CompanyQuerySchema()

@app.route('/', methods=['GET'])
def home():
    return """<h1>Welcome to API for company consultation</h1>
    <h3>Options for querying:</h6>
    <p>/allCompanies?company=BAIRES&department=BOGOTÁ&top_searchs=3</p>
    <p>/bestFit?company=BAIRES&department=BOGOTÁ&top_searchs=3</p>
    """



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


class AllCompanies(Resource):
    #@api.marshal_with(model)
    def get(self, company, department, search_limit):
        # args= company_get_args.parse_args()
        
        print('hey')
        open_the_website("https://www.einforma.co/buscador-empresas-empresarios")
        try:
            search_for(company, department)
        except:
            return jsonify({'Result': 'Resultados no encontrados'})
        look_for_companies(search_limit, company)
        results = look_for_companies(search_limit, company)
        print('hey')
        return jsonify(results)
api.add_resource(AllCompanies, "/allcompanies/<string:company>/<string:department>/<int:search_limit>")



class BestFit(Resource):
    #@api.marshal_with(model)
    def get(self, company, department, search_limit):
        errors = schema.validate(request.args)
        if not errors:
            abort(errors, 422)
        
        open_the_website("https://www.einforma.co/buscador-empresas-empresarios")
        try:
            search_for(company, department)
        except:
            return jsonify({'Result': 'Resultados no encontrados'})
        look_for_companies(search_limit, company)
        results = look_best_fit_company(search_limit, company)
        return jsonify(results)

api.add_resource(BestFit, "/bestfit/<string:company>/<string:department>/<int:search_limit>")




if __name__ == '__main__':
    app.run(debug=True, use_debugger=False, use_reloader=True)