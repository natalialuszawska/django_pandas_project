# -*- coding: utf-8 -*-
"""Aktualny Pandas projekt rozrywka (1).ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/18fXGXlrEA3qzKY76cP40MF97TpP5BHXu
"""

# import modułów i ustawienia
import pandas as pd
import matplotlib.pyplot as plt
pd.set_option('display.max_columns', None)

# from google.colab import drive
# drive.mount('/content/drive')

# Wczytanie danych spotify recent
spotify = pd.read_csv(r"spotify-2023.csv", sep = ',', encoding = 'latin-1')
spotify.head()

"""SPOTIFY"""

spotify.dtypes

#cleaning
spotify = spotify[spotify.streams.isin(['BPM110KeyAModeMajorDanceability53Valence75Energy69Acousticness7Instrumentalness0Liveness17Speechiness3']) == False]
spotify['in_shazam_charts'] = spotify['in_shazam_charts'].str.replace(',','')
spotify['in_deezer_playlists'] = spotify['in_deezer_playlists'].str.replace(',','')

# using dictionary to convert specific columns
convert_dict = {'streams': float
                ,'in_shazam_charts': float
                ,'in_deezer_playlists': float
                }

spotify = spotify.astype(convert_dict)

#top songs with indicators; zrobić porównania na początku porzednich dekad jak sie zmieniały wskaźniki w latach 90 itd
def top_songs_by_decades(year):
  # top 10 songs in 2023
  spotify_top_10_songs_year = spotify.groupby(["released_year","track_name", "artist(s)_name"],
                                              as_index=False)["streams"].sum()

  spotify_top_10_songs_year = spotify_top_10_songs_year[spotify_top_10_songs_year['released_year'] == year]

  spotify_top_10_songs_year = spotify_top_10_songs_year.sort_values(by=['streams'],ascending=False)

  spotify_top_10_songs_year = spotify_top_10_songs_year.iloc[:10]
  spotify_top_10_songs_year

  # indicators in for most listened songs 2023
  top_10_year_indicators = pd.merge(spotify_top_10_songs_year, spotify, on=['track_name','released_year'], how='left')

  # Ustawienie kolumny 'Song' jako indeksu
  top_10_year_indicators = top_10_year_indicators.loc[:,["track_name", "artist(s)_name_x","danceability_%", "valence_%", "energy_%", "acousticness_%", "instrumentalness_%","liveness_%","speechiness_%"]]#.set_index('track_name', inplace=True)
  top_10_year_indicators.set_index('track_name', inplace=True)
  return top_10_year_indicators

years = [2023,2022,2021]
for i in years:
  globals()[f'spotify_top_10_songs_{i}'] = top_songs_by_decades(year=i)

#Tworzenie wykresów dla każdego wskaźnika
for i in years:
    df = globals()[f'spotify_top_10_songs_{i}']
    df.plot(kind='bar', figsize=(10, 6))
    plt.title(f'Wskaźniki dla poszczególnych piosenek roku {i}')
    plt.xlabel('Piosenka')
    plt.ylabel('Wartość (%)')
    plt.grid(axis='y')  # Dodanie siatki tylko wzdłuż osi Y
    plt.legend(title='Wskaźniki', bbox_to_anchor=(1.05, 1), loc='upper left')  # Legenda poza obszarem wykresu
    plt.tight_layout()  # Dostosowanie układu, aby uniknąć przecinania się etykiet
    plt.show()

# in playlists
def top_songs_in_playlist(year):
  spotify_playlists = spotify
  spotify_playlists['in_playlists'] = spotify_playlists['in_spotify_playlists'] + spotify_playlists['in_apple_playlists'] + spotify_playlists['in_deezer_playlists']

  spotify_playlists = spotify_playlists.loc[:,["released_year","track_name", "artist(s)_name", "in_playlists"]]

  spotify_playlists = spotify_playlists.groupby(["released_year","track_name", "artist(s)_name"],
                                                as_index=False)["in_playlists"].sum()

  spotify_playlists = spotify_playlists[spotify_playlists['released_year'] == year].sort_values(by=['in_playlists'],
                                                                                                ascending=False)
  spotify_playlists = spotify_playlists.iloc[:10]

  # indicators in for most added songs 2023
  top_10_year_indicators_playlists = pd.merge(spotify_playlists, spotify, on=['track_name','released_year'], how='left')

  # Ustawienie kolumny 'Song' jako indeksu
  top_10_year_indicators_playlists = top_10_year_indicators_playlists.loc[:,["track_name", "artist(s)_name_x","danceability_%", "valence_%", "energy_%", "acousticness_%", "instrumentalness_%","liveness_%","speechiness_%"]]
  top_10_year_indicators_playlists.set_index('track_name', inplace=True)
  return top_10_year_indicators_playlists

