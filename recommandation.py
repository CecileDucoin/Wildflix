import streamlit as st
import pandas as pd
import os
from sklearn.neighbors import NearestNeighbors
import streamlit as st
import requests
import PIL
import seaborn as sns
import matplotlib.pyplot as plt
import numpy
from streamlit_authenticator import Authenticate
import plotly.express as px
import plotly.graph_objects as go


st.set_page_config(
    page_title="Wildflix",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""<style> [data-testid='stAppViewContainer']{
            background-color : #232846;}</style>""", unsafe_allow_html=True)

st.image('imagewild.png', width = 100)
titres_onglets = ['Bienvenue', 'Recommandation', 'Dashboard', 'Horaires et accès']
onglet1, onglet2, onglet3, onglet4= st.tabs(titres_onglets)

with onglet1:
    st.write('Bienvenue sur la page Wildflix :sunglasses: :popcorn:')
    st.image('imagewild.png', width = 400)
    st.write('Votre cinéma a ouvert ses portes en 1986. Depuis lors, il propose une expérience cinématographique unique à ses visiteurs.')
    st.write('Votre plateforme de recommandation  WildFlix vous offre une fonctionnalité de recommandation personnalisée.')
    st.write('Les utilisateurs peuvent indiquer un film et le système leur suggérera des films correspondants.')
    st.write('Cela permet aux spectateurs de découvrir de nouveaux films en fonction de leurs goûts.')

with onglet2:
    df = pd.read_csv('mon_fichier_skl_2.csv')
    st.title('Moteur de recommandation de films')

    col1, col2, col3 = st.columns(3)  # Créez trois colonnes

    with col1:
        st.image('cinema.jpg', width=300)

    with col2:
        st.image('cinema2.jpg', width=300)

    with col3:
        st.image('cinema3.jpg', width=300)
    
    choix = st.selectbox('Sélectionne un film, je te donnerai 5 recommandations de film : ', options=df.movie_title , index = 0 )
    # Remplacer "YOUR_API_KEY" par votre clé API OMDb
    OMDB_API_KEY = "3df042ed"
    def get_movie_poster(choix):
        response = requests.get(f"https://www.omdbapi.com/?t={choix}&apikey={OMDB_API_KEY}")
        data = response.json()
        if data["Response"] == "True":
            return data["Poster"]
        else:
            return None
        
    def get_movie_details(choix):
        response = requests.get(f"https://www.omdbapi.com/?t={choix}&apikey={OMDB_API_KEY}")
        data = response.json()
        if data["Response"] == "True":
            director = data.get("Director")
            duration = data.get("Runtime")
            actor = data.get("Actors")
            year = data.get("Year")
            return (f'Réalisateur : {director}, Durée : {duration}, Acteurs : {actor}, Année : {year}')
    
        else:
            return "Inconnu"
        
    if choix:
        poster_url = get_movie_poster(choix)
        infos = get_movie_details(choix)
    if poster_url:
        st.image(poster_url, caption=choix)
        st.write(infos)
    else:
        st.error(f"Affiche non disponible pour le film '{choix}'")
    nn = NearestNeighbors(n_neighbors=6, metric="manhattan")
    nn.fit(df.drop('movie_title', axis = 1).values)
    ligne = df[df.movie_title==choix].index[0]
    distances, index = nn.kneighbors([df.drop("movie_title", axis=1).iloc[ligne, :]])
    liste_des_recommandations = df.movie_title[index[0]]
    #st.write(liste_des_recommandations.values[1:])

    restit=liste_des_recommandations.values[1:].tolist()
    cols = st.columns(len(liste_des_recommandations.values[1:]))  # Get number of posters


    for i, e in enumerate(liste_des_recommandations.values[1:]):
        with cols[i]:
    # Add an empty space before the poster
            st.empty()
            poster_url = get_movie_poster(e)
            infos = get_movie_details(e)
            if poster_url:
                st.write(e)
                st.image(poster_url, width=200)
            if infos:
                st.write(infos)
            else:
                st.error(f"Affiche non disponible pour le film '{e}'")
    # Add another empty space after the poster
    st.empty()

with onglet3:

    lesDonneesDesComptes = {'usernames': {'utilisateur': {'name': 'utilisateur',
     'password': 'utilisateurMDP',
     'email': 'utilisateur@gmail.com',
     'failed_login_attemps': 0, # Sera géré automatiquement
     'logged_in': False, # Sera géré automatiquement
     'role': 'utilisateur'},
     'root': {'name': 'root',
     'password': 'rootMDP',
     'email': 'admin@gmail.com',
     'failed_login_attemps': 0, # Sera géré automatiquement
     'logged_in': False, # Sera géré automatiquement
     'role': 'administrateur'}}}

    authenticator = Authenticate(
    lesDonneesDesComptes, # Les données des comptes
    "cookie name", # Le nom du cookie, un str quelconque
    "cookie key", # La clé du cookie, un str quelconque
    30, # Le nombre de jours avant que le cookie expire 
    )
    authenticator.login()
    
    def accueil():

        # Charge les données depuis le fichier CSV
        movies_complet = pd.read_csv('movie_complet.csv')
        # Crée un titre pour ton tableau de bord Streamlit
        # Calcule la moyenne des scores IMDb par décennie
        average_imdb_score_per_decade = movies_complet.groupby('decade')['imdb_score'].mean()
        col1, col2 = st.columns(2)  # Créez 2 colonnes
        with col1:
        # Suppose you have a DataFrame called 'movies_complet' with columns 'decade' and 'imdb_score'

            average_imdb_score_per_decade = movies_complet.groupby('decade')['imdb_score'].mean().reset_index()

            fig = px.bar(average_imdb_score_per_decade, x='decade', y='imdb_score', color_discrete_sequence=['green'])
            fig.update_layout(
            xaxis_title='Décennie',
            yaxis_title='Score IMDb moyen',
            title='Score IMDb moyen par décennie',
            #xaxis=dict(tickangle=90),
            font=dict(color='white')
            )

            # To change the background color:
            fig.update_layout(
            plot_bgcolor='#232642'
            )

            # To change the font color:
            fig.update_layout(
            font=dict(color='white')
            )

            st.plotly_chart(fig)
        with col2:
            average_rating_per_couple = movies_complet.groupby('couple_director_actor_1')['imdb_score'].mean()
            #average_rating_per_couple
            # Tri décroissant
            average_rating_per_couple_sorted = average_rating_per_couple.sort_values(ascending=False)
            # Assuming your data is stored in pandas Dataframe named 'average_rating_per_couple_sorted'
            # Prepare data for Plotly
            couples = average_rating_per_couple_sorted.index[:10].tolist()
            ratings = average_rating_per_couple_sorted.values[:10].tolist()
            # Create the bar chart
            fig = go.Figure(
                data=[go.Bar(
                    x=ratings,
                    y=couples,
                    text=ratings,
                    textposition='auto',
                    marker_color='pink',
                    orientation='h'
                )]
            )
            # Update layout for interactivity and styling
            fig.update_layout(
                title='Couple Director - Actor (Top 10)',
                title_x=0.5,
                title_font_color="white",
                # title_font_weight="bold",  # Remove invalid property
                title_font_size=16,  # Increase title font size for emphasis
                #xaxis_title='Average Rating',
                xaxis_title_font_color="white",
                xaxis_title_font_size=15,
                #yaxis_title='Couple Director - Actor',
                yaxis_title_font_color="white",
                yaxis_title_font_size=4,
                xaxis_tickfont_color="white",
                xaxis_tickfont_size=4,
                yaxis_tickfont_color="white",
                yaxis_tickfont_size=15,
                xaxis_tickangle=45,
                xaxis_tickvals=ratings,
                plot_bgcolor='#232846',  # Set transparent white background
                xaxis_showgrid=False,
                yaxis_showgrid=False
            )
            #fig.show()
            st.plotly_chart(fig)

        col1, col2 = st.columns(2)  # Créez 2 colonnes
        with col1:
            df_select_genre = pd.read_csv('df_imdbscore_moyen_par_genre.csv')
            select_genre = st.selectbox("Sélectionnez une colonne pour le graphique en ligne :", df_select_genre['genre'])

            # Filtrage du dataframe pour ne garder que les films du genre sélectionné
            df_genre = df_select_genre[df_select_genre['genre'] == select_genre]

            fig = px.bar(df_genre, x='decade', y='imdb_score', color_discrete_sequence=['#BDB76B'])
            fig.update_layout(
                xaxis_title='Décennie',
                yaxis_title='Score IMDb moyen',
                title=f'Notation moyenne par décennie du genre : {select_genre}',
                font=dict(color='white')
            )

            # To change the background color:
            fig.update_layout(
                plot_bgcolor='#232846'
            )

            st.plotly_chart(fig)
        with col2:
        #Durée moyenne par genre
            df_genre = movies_complet['genres'].str.split('|', expand=True).stack().reset_index(level=0).set_index('level_0').rename(columns={0:'genre'})

            # Join the 'duration' column
            df_duree_moyenne_per_genre = df_genre.join(movies_complet['duration'])
            df_duree_moyenne_per_genre['duration'] = pd.to_numeric(df_duree_moyenne_per_genre['duration'], errors='coerce')

            # Calculate average duration per genre
            df_duree_moyenne_per_genre = df_duree_moyenne_per_genre.groupby('genre')['duration'].mean().reset_index().sort_values(by='duration', ascending=False)

            fig = px.bar(df_duree_moyenne_per_genre, x='duration', y='genre', color_discrete_sequence=['orange'])
            fig.update_layout(
                xaxis_title='Durée en minutes',
                yaxis_title='',
                title='Durée moyenne des films par genre',
                font=dict(color='white'),
                plot_bgcolor='#232846',
                height=550
            )

        
            st.plotly_chart(fig)





        top_5_by_decade = pd.read_csv('top_5_by_decade.csv')
        # Group by country and decade
        grouped_by_country_decade = movies_complet.groupby(['country', 'decade'])
        # Compter le nombre de films
        nb_films_by_country_per_decade = grouped_by_country_decade.size().unstack().fillna(0)
        # Mise en forme DataFrame (Reshape du dataframe avec la fonction .melt())
        nb_films_by_country_per_decade = nb_films_by_country_per_decade.reset_index().melt(
        id_vars=['country'],
        var_name='decade',
        value_name='nb_film'
        )
        
        # Filter les lignes dont le nb_film != 0 avant tri et selection du top 5
        top_5_by_decade = nb_films_by_country_per_decade[nb_films_by_country_per_decade['nb_film'] > 0]
        # Tri par decade et sélection du top 5
        top_5_by_decade = top_5_by_decade.sort_values(by=['decade', 'nb_film'], ascending=[False, False])
        # Regroupement par decade and select the top 5 countries
        top_5_by_decade = top_5_by_decade.groupby('decade').head(5)
        # Crée un titre pour ton tableau de bord Streamlit
        st.title('Top 5 des pays producteurs de films par décennies')
        # Affichage de la carte
        fig = px.scatter_geo(top_5_by_decade,
                     locations='country',
                     locationmode='country names',
                     color='country',
                     hover_data=['country', 'nb_film'],  # Utilisation de hover_data pour afficher plusieurs colonnes
                     size='nb_film',
                     animation_frame='decade',
                     projection='natural earth'
                     )

        # Modifier le fond de la carte et les contours
        fig.update_geos(
            bgcolor='#232846',
            showcoastlines=True, coastlinecolor='white',
            showland=True, landcolor='#232846',
            showocean=True, oceancolor='#232846',
            showlakes=True, lakecolor='#232846',
            showrivers=True, rivercolor='white'
        )

        st.plotly_chart(fig)

       
        

    if st.session_state["authentication_status"]:
        accueil()
  # Le bouton de déconnexion
        authenticator.logout("Déconnexion")
    elif st.session_state["authentication_status"] is False:
        st.error("L'username ou le password est/sont incorrect")
    elif st.session_state["authentication_status"] is None:
        st.warning('Les champs username et mot de passe doivent être remplis')


    with onglet4:
        st.write('Horaires et accès')
        st.image('plan.jpg', width = 400)



    











    
















    
