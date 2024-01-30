import streamlit as st
import requests

def fetch_trainers():
    url = 'https://apex.oracle.com/pls/apex/tporacle/entraineuree/?limit=10000'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        trainers_data = response.json()
        return trainers_data['items']

    except requests.exceptions.RequestException as e:
        st.error(f'Erreur lors de la requête HTTP pour récupérer les entraineurs : {e}')

def fetch_sessions():
    url = 'https://apex.oracle.com/pls/apex/tporacle/seanceee/?limit=10000'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        sessions_data = response.json()
        return sessions_data['items']

    except requests.exceptions.RequestException as e:
        st.error(f'Erreur lors de la requête HTTP pour récupérer les séances : {e}')

def fetch_session_schedule():
    url = f'https://apex.oracle.com/pls/apex/tporacle/horaireee/?limit=10000'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        schedule_data = response.json()
        return schedule_data['items']

    except requests.exceptions.RequestException as e:
        st.error(f'Erreur lors de la requête HTTP : {e}')

def insert_session_schedule(data):
    url = 'https://apex.oracle.com/pls/apex/tporacle/horaireee/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        st.success('Insertion réussie!')
    except requests.exceptions.RequestException as e:
        st.error(f'Erreur lors de la requête HTTP pour insérer la séance : {e}')

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
        img {
            max-width: 100%;
            height: auto;
            border-radius: 10px;
            margin-bottom: 20px;
        }
    </style>
""", unsafe_allow_html=True)

    st.title("Formulaire d'insertion de séance hebdomadaire")

    entraineur = fetch_trainers()
    seance = fetch_sessions()

    # Form inputs
    trainer_codee = st.selectbox('Selectionner le code de l\'entraineur', ['Tous'] + list(set(str(item['codee']) for item in entraineur)))
    session_id =st.selectbox('selectionner le code de la session', ['Tous'] + list(set(str(item['id_s']) for item in seance)))
    day = st.selectbox("Sélectionner le jour de la semaine", ["LUNDI", "MARDI", "MERCREDI", "JEUDI", "VENDREDI"])
    start_time = st.text_input("Heure de début")
    duration = st.number_input("Durée de la séance (en minutes)", min_value=1, max_value=60, value=30)
    gym_salle = st.text_input("Salle de gym")
    
    if st.button("Insérer la séance"):
        # Data to be inserted
           data = {
            "entraineur_codee": trainer_codee,
            "jour": day,
            "heure_debut": str(start_time),
            "durree": duration,
            "gym_salle": gym_salle,
            "seance_id_s": session_id,
               }
           horaire_data = fetch_session_schedule()
           seances_existantes = [item for item in horaire_data if 'seance_id_s' in item and str(item['seance_id_s']) == session_id]
           seance_fin = [item for item in seances_existantes if 'jour' in item and str(item['jour']) == day]
           if not seance_fin:
            insert_session_schedule(data)
           else:
            st.error("Une séance existe déjà pour ce jour.")

        # Perform validation and insertion
          

if __name__ == "__main__":
    main()
