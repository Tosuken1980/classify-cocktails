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

preparation_options = ['blended', 'builded', 'layered', 'muddle', 'throw', 'shaken', 'stirred', 'swizzle']
temperature_options = ['ice drinks', 'up drinks', 'warm drinks']
appeareance_options = ['cloudy', 'clear', 'milky']

csv_obj = s3.get_object(Bucket=bucket_name, Key=object_name)
body = csv_obj['Body'].read().decode('utf-8')
df_cocktails = pd.read_csv(StringIO(body))

df_sample = df_cocktails.iloc[:10]

responses = []
st.set_page_config(page_title="Mi App", layout="wide", initial_sidebar_state="expanded")

st.title("Evaluation of Cocktail Ingredients and Classification")


for _ , cocktail in df_sample.iterrows():
    st.subheader(f"Cocktail: {cocktail['cocktail_name']}")

    col1, colsep, col2, col3, col4 = st.columns([3, 0.1, 1, 1, 1])

    # En la primera columna, poner la clasificación propuesta
    with col1:
        st.write(f"Ingredients: {cocktail['transformed_ingredients']}")
        show_directions = st.checkbox(f"Show directions?", value=False, key=f"checkbox_{cocktail['cocktail_name']}")
        if show_directions:
            st.write(cocktail["directions"])

    with colsep:
        st.write(" ")

    with col2:
        st.write(f"Preparation: {cocktail['cocktail_preparation']}")

        agreement_preparation = st.radio(f"Do you agree?", ("Yes", "No"), key=f"radio_prep_{cocktail['cocktail_name']}")

        # Si no están de acuerdo, pedir una propuesta
        if agreement_preparation == "No":
            alternative_preparation = st.selectbox(f"Proposed classification", 
                                               options=preparation_options, 
                                               key=f"select_prep_{cocktail['cocktail_name']}")
        else:
            alternative_preparation = None

    with col3:
        st.write(f"Type: {cocktail['temperature_serving']}")

        agreement_temperature = st.radio(f"Do you agree?", ("Yes", "No"), key=f"radio_temp_{cocktail['cocktail_name']}")

        # Si no están de acuerdo, pedir una propuesta
        if agreement_temperature == "No":
            #alternative_temperature = st.text_input(f"Proposed classification", key=f"text_temp_{cocktail['cocktail_name']}")
            alternative_temperature = st.selectbox(f"Proposed classification", 
                                               options=temperature_options, 
                                               key=f"select_temp_{cocktail['cocktail_name']}")
        else:
            alternative_temperature = None

    with col4:
        st.write(f"Appearence: {cocktail['cocktail_appearance']}")

        agreement_appearence = st.radio(f"Do you agree?", ("Yes", "No"), key=f"radio_appe_{cocktail['cocktail_name']}")

        # Si no están de acuerdo, pedir una propuesta
        if agreement_appearence == "No":
            alternative_appearence = st.selectbox(f"Proposed classification", 
                                               options=appeareance_options, 
                                               key=f"select_appe_{cocktail['cocktail_name']}")
        else:
            alternative_appearence = None

      # Guardar respuestas en la lista
    responses.append({
        'Cocktail name': cocktail['cocktail_name'],
        'Proposed preparation': alternative_preparation,
        'Proposed type': alternative_temperature,
        'Proposed appearence': alternative_appearence
    })
    st.write("---")

# Al hacer clic en enviar, se podría guardar la información o hacer algo con ella
if st.button("Send evaluation"):
    st.write("Thanks for your contribution!")
    df_responses = pd.DataFrame(responses)
    st.write("Evaluation Responses:")
    st.dataframe(df_responses) 