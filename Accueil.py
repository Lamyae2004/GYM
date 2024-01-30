import streamlit as st

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

st.title("Welcome to GymOnline")
image_path = "salle-sport-halteres-au-sol (1).jpg"
st.image(image_path, use_column_width=True)
# Contenu de la page d'accueil


st.markdown("""
     Que vous soyez un débutant passionné, un athlète chevronné ou quelque part entre les deux, notre application est conçue pour répondre à tous vos besoins en matière de remise en forme.
     
    
""")

st.header("Why us?")
st.markdown("""
    Nous comprenons que chaque parcours de remise en forme est unique. C'est pourquoi nous offrons des plans d'entraînement personnalisés, adaptés à votre niveau, à vos objectifs et à votre emploi du temps. Que vous aspiriez à perdre du poids, à gagner en muscle, à améliorer votre endurance ou simplement à rester actif, nous sommes là pour vous guider à chaque étape.
""")
st.header("Our Services")
st.markdown("""
    + Plans d'entraînement personnalisés 

+ Suivi des progrès 

+ Nutrition équilibrée 

+ Communauté engageante 
""")
st.header("Contact us")
st.markdown("""
   + Gmail: GymOnline@gmail.com
   + Tel: +212611370522
   
""")
