from cgitb import html
from tkinter.messagebox import NO
from turtle import end_fill
from RPA.Browser.Selenium import Selenium
import business_table

browser_lib = Selenium()


def open_the_website(url):
    browser_lib.open_available_browser(url)


def search_for(company, location):
    input_field = "css:input"
    browser_lib.input_text(input_field, company)
    browser_lib.press_keys(input_field, "ENTER")
    browser_lib.select_from_list_by_label("id:PROVINCIA", location)

def look_for_companies(top_results):
    companies_founded = browser_lib.get_text('xpath://*[@id="a_nacional"]')
    
    if companies_founded == "Empresas y Empresarios (0)":
        print("Resultados no encontrados" )
        return "Resultados no encontrados" 

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
                if char not in actual_company:
                    actual_score -= 1
            browser_lib.click_element(f'xpath://h3[contains(text(), "{row[0]}")]')
            store_screenshot(f"output/{row[0]}.png")
            print(store_result())
            browser_lib.go_back()
            actual_row += 1

            
        

def store_screenshot(filename):
    browser_lib.screenshot(filename=filename)

def store_result():
    ICI = browser_lib.get_text('xpath://*[@id="imprimir"]/table/tbody/tr[2]/td[2]/a') if browser_lib.is_element_visible('xpath://*[@id="imprimir"]/table/tbody/tr[2]/td[2]/a') else None
    NIT = browser_lib.get_text('xpath://*[@id="imprimir"]/table/tbody/tr[3]/td[2]/a') if browser_lib.is_element_visible('xpath://*[@id="imprimir"]/table/tbody/tr[3]/td[2]/a') else None
    razon_social = browser_lib.get_text('xpath://*[@id="imprimir"]/table/tbody/tr[4]/td[2]') if browser_lib.is_element_visible('xpath://*[@id="imprimir"]/table/tbody/tr[4]/td[2]') else None
    forma_juridica = browser_lib.get_text('xpath://*[@id="imprimir"]/table/tbody/tr[5]/td[2]') if browser_lib.is_element_visible('xpath://*[@id="imprimir"]/table/tbody/tr[5]/td[2]') else None
    departamento = browser_lib.get_text('xpath://*[@id="imprimir"]/table/tbody/tr[6]/td[2]') if browser_lib.is_element_visible('xpath://*[@id="imprimir"]/table/tbody/tr[5]/td[2]') else None
    direccion_actual = browser_lib.get_text('xpath://*[@id="imprimir"]/table/tbody/tr[7]/td[2]/a') if browser_lib.is_element_visible('xpath://*[@id="imprimir"]/table/tbody/tr[7]/td[2]/a') else None
    telefono = browser_lib.get_text('xpath://*[@id="imprimir"]/table/tbody/tr[8]/td[2]/a') if browser_lib.is_element_visible('xpath://*[@id="imprimir"]/table/tbody/tr[8]/td[2]/a') else None
    email = browser_lib.get_text('xpath://*[@id="imprimir"]/table/tbody/tr[9]/td[2]/a') if browser_lib.is_element_visible('xpath://*[@id="imprimir"]/table/tbody/tr[9]/td[2]/a') else None
    CIIU = browser_lib.get_text('xpath://*[@id="imprimir"]/table/tbody/tr[10]/td[2]') if browser_lib.is_element_visible('xpath://*[@id="imprimir"]/table/tbody/tr[10]/td[2]') else None
    fecha_constitucion = browser_lib.get_text('xpath://*[@id="imprimir"]/table/tbody/tr[11]/td[2]') if browser_lib.is_element_visible('xpath://*[@id="imprimir"]/table/tbody/tr[11]/td[2]') else None
    matricula_mercantil = browser_lib.get_text('xpath://*[@id="imprimir"]/table/tbody/tr[12]/td[2]/a') if browser_lib.is_element_visible('xpath://*[@id="imprimir"]/table/tbody/tr[12]/td[2]/a') else None
    ultimo_balance_einforma = browser_lib.get_text('xpath://*[@id="imprimir"]/table/tbody/tr[14]/td[2]') if browser_lib.is_element_visible('xpath://*[@id="imprimir"]/table/tbody/tr[14]/td[2]') else None
    fecha_ultimo_dato = browser_lib.get_text('xpath://*[@id="imprimir"]/table/tbody/tr[14]/td[2]') if browser_lib.is_element_visible('xpath://*[@id="imprimir"]/table/tbody/tr[14]/td[2]') else None
    fecha_actualizacion_camara_comercio = browser_lib.get_text('xpath://*[@id="imprimir"]/table/tbody/tr[16]/td[2]') if browser_lib.is_element_visible('xpath://*[@id="imprimir"]/table/tbody/tr[16]/td[2]') else None

    result_dict = {
        "ICI": ICI,
        "NIT": NIT,
        "razon_social": razon_social,
        "forma_juridica": forma_juridica,
        "departamento": departamento,
        "direccion_actual": direccion_actual,
        "telefono": telefono,
        "email": email,
        "CIIU": CIIU,
        "fecha_constitucion": fecha_constitucion,
        "matricula_mercantil": matricula_mercantil,
        "ultimo_balance_einforma": ultimo_balance_einforma,
        "fecha_ultimo_dato": fecha_ultimo_dato,
        "ultimo_balance_einforma": fecha_actualizacion_camara_comercio
    }
    return result_dict

# Define a main() function that calls the other functions in order:
def main():
    try:
        open_the_website("https://www.einforma.co/buscador-empresas-empresarios")
        search_for("baires", "BOGOTÁ")
        look_for_companies(9)
    finally:
        browser_lib.close_all_browsers()


# Call the main() function, checking that we are running as a stand-alone script:
if __name__ == "__main__":
    main()