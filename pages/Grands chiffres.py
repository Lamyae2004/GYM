import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# Fonction pour récupérer les données depuis Oracle Apex
def get_data_from_oracle_apex():
    url = 'https://apex.oracle.com/pls/apex/tporacle/horaireee/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)
    data = response.json()['items']  
    return data

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

    st.title("Graphiques Séances Programmées")

    # récupération des données depuis Oracle Apex
    data = get_data_from_oracle_apex()

    # Crétion d'un DataFrame pandas à partir des données
    df = pd.DataFrame(data)

    
    # le graphique à barres pour le nombre de séances par plage horaire
    st.subheader("Nombre de séances par plage horaire")
    bar_chart = px.bar(df, x='heure_debut', title='Nombre de séances par plage horaire')
    st.plotly_chart(bar_chart)

    # le nombre de séances par jour
    df['nombre_de_seances'] = 1  # Chaque ligne représente une séance
    df_grouped = df.groupby('jour').sum().reset_index()

    #le graphique à courbes pour le nombre de séances par jour de la semaine
    st.subheader("Nombre de séances par jour de la semaine")
    line_chart = px.line(df_grouped, x='jour', y='nombre_de_seances', title='Nombre de séances par jour de la semaine')
    st.plotly_chart(line_chart)

if __name__ == '__main__':
    main()