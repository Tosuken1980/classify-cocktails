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

# Lista de cócteles y sus ingredientes
cocktails = [
    {"name": df_sample.iloc[0]["cocktail_name"], "ingredients": df_sample.iloc[0]["transformed_ingredients"], "classification": df_sample.iloc[0]["cocktail_preparation"]},
    {"name": df_sample.iloc[1]["cocktail_name"], "ingredients": df_sample.iloc[1]["transformed_ingredients"], "classification": df_sample.iloc[1]["cocktail_preparation"]},
    {"name": df_sample.iloc[2]["cocktail_name"], "ingredients": df_cocktails.iloc[2]["transformed_ingredients"], "classification": df_sample.iloc[2]["cocktail_preparation"]},
    {"name": df_sample.iloc[3]["cocktail_name"], "ingredients": df_sample.iloc[3]["transformed_ingredients"], "classification": df_sample.iloc[3]["cocktail_preparation"]}
    # Añadir más cócteles aquí
]

st.title("Evaluation of Cocktail Ingredients and Classification")

for _ , cocktail in df_sample.iterrows():
    st.subheader(f"Cocktail: {cocktail['cocktail_name']}")
    st.write(f"Ingredients: {cocktail['ingredients']}")
    st.write(f"Proposed classification: {cocktail['classification']}")

    # Preguntar si están de acuerdo con la clasificación
    agreement = st.radio(f"Do you agree with the classification for  {cocktail['cocktail_name']}?", ("Yes", "No"))

    # Si no están de acuerdo, pedir una propuesta
    if agreement == "No":
        alternative = st.text_input(f"Proposed classification for {cocktail['cocktail_name']}")
    else:
        alternative = None

    st.write("---")

# Al hacer clic en enviar, se podría guardar la información o hacer algo con ella
if st.button("Send evaluation"):
    st.write("Thanks for your contribution!")
    # Aquí puedes guardar las respuestas en una base de datos o archivo