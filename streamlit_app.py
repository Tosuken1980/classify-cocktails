from openai import OpenAI
import numpy as np
import pandas as pd
from datetime import datetime
import streamlit as st
import boto3
from io import StringIO


client = OpenAI(api_key=st.secrets['OPENAI_API_KEY'])
s3 = boto3.client('s3', aws_access_key_id=st.secrets['aws_access_key_id'], aws_secret_access_key=st.secrets['aws_secret_access_key'])

bucket_name = st.secrets["bucket_mixo_data"]
object_name = "cocktails_selected.csv"

# Options for the selection on each category
preparation_options = ['blended', 'builded', 'layered', 'muddle', 'throw', 'shaken', 'stirred', 'swizzle', 'other']
temperature_options = ['iced drinks', 'up drinks', 'warm drinks', 'other']
appeareance_options = ['cloudy', 'clear', 'milky', 'other']

csv_obj = s3.get_object(Bucket=bucket_name, Key=object_name)
body = csv_obj['Body'].read().decode('utf-8')
df_selection = pd.read_csv(StringIO(body))
n_cocktails = df_selection.shape[0]
batch_ids = np.sort(df_selection['batch_id'].unique()) + 1


responses = []
st.set_page_config(page_title="Cocktail classification", layout="wide", initial_sidebar_state="expanded")
st.title("Evaluation of Cocktail Ingredients and Classification")

col_ini1, col_ini2 = st.columns([1, 3])
with col_ini1:
    st.markdown("<h3 style='text-align: left;'>Please enter your name:</h3>", unsafe_allow_html=True)
    evaluator_name = st.text_input("Name", " ", label_visibility='hidden')
    st.markdown("<h3 style='text-align: left;'>Please select a batch for classify 10 cocktails:</h3>", unsafe_allow_html=True)
    selected_batch_id = st.selectbox("Batch", batch_ids, label_visibility='hidden')

df_sample = df_selection[df_selection.batch_id==selected_batch_id - 1]


for _ , cocktail in df_sample.iterrows():
    st.subheader(f"Cocktail: {cocktail['cocktail_name']}")

    col1, colsep, col2, col3, col4 = st.columns([3, 0.1, 1, 1, 1])

    with col1:
        st.markdown(f"**Ingredients:** {cocktail['transformed_ingredients']}")
        show_directions = st.checkbox(f"Show directions?", value=False, key=f"checkbox_{cocktail['cocktail_name']}")
        if show_directions:
            st.write(cocktail["directions"])

    with colsep:
        st.write(" ")

    with col2:
        st.markdown(f"<span style='color:gray;font-weight:bold;'>Preparation:</span> <span style='color:red; font-weight:bold;'>{cocktail['cocktail_preparation']}</span>", unsafe_allow_html=True)

        agreement_preparation = st.radio(f"Do you agree?", ("Yes", "No"), key=f"radio_prep_{cocktail['cocktail_name']}")

        if agreement_preparation == "No":
            alternative_preparation = st.selectbox(f"Proposed classification", 
                                               options=preparation_options, 
                                               key=f"select_prep_{cocktail['cocktail_name']}")
            if alternative_preparation == "other":
                alternative_preparation = st.text_input("Specify:", label_visibility='hidden')
        else:
            alternative_preparation = None

    with col3:
        st.markdown(f"<span style='color:gray; font-weight:bold;'>Type:</span> <span style='color:red; font-weight:bold;'>{cocktail['temperature_serving']}</span>", unsafe_allow_html=True)
        agreement_temperature = st.radio(f"Do you agree?", ("Yes", "No"), key=f"radio_temp_{cocktail['cocktail_name']}")

        if agreement_temperature == "No":
            alternative_temperature = st.selectbox(f"Proposed classification", 
                                               options=temperature_options, 
                                               key=f"select_temp_{cocktail['cocktail_name']}")
        else:
            alternative_temperature = None

    with col4:
        st.markdown(f"<span style='color:gray;font-weight:bold;'>Appearence:</span> <span style='color:red; font-weight:bold;'>{cocktail['cocktail_appearance']}</span>", unsafe_allow_html=True)
        agreement_appearence = st.radio(f"Do you agree?", ("Yes", "No"), key=f"radio_appe_{cocktail['cocktail_name']}")

        if agreement_appearence == "No":
            alternative_appearence = st.selectbox(f"Proposed classification", 
                                               options=appeareance_options, 
                                               key=f"select_appe_{cocktail['cocktail_name']}")
        else:
            alternative_appearence = None

    responses.append({
        'Cocktail name': cocktail['cocktail_name'],
        'Proposed preparation': alternative_preparation,
        'Proposed type': alternative_temperature,
        'Proposed appearence': alternative_appearence
    })
    st.write("---")

if st.button("Send evaluation"):
    if evaluator_name:

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"survey/batch_{selected_batch_id - 1}_{evaluator_name}_{timestamp}.csv"
        
        # Convertir las respuestas en un DataFrame
        df_responses = pd.DataFrame(responses)

        csv_buffer = StringIO()
        df_responses.to_csv(csv_buffer, index=False)
        
        s3.put_object(Bucket=bucket_name, Key=filename, Body=csv_buffer.getvalue())
        
        st.write("Thanks for your contribution!")
        st.write("Evaluation Responses:")
        st.dataframe(df_responses)
    else:
        st.warning("Please enter your name before submitting.")
