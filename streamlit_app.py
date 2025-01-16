from openai import OpenAI
import numpy as np
import pandas as pd
from datetime import datetime
import streamlit as st
import boto3
import re
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

def get_weekly_batch():
    start_date = datetime.strptime("2025-01-20", "%Y-%m-%d")
    today = datetime.now()
    weeks_since_start = (today - start_date).days // 7
    return (weeks_since_start % 20) + 1

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email) is not None

current_batch = get_weekly_batch()
df_sample = df_selection[df_selection['batch_id'] == current_batch]
batch_ids = np.sort(df_selection['batch_id'].unique())


responses = []
st.set_page_config(page_title="Cocktail classification", layout="wide", initial_sidebar_state="expanded")
st.title("Evaluation of a Cocktail")
st.markdown(f"<h3 style='color:gray;font-weight:bold;'>Working on batch </span> <span style='color:blue; font-weight:bold;'>{current_batch}</span>", unsafe_allow_html=True)

col_ini1, col_ini2 = st.columns([1, 3])
with col_ini1:
    st.markdown("<h3 style='text-align: left;'>Please enter your name:</h3>", unsafe_allow_html=True)
    evaluator_name = st.text_input("Name", " ", label_visibility='hidden', key=f"text_input_name")
    st.markdown("<h3 style='text-align: left;'>Please enter your email:</h3>", unsafe_allow_html=True)
    evaluator_email = st.text_input("email", " ", label_visibility='hidden', key=f"text_input_email")


for _ , cocktail in df_sample.iterrows():
    st.subheader(f"Cocktail: {cocktail['cocktail_name']}")

    col1, colsep, col2, col3, col4, col5, col6 = st.columns([3, 0.1, 1, 1, 1, 1, 1])

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
                alternative_preparation = st.text_input("Specify:", label_visibility='hidden', key=f"text_input_prep_{cocktail['cocktail_name']}")
        else:
            alternative_preparation = None

    with col3:
        st.markdown(f"<span style='color:gray; font-weight:bold;'>Type:</span> <span style='color:red; font-weight:bold;'>{cocktail['temperature_serving']}</span>", unsafe_allow_html=True)
        agreement_temperature = st.radio(f"Do you agree?", ("Yes", "No"), key=f"radio_temp_{cocktail['cocktail_name']}")

        if agreement_temperature == "No":
            alternative_temperature = st.selectbox(f"Proposed classification", 
                                               options=temperature_options, 
                                               key=f"select_temp_{cocktail['cocktail_name']}")
            if alternative_temperature == "other":
                alternative_temperature = st.text_input("Specify:", label_visibility='hidden', key=f"text_input_temp_{cocktail['cocktail_name']}")
        else:
            alternative_temperature = None

    with col4:
        st.markdown(f"<span style='color:gray;font-weight:bold;'>Appearence:</span> <span style='color:red; font-weight:bold;'>{cocktail['cocktail_appearance']}</span>", unsafe_allow_html=True)
        agreement_appearence = st.radio(f"Do you agree?", ("Yes", "No"), key=f"radio_appe_{cocktail['cocktail_name']}")

        if agreement_appearence == "No":
            alternative_appearence = st.selectbox(f"Proposed classification", 
                                               options=appeareance_options, 
                                               key=f"select_appe_{cocktail['cocktail_name']}")
            if alternative_appearence == "other":
                alternative_appearence = st.text_input("Specify:", label_visibility='hidden', key=f"text_input_appea_{cocktail['cocktail_name']}")
        else:
            alternative_appearence = None

    with col5:
        st.markdown(f"<span style='color:gray;font-weight:bold;'>Ice:</span> <span style='color:red; font-weight:bold;'>{cocktail['ice_type']}</span>", unsafe_allow_html=True)
        agreement_ice = st.radio(f"Do you agree?", ("Yes", "No"), key=f"radio_ice_{cocktail['cocktail_name']}")

        if agreement_ice == "No":
            alternative_ice = st.text_input("Specify:", label_visibility='hidden', key=f"text_input_ice_{cocktail['cocktail_name']}")
        else:
            alternative_ice = None

    with col6:
        st.markdown(f"<span style='color:gray;font-weight:bold;'>Glassware:</span> <span style='color:red; font-weight:bold;'>{cocktail['standard_glass_type']}</span>", unsafe_allow_html=True)
        agreement_glass = st.radio(f"Do you agree?", ("Yes", "No"), key=f"radio_glass_{cocktail['cocktail_name']}")

        if agreement_glass == "No":
            alternative_glass = st.text_input("Specify:", label_visibility='hidden', key=f"text_input_glass_{cocktail['cocktail_name']}")
        else:
            alternative_glass = None

    responses.append({
        'Cocktail name': cocktail['cocktail_name'],
        'Proposed preparation': alternative_preparation,
        'Proposed type': alternative_temperature,
        'Proposed appearence': alternative_appearence,
        'Proposed ice': alternative_ice,
        'Proposed glassware': alternative_glass
    })
    st.write("---")

if st.button("Send evaluation"):
    if is_valid_email(evaluator_email.strip()) and evaluator_name.strip() != "":

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"survey/batch_{current_batch}_{evaluator_name}_{timestamp}.csv"
        
        # Convertir las respuestas en un DataFrame
        responses[-1]['User name'] = evaluator_name.strip()
        responses[-1]['User email'] = evaluator_email.strip()

        df_responses = pd.DataFrame(responses)

        csv_buffer = StringIO()
        df_responses.to_csv(csv_buffer, index=False)
        
        s3.put_object(Bucket=bucket_name, Key=filename, Body=csv_buffer.getvalue())
        
        st.write("Thanks for your contribution!")
        st.write("Evaluation Responses:")
        st.dataframe(df_responses)
    else:
        st.warning("Please enter your name and a valid email address before submitting.")
