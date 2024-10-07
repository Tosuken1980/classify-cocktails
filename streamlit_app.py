from openai import OpenAI
import json
import os
import pandas as pd
from datetime import datetime
from zoneinfo import ZoneInfo
import streamlit as st
from PIL import Image
import io
import boto3
import requests
from io import StringIO


client = OpenAI(api_key=st.secrets['OPENAI_API_KEY'])
s3 = boto3.client('s3', aws_access_key_id=st.secrets['aws_access_key_id'], aws_secret_access_key=st.secrets['aws_secret_access_key'])

bucket_name = st.secrets["bucket_mixo_data"]
object_name = "cocktails_info_v6.csv"


csv_obj = s3.get_object(Bucket=bucket_name, Key=object_name)
body = csv_obj['Body'].read().decode('utf-8')
df_cocktails = pd.read_csv(StringIO(body))


# Lista de cócteles y sus ingredientes
cocktails = [
    {"name": "Piña Colada", "ingredients": df_cocktails.iloc[2]["transformed_ingredients"], "classification": "Milky"},
    {"name": "Margarita", "ingredients": "Tequila, Lime juice, Triple sec", "classification": "Clear"},
    {"name": "Pi", "ingredients": df_cocktails.iloc[4]["transformed_ingredients"], "classification": "Milky"},
    {"name": "Margarita", "ingredients": "Tequila, Lime juice, Triple sec", "classification": "Clear"},
    # Añadir más cócteles aquí
]

st.title("Evaluación de Ingredientes y Clasificación de Cócteles")

# Iterar sobre los cócteles para generar el formulario
for cocktail in cocktails:
    st.subheader(f"Cóctel: {cocktail['name']}")
    st.write(f"Ingredientes: {cocktail['ingredients']}")
    st.write(f"Clasificación propuesta: {cocktail['classification']}")
    
    # Preguntar si están de acuerdo con la clasificación
    agreement = st.radio(f"¿Estás de acuerdo con la clasificación de {cocktail['name']}?", ("Sí", "No"))

    # Si no están de acuerdo, pedir una propuesta
    if agreement == "No":
        alternative = st.text_input(f"Propuesta de clasificación para {cocktail['name']}")
    else:
        alternative = None

    st.write("---")

# Al hacer clic en enviar, se podría guardar la información o hacer algo con ella
if st.button("Enviar evaluación"):
    st.write("¡Gracias por tu evaluación!")
    # Aquí puedes guardar las respuestas en una base de datos o archivo