from fastapi import FastAPI, Depends
from pydantic import BaseModel
import pickle
import pandas as pd
import numpy as np
import uvicorn
from security.admin_security_routes import admin_security_router
from security.security_api_key import verificar_api_key
from db.database import database

app = FastAPI()

diabetes_ml_model = pickle.load(open('rf_model.pkl', 'rb'))

class DiabetesPredIn(BaseModel):
    embarazos: int
    glucosa: float
    presion_arterial: float
    espesor_piel: float
    insulina: float
    imc: float
    diabetes_pedigree_function: float
    edad: int
        
class DiabetesPredOut(BaseModel):
    tiene_diabetes: bool
    

@app.get('/')
async def index():
    return {'mensaje': 'Hello from Diabetes Prediction API'}


@app.post('/diabetes-predictions', response_model=DiabetesPredOut, status_code=201, dependencies=[Depends(verificar_api_key)])
async def procesar_prediccion_diabetes(diabetes_pred_in: DiabetesPredIn):
    
    print('Nuevo request para predecir un caso de diabetes:', diabetes_pred_in)
    
    input_values = [diabetes_pred_in.embarazos,
                     diabetes_pred_in.glucosa,
                     diabetes_pred_in.presion_arterial,
                     diabetes_pred_in.espesor_piel,
                     diabetes_pred_in.insulina,
                     diabetes_pred_in.imc,
                     diabetes_pred_in.diabetes_pedigree_function,
                     diabetes_pred_in.edad]
    
    # Creando un numpy array bidimensional
    # Un numpy array es un contenedor eficiente en memoria que permite realizar operaciones numéricas rápidas
    features = [np.array(input_values)]     
    
    # Creando un dataframe a partir del array bidimensional
    features_df = pd.DataFrame(features)
    
    # Generando las predicciones
    prediction_values = diabetes_ml_model.predict_proba(features_df)
    
    # Determinando la predicción final
    final_prediction = np.argmax(prediction_values)
    
    return DiabetesPredOut(tiene_diabetes = final_prediction)


app.include_router(admin_security_router, prefix='/admin', tags=['security-admin'])


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
    

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000, debug=True)