years = [2023,2022,2021]
for i in years:
  globals()[f'spotify_top_in_playlists_{i}'] = top_songs_in_playlist(year=i)

#Tworzenie wykresów dla każdego wskaźnika
for i in years:
    df = globals()[f'spotify_top_in_playlists_{i}']
    df.plot(kind='bar', figsize=(10, 6))
    plt.title(f'Wskaźniki dla poszczególnych piosenek roku {i}')
    plt.xlabel('Piosenka')
    plt.ylabel('Wartość (%)')
    plt.grid(axis='y')  # Dodanie siatki tylko wzdłuż osi Y
    plt.legend(title='Wskaźniki', bbox_to_anchor=(1.05, 1), loc='upper left')  # Legenda poza obszarem wykresu
    plt.tight_layout()  # Dostosowanie układu, aby uniknąć przecinania się etykiet
    plt.show()

# Wczytanie danych spotify 20's
spotify20s = pd.read_csv("BestSpotify2000_2023.csv", sep = ';', encoding = 'utf-8')
spotify20s.head()

spotify20s.columns

spotify20s.rename(columns={"danceability ": "danceability","speechiness ": "speechiness"}, inplace = True)

spotify20sAgg = spotify20s.groupby('year', as_index=False).agg({
    'bpm': [('avg', 'mean'), ('median', 'median')],
    'energy': [('avg', 'mean'), ('median', 'median')],
    'danceability': [('avg', 'mean'), ('median', 'median')],
    'dB': [('avg', 'mean'), ('median', 'median')],
    'liveness': [('avg', 'mean'), ('median', 'median')],
    'valence': [('avg', 'mean'), ('median', 'median')],
    'duration': [('avg', 'mean'), ('median', 'median')],
    'acousticness': [('avg', 'mean'), ('median', 'median')],
    'speechiness': [('avg', 'mean'), ('median', 'median')],
})
spotify20sAgg.columns = ['_'.join(col).rstrip('_') for col in spotify20sAgg.columns.values]

spotify20sAgg.head()

years_of_interest = [2023,2017,2012,2007]
filtered_data = spotify20sAgg[spotify20sAgg['year'].isin(years_of_interest)]

# Tworzenie wykresu słupkowego
plt.figure(figsize=(10, 6))

# Możemy wybrać kilka kluczowych kolumn do wizualizacji
columns_of_interest = ['bpm_avg', 'bpm_median', 'energy_avg', 'energy_median', 'danceability_avg', 'danceability_median']
colors = ['blue', 'green', 'red', 'purple', 'orange', 'gray']  # Kolory dla różnych kolumn
width = 0.15  # Szerokość słupków

# Rysowanie słupków dla każdej kolumny
for i, column in enumerate(columns_of_interest):
    plt.bar(filtered_data['year'] + i * width, filtered_data[column], width=width, label=column, color=colors[i])

plt.title('Średnia i Mediana różnych cech muzycznych dla wybranych lat')
plt.xlabel('Rok')
plt.ylabel('Wartości')
plt.legend()
plt.grid(True)
plt.xticks(filtered_data['year'] + width, filtered_data['year'])  # Ustawienie oznaczeń osi x na lata z danych
plt.show()

# Grupowanie danych po roku i gatunku, zliczanie wystąpień
genre_counts = spotify20s.groupby(['year', 'top genre']).size()

# Resetowanie indeksu do zwykłego DataFrame
genre_counts = genre_counts.reset_index(name='count')

# Sortowanie danych po roku i liczbie wystąpień (malejąco)
genre_counts = genre_counts.sort_values(['year', 'count'], ascending=[True, False])

# Wybieranie najczęściej występującego gatunku dla każdego roku
most_common_genre_per_year = genre_counts.drop_duplicates('year')

print(most_common_genre_per_year)