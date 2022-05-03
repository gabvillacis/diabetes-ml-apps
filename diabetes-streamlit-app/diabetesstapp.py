import streamlit as st
import requests
import os
import json

API_URLBASE = os.getenv("API_URLBASE")
API_KEY = os.getenv("API_KEY")

def execute_prediction_request(embarazos: int, glucosa: float, presion_arterial: float, espesor_piel: float,
                                insulina: float, imc: float, diabetes_pedigree_function: float, edad: int) -> bool:

    payload = {
        'embarazos': embarazos,
        'glucosa': glucosa,
        'presion_arterial': presion_arterial,
        'espesor_piel': espesor_piel,
        'insulina': insulina,
        'imc': imc,
        'diabetes_pedigree_function': diabetes_pedigree_function,
        'edad': edad
    }
    
    headers_dict = {'x-api-key': API_KEY}
    
    response = requests.post(API_URLBASE + '/diabetes-predictions', headers=headers_dict, data=json.dumps(payload))
    
    if response.status_code == 201:       
        return response.json().get('tiene_diabetes')
    else:
        response.raise_for_status()


header_container = st.container()

with header_container:
    st.title('Formulario de Predicción de Diabetes')
    st.write('Llene el siguiente formulario y compruebe un posible caso de Diabetes')
    

with st.form(key='diabetes-pred-form'):
    col1, col2 = st.columns(2)
    
    embarazos = col1.slider(label='Nro. de Embarazos:', min_value=0, max_value=15)
    glucosa = col1.text_input(label='Glucosa:')
    presion_arterial = col1.text_input(label='Presión Arterial:')
    espesor_piel = col1.text_input(label='Espesor Piel:')
    insulina = col2.text_input(label='Insulina:')
    imc = col2.text_input(label='Indice Masa Corporal:')
    diabetes_pedigree = col2.text_input(label='Función Diabetes Pedigree:')
    edad = col2.slider(label='Edad:', min_value=1, max_value=120)
    
    submit = st.form_submit_button(label='Check')
    
    if submit:
        try:
            tiene_diabetes = execute_prediction_request(embarazos, glucosa, presion_arterial, espesor_piel,
                                                        insulina, imc, diabetes_pedigree, edad)
            
            if tiene_diabetes:
                st.error('Los datos ingresados infieren un caso de Diabetes POSITIVO!')
            else:
                st.success('Los datos ingresados infieren un caso de Diabetes NEGATIVO!')
                
        except requests.exceptions.RequestException as ex:
            st.error('Oops!! Algo salió mal en la comunicación con el servicio de predicción.')
