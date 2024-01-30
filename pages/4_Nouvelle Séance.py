import streamlit as st
import requests
import json

def insert_seance(data):
    url = 'https://apex.oracle.com/pls/apex/tporacle/seanceee/?limit=10000'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 201:
            st.success('Séance insérée avec succès!')
        else:
            st.warning(f'Échec de l\'insertion de la séance. Statut : {response.status_code}')
            st.write(response.json())

    except requests.exceptions.RequestException as e:
        st.error(f'Erreur lors de la requête HTTP : {e}')

def main():
    st.set_page_config(
        page_title="GymOline",
        page_icon=":muscle:",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.markdown("""
        <style>
        .st-emotion-cache-1wrcr25 {
            background-image:linear-gradient(315deg,#87bdd8 40%,#daebe8 47%);
        }
        body {
            font-family: 'arial', sans-serif;
            color: #333;
            margin: 0;
            padding: 0;
            
            font-width:bold;

        }
            .container {
                max-width: 800px;
                margin: 50px auto;
                padding: 20px;
                background-color: #fff;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        h1 {
            color: #0072b5;
            text-align:center;
        }
        h2 {
            color: #0072b5;
            text-align:center;
        }

    </style>
""", unsafe_allow_html=True)

    st.title('Insertion de Nouvelles Séances')

    # Formulaire pour la saisie des données de la séance
    id_s = st.number_input('ID_S', min_value=1, step=1)
    nom = st.text_input('Nom')
    type_seance = st.text_input('Type')
    niveau = st.number_input('Niveau', min_value=1, max_value=4, step=1)

    if st.button('Insérer la Séance'):
        # Vérifier que tous les champs sont remplis
        if id_s and nom and type_seance and niveau:
            data = {
                'id_s': id_s,
                'nom': nom,
                'type': type_seance,
                'niveau': niveau
            }

            insert_seance(data)
        else:
            st.warning('Veuillez remplir tous les champs.')

if __name__ == '__main__':
    main()
