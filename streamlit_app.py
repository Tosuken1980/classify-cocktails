import streamlit as st

st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)
# Lista de cócteles y sus ingredientes
cocktails = [
    {"name": "Piña Colada", "ingredients": "Coconut cream, Pineapple juice, White rum", "classification": "Milky"},
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
