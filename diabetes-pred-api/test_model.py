import pickle
import pandas as pd
import numpy as np


# Cargando el modelo:
diabetes_ml_model = pickle.load(open('rf_model.pkl', 'rb'))

# Definiendo la función de predicción:
# Orden de los valores: ['Pregnancies', 'PlasmaGlucose', 'DiastolicBloodPressure', 'TricepsThickness', 'SerumInsulin', 'BMI', 'DiabetesPedigree', 'Age']
def predict(input_values):
    
    # Creando un numpy array bidimensional
    # Un numpy array es un contenedor eficiente en memoria que permite realizar operaciones numéricas rápidas
    features = [np.array(input_values)]
    print('features', features)    
    
    # Creando un dataframe a partir del array bidimensional
    features_df = pd.DataFrame(features)
    print('features_df', features_df)
    
    # Generando las predicciones
    prediction_values = diabetes_ml_model.predict_proba(features_df)
    print('prediction_values', prediction_values)


    # Determinando la predicción final
    final_prediction = np.argmax(prediction_values)
    print('final_prediction', final_prediction)



positive_case_values_1 = (5, 114, 101, 43, 70, 36.49531966, 0.079190164, 38)
positive_case_values_2 = (9, 103, 78, 25, 304, 29.58219193, 1.282869847, 43)
positive_case_values_3 = (5,114,101,43,70,36.49531966,0.079190164,38)

negative_case_values_1 = (0,171,80,34,23,43.50972593,1.213191354,21)
negative_case_values_2 = (0,109,56,44,26,20.21133193,0.780654857,26)


predict(positive_case_values_1)
#predict(positive_case_values_2)
#predict(positive_case_values_3)

#predict(negative_case_values_1)
#predict(negative_case_values_2)
