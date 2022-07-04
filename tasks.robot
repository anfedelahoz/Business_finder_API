*** Settings ***
Documentation       Template robot main suite.

Library             business_table.py
Library             RPA.Browser.Selenium
Library             RPA.Tables
Library             RPA.JSON

*** Variables ***
${EINFORMA_URL}     https://www.einforma.co/buscador-empresas-empresarios
${COMPANY}          OLIMPIA
${LOCATION}         BOGOTÁ
${TOP_RESULTS}      2
${RESULTS}          0
${BEST_SCORE}       100
${BEST_FIT_SCORE}   0
${BEST_FIT_TEXT}    ""
${COMPANIES}        Create List

*** Tasks ***
Minimal task
    Open EINFORMA search page
    Search for    ${COMPANY}
    Select Location
    Wait Until Element Is Visible    id:logo

    ${ACTUAL_ROW}=   Set Variable      ${0}
    ${ACTUAL_COMPANY}=     Set Variable     " "
    
    ${companies_founded}=   Get Text   xpath://*[@id="a_nacional"]
    IF      "${companies_founded}"!="Empresas y Empresarios (0)"

        WHILE   ${RESULTS} < ${TOP_RESULTS}     limit=30
            ${html_table}=    Get Business table
            ${table}=    Read Table From Html    ${html_table}
            ${dimensions}=    Get Table Dimensions    ${table}
            ${first_row}=    Get Table Row    ${table}    ${0}
            ${first_cell}=    RPA.Tables.Get Table Cell    ${table}    ${0}    ${0}
            ${table_len}=    Get Length     ${table}
            #${before}=      Convert string to JSON   {"Companies": []}
            FOR    ${row}    IN    @{table}

                Exit For Loop If  ${ACTUAL_ROW} == ${TOP_RESULTS}
                ${ACTUAL_ROW}=    Evaluate    ${ACTUAL_ROW} + 1
                Log To Console    ${row}
                
                ${ACTUAL_COMPANY}=   Set Variable  ${row[0]}

                ${ACTUAL_SCORE}=  Set Variable  ${BEST_SCORE}  
                FOR  ${CHAR}  IN   ${ACTUAL_COMPANY}
                    ${ACTUAL_SCORE}=  Evaluate  ${ACTUAL_SCORE} - 10
                    
                END

                IF   ${ACTUAL_SCORE} > ${BEST_FIT_SCORE}
                    ${BEST_FIT_SCORE}=  Set Variable  ${ACTUAL_SCORE}
                    ${BEST_FIT_TEXT}=   Set Variable   ${ACTUAL_COMPANY}
                END


                Click Element   xpath://h3[contains(text(), "${row[0]}")]
                Collect screenshot    ${row[0]}


                ${ICI}=     Get Text     xpath://*[@id="imprimir"]/table/tbody/tr[2]/td[2]/a
                ${NIT}=     Get Text     xpath://*[@id="imprimir"]/table/tbody/tr[3]/td[2]/a
                ${razon_social}=     Get Text     xpath://*[@id="imprimir"]/table/tbody/tr[4]/td[2]
                ${forma_juridica}=      Get Text     xpath://*[@id="imprimir"]/table/tbody/tr[5]/td[2]
                ${departamento}=      Get Text      xpath://*[@id="imprimir"]/table/tbody/tr[6]/td[2]
                ${direccion_actual}=      Get Text     xpath://*[@id="imprimir"]/table/tbody/tr[7]/td[2]/a
                ${telefono}=      Get Text     xpath://*[@id="imprimir"]/table/tbody/tr[8]/td[2]/a
                ${email}=      Get Text    xpath://*[@id="imprimir"]/table/tbody/tr[9]/td[2]/a
                ${actividad_CIIU}=    Get Text    xpath://*[@id="imprimir"]/table/tbody/tr[10]/td[2]
                ${fecha_constitucion}=     Get Text    xpath://*[@id="imprimir"]/table/tbody/tr[11]/td[2]
                ${matricula_mercantil}=     Get Text   xpath://*[@id="imprimir"]/table/tbody/tr[12]/td[2]/a

                
                # ${company}=     Create Dictionary with   ${ICI}    ${NIT}    ${razon_social}     ${forma_juridica}     ${departamento}     ${direccion_actual}     ${telefono}    ${email}    ${actividad_CIIU}    ${fecha_constitucion}    ${matricula_mercantil}    ${ACTUAL_SCORE}
                # ${after}=       Add to JSON     ${before}    $.Companies   ${company}
      
                Go Back

            END

            # Log To Console  ${after}
            TRY
                Click Element   xpath://a[contains(text(), 'siguiente')]
            EXCEPT
                Log To Console   "No more companies were founded"
                BREAK
            END
        END


        Log To Console    ${ACTUAL_ROW}
        Log To Console    ${BEST_FIT_SCORE}
        Log To Console    ${BEST_FIT_TEXT}
        # Click Element   xpath://h3[contains(text(), "${BEST_FIT_TEXT}")]

    ELSE
        Log to Console    "Heyyyyy"
    END


*** Keywords ***
Open EINFORMA search page
    Open Available Browser   ${EINFORMA_URL}    headless=True
    Run Keyword And Ignore Error    Accept Google Consent

Search for
    [Arguments]    ${text}
    Input Text    id:search2    ${text}
    Click Button    id:boton_buscador_nacional
    Wait Until Page Contains Element   search2

Select Location
    Select From List By Label   id:PROVINCIA  ${LOCATION}

Collect screenshot
    [Arguments]    ${name}
    Screenshot    xpath://*[@id="imprimir"]/table    output${/}${name}.png
 
Get Business table
    ${html_table}=     Get Element Attribute    css:table#nacional    outerHTML
    RETURN      ${html_table}
    
Go to next page 
    ${table_len}=    Get Length     ${table}
    IF  ${table_len}  >  {12}
        Click Element   xpath://a[contains(text(), 'siguiente')]
    ELSE      
        Click Element    css:table#nacional    outerHTML
    END

Create Dictionary with 
    [Arguments]    ${ICI}   ${NIT}    ${razon_social}   ${forma_juridica}   ${departamento}    ${direccion_actual}    ${telefono}   ${email}    ${actividad_CIIU}    ${fecha_constitucion}     ${matricula_mercantil}    ${score_similitud}
    ${Dictionary}=   Create Dictionary  'ICI'=${ICI}   'NIT'=${NIT}   'razon_social'=${razon_social}  'forma_juridica'=${forma_juridica}   'departamento'=${departamento}    'direccion_actual'=${direccion_actual}  'telefono'=${telefono}  'email'=${email}   'actividad_CIIU'=${actividad_CIIU}     'fecha_constitucion'=${fecha_constitucion}   'matricula_mercantil'=${matricula_mercantil}  'score_similitud'=${score_similitud}
    Log To Console     ${Dictionary}