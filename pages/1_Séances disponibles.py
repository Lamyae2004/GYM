import streamlit as st
import requests
import pandas as pd

def fetch_seance_data():
    url = 'https://apex.oracle.com/pls/apex/tporacle/seanceee'
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

def show_selected_sessions_schedule(seance_data):
    selected_seance = st.multiselect("Sélectionner des séances pour afficher les horaires", [seance['id_s'] for seance in seance_data])

    for session_id in selected_seance:  # Correction ici
        schedule_data = fetch_session_schedule(session_id)
        if schedule_data:
            st.write(f"Horaire pour la séance {session_id}:")
            st.table(schedule_data)
        else:
            st.warning(f"Aucun horaire disponible pour la séance {session_id}.")

def fetch_session_schedule(session_id):
    url = f'https://apex.oracle.com/pls/apex/tporacle/horaireee/?limit=10000&SEANCE_id_S={session_id}'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        schedule_data = response.json()
        formatted_schedule = []
        for session_schedule in schedule_data['items']:
            if (session_schedule["seance_id_s"] == session_id):
                formatted_schedule.append({
                    "jour": session_schedule["jour"],
                    "heure_de_debut": session_schedule["heure_debut"],
                    "duree": session_schedule["durree"],
                    "gymsalle": session_schedule["gym_salle"],
                    "numero de seance": session_schedule["seance_id_s"],  # Change to the desired column name
                })
                return formatted_schedule


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

    st.title('Affichage et Filtrage des Séances')

    # Récupérer les données de la table SEANCE
    seance_data = fetch_seance_data()

    if seance_data is not None:
        # Filtrer par type
        selected_type = st.selectbox('Filtrer par Type', ['Tous'] + list(set(str(item['type']) for item in seance_data)))

        # Filtrer par niveau
        selected_niveau = st.selectbox('Filtrer par Niveau', ['Tous'] + list(set(str(item['niveau']) for item in seance_data)))

        # Appliquer les filtres
        filtered_data = seance_data
        if selected_type != 'Tous':
            filtered_data = [item for item in filtered_data if str(item['type']) == selected_type]
        if selected_niveau != 'Tous':
            filtered_data = [item for item in filtered_data if str(item['niveau']) == selected_niveau]

        st.metric("Nombre de séances disponibles", len(filtered_data))
        distinct_types = set(item['type'] for item in filtered_data)
        st.metric("Types de séances distincts", len(distinct_types))
        st.write(f'Types de séances distincts: {", ".join(distinct_types)}')
        # Afficher les données filtrées
        st.write(f'Données de la table SEANCE (Filtrées par Type: {selected_type}, Niveau: {selected_niveau}):')
        formatted_sessions = []
    for session in filtered_data:
        formatted_sessions.append({
            "numero de seance": session['id_s'],
            "Nom de la séance": session['nom'],
            "Type de séance": session['type'],
            "Niveau": session['niveau'],
        })
    st.table(formatted_sessions)

        # Ajouter un expander pour les horaires des séances sélectionnées
    with st.expander("Afficher les horaires des séances sélectionnées"):
            show_selected_sessions_schedule(filtered_data)

if __name__ == '__main__':
    main()