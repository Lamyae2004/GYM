import streamlit as st
import requests
import pandas as pd

def fetch_seance_data():
    url = 'https://apex.oracle.com/pls/apex/tporacle/entraineuree/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Lève une exception pour les codes d'erreur HTTP

        if response.status_code == 200:
            data = response.json()

            # Accéder aux données de la clé "items"
            items = data.get("items", [])

            # Vérifier si les données sont une liste d'objets (dictionnaires)
            if isinstance(items, list) and all(isinstance(item, dict) for item in items):
                return items
            else:
                st.warning('Les données de la table SEANCE ne sont pas au format attendu.')
                return None

        else:
            st.warning(f'La requête a réussi, mais le statut était {response.status_code}.')
            return None

    except requests.exceptions.RequestException as e:
        st.error(f'Erreur lors de la requête HTTP : {e}')
        return None

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

    st.title('Affichage et Filtrage des Entraineurs')

    # Récupérer les données de la table SEANCE
    seance_data = fetch_seance_data()

    # Vérifier si les données ont été récupérées
    if seance_data is not None:
        # Filtrer par type
        selected_type = st.selectbox('Filtrer par nom', ['Tous'] + list(set(str(item['nom']) for item in seance_data)))

        # Filtrer par niveau
        selected_niveau = st.selectbox('Filtrer par date de naissance', ['Tous'] + list(set(str(item['date_naiss']) for item in seance_data)))

        # Appliquer les filtres
        filtered_data = seance_data
        if selected_type != 'Tous':
            filtered_data = [item for item in filtered_data if str(item['nom']) == selected_type]
        if selected_niveau != 'Tous':
            filtered_data = [item for item in filtered_data if str(item['date_naiss']) == selected_niveau]

        # Afficher les données filtrées
        st.write(f'Données de la table Entraineur (Filtrées par nom: {selected_type}, date de naissance: {selected_niveau}):')
        #st.json(filtered_data)
        formatted_trainers = []
    for trainer in filtered_data:
        formatted_trainers.append({
            "code": trainer['codee'],
            "prénom": trainer['prenom'],
            "Nom": trainer['nom'],
            "date_naissance ": trainer['date_naiss'],
            "Son_email": trainer['email'],
            "numéro_téléphone": trainer['numtele'],    
        })
    st.table(formatted_trainers)

if __name__ == '__main__':
    main()
