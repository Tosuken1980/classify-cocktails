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

df_sample = df_cocktails.iloc[:4]

st.title("Evaluation of Cocktail Ingredients and Classification")

for _ , cocktail in df_sample.iterrows():
    st.subheader(f"Cocktail: {cocktail['cocktail_name']}")
    st.write(f"Ingredients: {cocktail['transformed_ingredients']}")
        # Crear dos columnas
    col1, col2 = st.columns([2, 1])  # Puedes ajustar el ancho de las columnas con los valores de la lista

    # En la primera columna, poner la clasificación propuesta
    with col1:
        st.write(f"Proposed classification: {cocktail['cocktail_preparation']}")

    # En la segunda columna, poner la opción del radio
    with col2:
        agreement = st.radio(f"Do you agree?", ("Yes", "No"), key=f"radio_{cocktail['cocktail_name']}")

        # Si no están de acuerdo, pedir una propuesta
        if agreement == "No":
            alternative = st.text_input(f"Proposed classification for {cocktail['cocktail_name']}", key=f"text_{cocktail['cocktail_name']}")
        else:
            alternative = None


    st.write("---")

# Al hacer clic en enviar, se podría guardar la información o hacer algo con ella
if st.button("Send evaluation"):
    st.write("Thanks for your contribution!")
    # Aquí puedes guardar las respuestas en una base de datos o archivo