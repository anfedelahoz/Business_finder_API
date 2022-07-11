from unittest import result
from RPA.Browser.Selenium import Selenium
import business_table
import json
from datetime import datetime

browser_lib = Selenium()


def open_the_website(url):
    browser_lib.open_available_browser(url, headless=True)


def search_for(company, location):
    input_field = "css:input"
    browser_lib.input_text(input_field, company)
    browser_lib.press_keys(input_field, "ENTER")
    browser_lib.select_from_list_by_label("id:PROVINCIA", location)

def look_for_companies(top_results, company_search):
    companies_founded = browser_lib.get_text('xpath://*[@id="a_nacional"]')
    companies_list = []
    data = {"companies": companies_list}
    if companies_founded == "Empresas y Empresarios (0)":
        return {'Result': 'Resultados no encontrados'}
    best_score = 100
    actual_row = 0
    html_table = browser_lib.get_element_attribute("css:table#nacional", "outerHTML")
    table = business_table.read_table_from_html(html_table)
    while actual_row < top_results:
        for row in table:
            if actual_row >= top_results:
                break
            actual_company = row[0]
            actual_score = best_score


            for char in actual_company:
                if char not in company_search:
                    actual_score -= 1
            browser_lib.click_element(f'xpath://h3[contains(text(), "{row[0]}")]')
            store_screenshot(f"images/{row[0]}.png")
            companies_list.append(store_result(actual_score))
            browser_lib.go_back()
            actual_row += 1
    data_json = data
  
    return data_json


def look_best_fit_company(top_searchs, company_name):
    data = look_for_companies(top_searchs, company_name)
    best_score_fit = 0
    best_dict_fit = {}
    for dicti in data['companies']:
        for key, value in dicti.items():
            if key == 'Score_similitud':
                if value > best_score_fit:
                    best_score_fit = value
                    best_dict_fit = dicti

    best_fit = best_dict_fit
    return best_fit



def store_screenshot(filename):
    browser_lib.screenshot('xpath://*[@id="imprimir"]/table', filename=filename.replace(" ", "_"))


def store_result(score_similitud):
    html_table_results = browser_lib.get_element_attribute('xpath://*[@id="imprimir"]/table', "outerHTML")
    table_results = business_table.read_table_from_html_results(html_table_results)

    my_dict = {}
    for row in table_results:
        label = row[0].replace(':',"")
        value = row[1]
        my_dict[label] = value

    ICI = my_dict.get('ICI')
    NIT = my_dict.get('Nit')
    razon_social = my_dict.get('Razón Social')
    forma_juridica = my_dict.get('Forma Jurídica')
    departamento = my_dict.get('Departamento')
    direccion_actual = my_dict.get('Dirección Actual')
    telefono = my_dict.get('Teléfono')
    email = my_dict.get('Email')
    CIIU = my_dict.get('Actividad CIIU')
    fecha_constitucion = my_dict.get('Fecha Constitución')
    matricula_mercantil = my_dict.get('Matrícula Mercantil')
    ultimo_balance_einforma = my_dict.get('Último Balance disponible en eInforma')
    fecha_ultimo_dato = my_dict.get('Fecha Último Dato')
    fecha_actualizacion_camara_comercio = my_dict.get('Fecha Actualización Cámara Comercio')

    def validate_date(date_text):
        try:
            date_format = datetime.strptime(date_text, '%d/%m/%Y')
            return date_format
        except ValueError:
            return None
 

    result_dict = {
        "ICI": ICI,
        "NIT": NIT,
        "Razon_social": razon_social,
        "Forma_juridica": forma_juridica,
        "Departamento": departamento,
        "Direccion_actual": direccion_actual,
        "Telefono": telefono,
        "Email": email,
        "CIIU": CIIU,
        "Fecha_constitucion": None if fecha_constitucion == None else validate_date(fecha_constitucion) ,
        "Matricula_mercantil": matricula_mercantil,
        "Ultimo_balance_einforma": ultimo_balance_einforma,
        "Fecha_ultimo_dato": fecha_ultimo_dato,
        "Ultimo_balance_einforma": fecha_actualizacion_camara_comercio,
        "Score_similitud": score_similitud,
        "Screenshot": f'localhost:5000/images/{razon_social.replace(" ", "_")}.png' 
    }

    return result_dict

# Define a main() function that calls the other functions in order:
def main():
    try:
        company_name = "Olimpia"
        location = "BOGOTÁ"
        top_searchs = 3
        open_the_website("https://www.einforma.co/buscador-empresas-empresarios")
        try:
            search_for(company_name, location)
        except AssertionError:
            print('No encontrado')
            return {'Result':"Resultados no encontrados"}
        look_best_fit_company(top_searchs, company_name)
        
    finally:
        browser_lib.close_all_browsers()


# Call the main() function, checking that we are running as a stand-alone script:
if __name__ == "__main__":
    main()