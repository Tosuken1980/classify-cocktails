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

st.title("Evaluation of Cocktail Ingredients and Classification")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)
# Lista de cócteles y sus ingredientes
cocktails = df_cocktails.sample(5)


for cocktail in cocktails:
    st.subheader(f"Cóctel: {cocktail['cocktail_name']}")
    st.write(f"Ingredientes: {cocktail['ingredients']}")
    st.write(f"Clasificación propuesta: {cocktail['classification']}")
    
    # Preguntar si están de acuerdo con la clasificación
    agreement = st.radio(f"¿Estás de acuerdo con la clasificación de {cocktail['cocktail_name']}?", ("Sí", "No"))

    # Si no están de acuerdo, pedir una propuesta
    if agreement == "No":
        alternative = st.text_input(f"Propuesta de clasificación para {cocktail['cocktail_name']}")
    else:
        alternative = None

    st.write("---")

# Al hacer clic en enviar, se podría guardar la información o hacer algo con ella
if st.button("Enviar evaluación"):
    st.write("¡Gracias por tu evaluación!")
    # Aquí puedes guardar las respuestas en una base de datos o archivo