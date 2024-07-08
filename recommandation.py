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

st.set_page_config(
    page_title="Wildflix",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.image('imagewild.png', width = 100)
titres_onglets = ['Bienvenue', 'Recommandation', 'Dashboard']
onglet1, onglet2, onglet3 = st.tabs(titres_onglets)

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
            # Crée un graphique à barres avec Seaborn et ajuste la taille
            plt.figure(figsize=(4, 2))  # Réduit la taille de moitié
            sns.barplot(x=average_imdb_score_per_decade.index, y=average_imdb_score_per_decade.values, color='grey')
        # Ajoute des étiquettes et des titres
            plt.xlabel('Décennie', color='black',fontsize=4)
            plt.ylabel('Score IMDb moyen', color='black',fontsize=4)
            plt.title('Notation moyenne par décennie', color='black',fontsize=6,fontweight='bold')
            plt.xticks(fontsize=4)
            plt.yticks(fontsize=4)
        # Supprimer le contour par défaut
            plt.gca().spines['top'].set_visible(False)
            plt.gca().spines['right'].set_visible(False)
            plt.gca().spines['bottom'].set_visible(False)
            plt.gca().spines['left'].set_visible(False)
            plt.gca().set_facecolor('#FAFAD2')
        # Affiche le graphique sur Streamlit
            st.set_option('deprecation.showPyplotGlobalUse', False)
            st.pyplot()
        with col2:
            average_rating_per_couple = movies_complet.groupby('couple_director_actor_1')['imdb_score'].mean()
        #average_rating_per_couple
        # Tri décroissant
            average_rating_per_couple_sorted = average_rating_per_couple.sort_values(ascending=False)
        # Création du graphique pour afficher le couple Top 10
            plt.figure(figsize=(4, 2))
            plt.barh(average_rating_per_couple_sorted.index[:10], average_rating_per_couple_sorted.values[:10], color = 'pink')  # Affichage du top 10 couplle
            plt.xlabel('Average Rating', color = "purple",fontsize=4)
            plt.ylabel('Couple Director - Actor',color = "purple",fontsize=4)
            plt.title('Couple Director - Actor (Top 10)', color = "purple", fontsize=6,fontweight='bold')
            plt.gca().spines['top'].set_visible(False)
            plt.gca().spines['right'].set_visible(False)
            plt.gca().spines['bottom'].set_visible(True)
            plt.gca().spines['bottom'].set_color('purple')
            plt.gca().spines['bottom'].set_linewidth(0.2)
            plt.gca().spines['left'].set_visible(True)
            plt.gca().spines['left'].set_color('purple')
            plt.gca().spines['left'].set_linewidth(0.2)
            plt.gca().set_facecolor('#FAFAD2')
            plt.yticks(fontsize=4, color = "purple")
            plt.xticks(fontsize=4, color = "purple")
            plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability
            plt.tight_layout()
            plt.show()
            st.pyplot()
        col1, col2 = st.columns(2)  # Créez 2 colonnes
        with col1:
            df_select_genre = pd.read_csv('df_imdbscore_moyen_par_genre.csv')
        # Sélection du genre à partir d'un input
            select_genre = st.selectbox("Select a column for the line chart:", df_select_genre['genre'])
        # Filtrage du dataframe pour ne garder que les films du genre sélectionné
            df_genre = df_select_genre[df_select_genre['genre'] == select_genre]
        #Create the barplot using Seaborn
            plt.figure(figsize=(5, 3))
            sns.barplot(x=df_genre['decade'], y=df_genre['imdb_score'], color = '#BDB76B')
            plt.xlabel('decade',fontsize=4)
            plt.ylabel('imdb_score',fontsize=4)
            plt.title(f'Notation moyenne par decennie du genre : {select_genre} ',fontsize=6,fontweight='bold')
            plt.xticks(fontsize=4)
            plt.yticks(fontsize=4)
            plt.gca().spines['top'].set_visible(False)
            plt.gca().spines['right'].set_visible(False)
            plt.gca().spines['bottom'].set_visible(False)
            plt.gca().spines['left'].set_visible(False)
            plt.gca().set_facecolor('#FAFAD2')
            plt.tight_layout()
            plt.show()
            st.pyplot()
        with col2:
    #Durée moyenne par genre
            df_genre = movies_complet['genres'].str.split('|', expand=True).stack().reset_index(level=0).set_index('level_0').rename(columns={0:'genre'}) #Extract genres into a single column DataFrame
            df_duree_moyenne_per_genre = df_genre.join(movies_complet['duration'])
            df_duree_moyenne_per_genre['duration'] = pd.to_numeric(df_duree_moyenne_per_genre['duration'], errors='coerce')
            df_duree_moyenne_per_genre = df_duree_moyenne_per_genre.groupby('genre')['duration'].mean().reset_index().sort_values(by='duration', ascending=False) # Reset index to convert to DataFrame
            g=sns.catplot(x="duration", y='genre', data=df_duree_moyenne_per_genre, kind='bar',color='orange',height=2)#, order=nb_votes_par_genre.index) # Use the DataFrame here
            g.ax.set_xticklabels(g.ax.get_xticklabels(), fontsize=2)  # Rotate x-axis labels and reduce font size
            g.ax.set_yticklabels(g.ax.get_yticklabels(), fontsize=2)
            g.set_axis_labels("Durée en minutes", "",fontsize=2)
            plt.title("Durée moyenne des films par genre", color='black',fontsize=4,fontweight='bold')
            plt.gca().set_facecolor('#FAFAD2')
            plt.tight_layout()  # Adjust layout to prevent labels from overlapping
            plt.show()
            st.pyplot()

            #Affichage du top 5 des pays producteurs de films pour chaque decade
        # Ouverture du dataframe enregistrer au format csv
    
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
                hover_data=['country', 'nb_film'], # Use hover_data to display multiple columns
                size='nb_film',
                animation_frame='decade',
                projection='natural earth'
                )
        st.plotly_chart(fig)
        
        sns.regplot(x = 'gross', y= 'imdb_score', data = movies_complet)
        plt.xlabel('Budget',fontsize=4)
        plt.ylabel('Score IMDb',fontsize=4)
        plt.title('Budget et notation', color='black',fontsize=6,fontweight='bold')
        plt.xticks(fontsize=4)
        plt.yticks(fontsize=4)
        plt.gca().spines['top'].set_visible(False)
        plt.gca().spines['right'].set_visible(False)
        plt.gca().spines['bottom'].set_visible(True)
        plt.gca().spines['left'].set_visible(True)
        plt.gca().set_facecolor('#FAFAD2')
        plt.gca().spines['left'].set_color('blue')
        plt.gca().spines['left'].set_linewidth(0.2)
        plt.gca().spines['bottom'].set_color('blue')
        plt.gca().spines['bottom'].set_linewidth(0.2)
        st.pyplot()

    if st.session_state["authentication_status"]:
        accueil()
  # Le bouton de déconnexion
        authenticator.logout("Déconnexion")
    elif st.session_state["authentication_status"] is False:
        st.error("L'username ou le password est/sont incorrect")
    elif st.session_state["authentication_status"] is None:
        st.warning('Les champs username et mot de passe doivent être remplis')















    
