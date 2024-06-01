import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import mpld3
from django.shortcuts import render
from django.http import HttpResponse
pd.set_option('display.max_columns', None)
pd.set_option('display.max_columns', None)


def load_data():
    spotify = pd.read_csv("/Users/natalialuszawska/Desktop/STUDIA/SEM_3/proj_django/django_with_pandas/charts/spotify-2023.csv", sep=',', encoding='latin-1')
    spotify.head()
    spotify.dtypes

    spotify = spotify[spotify.streams.isin(['BPM110KeyAModeMajorDanceability53Valence75Energy69Acousticness7Instrumentalness0Liveness17Speechiness3']) == False]
    spotify['in_shazam_charts'] = spotify['in_shazam_charts'].str.replace(',','')
    spotify['in_deezer_playlists'] = spotify['in_deezer_playlists'].str.replace(',','')

    convert_dict = {'streams': float
                    ,'in_shazam_charts': float
                    ,'in_deezer_playlists': float
                    }

    spotify = spotify.astype(convert_dict)

    return spotify

def top_songs_by_decades(spotify, year):
  spotify_top_10_songs_year = spotify.groupby(["released_year","track_name", "artist(s)_name"],
                                              as_index=False)["streams"].sum()

  spotify_top_10_songs_year = spotify_top_10_songs_year[spotify_top_10_songs_year['released_year'] == year]

  print('dupa')
  spotify_top_10_songs_year = spotify_top_10_songs_year.sort_values(by=['streams'],ascending=False)
  spotify_top_10_songs_year = spotify_top_10_songs_year.iloc[:10]
  spotify_top_10_songs_year

  top_10_year_indicators = pd.merge(spotify_top_10_songs_year, spotify, on=['track_name','released_year'], how='left')

  top_10_year_indicators = top_10_year_indicators.loc[:,["track_name", "artist(s)_name_x","danceability_%", "valence_%", "energy_%", "acousticness_%", "instrumentalness_%","liveness_%","speechiness_%"]]#.set_index('track_name', inplace=True)
  top_10_year_indicators.set_index('track_name',  inplace=True)
  return top_10_year_indicators

def top_songs_in_playlist(spotify, year):
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

# def create_chart(top_10_year_indicators, year):

#     fig, ax = plt.subplots(figsize=(10, 6))

#     # Rysowanie wykresu słupkowego
#     top_10_year_indicators.plot(kind='bar', x='track_name', ax=ax)
#     # Ustawienie tytułów i etykiet
#     ax.set_title(f'Wskaźniki dla poszczególnych piosenek roku {year}')
#     ax.set_xlabel('Piosenka')
#     ax.set_ylabel('Wartość (%)')
#     ax.grid(axis='y')
#     ax.legend(title='Wskaźniki', bbox_to_anchor=(1.05, 1), loc='upper left')
    
#     # Ustawienie etykiet osi X na nazwy piosenek
#     ax.set_xticks(range(len(top_10_year_indicators)))
#     print('...................................')
#     print('top_10_year_indicators', top_10_year_indicators['track_name'].values)
#     ax.set_xticklabels(top_10_year_indicators['track_name'].values, rotation=45, ha='right')
    
#     fig.tight_layout()
    
#     return mpld3.fig_to_html(fig)

# def create_chart(top_10_year_indicators, year):
#     from matplotlib.legend import Legend
#     fig, ax = plt.subplots(figsize=(10, 6))

#     # Rysowanie wykresu słupkowego
#     top_10_year_indicators.plot(kind='bar', ax=ax)

#     # Ustawienie tytułów i etykiet
#     ax.set_title(f'Wskaźniki dla poszczególnych piosenek roku {year}')
#     ax.set_xlabel('Piosenka')
#     ax.set_ylabel('Wartość (%)')
#     ax.grid(axis='y')

#     # Ustawienie etykiet osi X na nazwy piosenek
#     ax.set_xticks(range(len(top_10_year_indicators)))
#     ax.set_xticklabels(top_10_year_indicators.index, rotation=45, ha='right')

#     # Dodanie pierwszej legendy dla wskaźników
#     handles, labels = ax.get_legend_handles_labels()
#     first_legend = ax.legend(handles, labels, title='Wskaźniki', bbox_to_anchor=(1.05, 1), loc='upper left')

#     # Dodanie pierwszej legendy do osi
#     ax.add_artist(first_legend)

#     # Dodanie drugiej legendy dla nazw piosenek
#     labels = [f"{index}: {artist}" for index, artist in zip(top_10_year_indicators.index, top_10_year_indicators['artist(s)_name_x'])]
#     handles = [plt.Line2D([0], [0], color='w', label=label) for label in labels]
#     second_legend = Legend(ax, handles=handles, labels=labels,title='Piosenki', bbox_to_anchor=(1.05, -0.2), loc='upper left', frameon=False)
#     ax.add_artist(second_legend)

#     fig.tight_layout()

#     return mpld3.fig_to_html(fig)
def create_chart(top_10_year_indicators, year):
    fig, ax = plt.subplots(figsize=(14, 8))

    # Przygotowanie danych
    indicators = ['danceability_%', 'valence_%', 'energy_%', 'acousticness_%', 'instrumentalness_%', 'liveness_%', 'speechiness_%']
    track_names = top_10_year_indicators.index.tolist()
    
    # Rysowanie wykresu słupkowego dla każdego wskaźnika
    width = 0.1  # Szerokość słupków
    x = range(len(track_names))
    
    for i, indicator in enumerate(indicators):
        values = top_10_year_indicators[indicator]
        ax.bar([p + width * i for p in x], values, width=width, label=indicator)
    
    # Ustawienie tytułów i etykiet
    ax.set_title(f'Wskaźniki dla poszczególnych piosenek roku {year}')
    ax.set_xlabel('Piosenka')
    ax.set_ylabel('Wartość (%)')
    ax.set_xticks([p + width * (len(indicators) / 2) for p in x])
    ax.set_xticklabels(track_names, rotation=45, ha='right')
    ax.legend(title='Wskaźniki', bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.grid(axis='y')

    fig.tight_layout()
    
    return mpld3.fig_to_html(fig)

def create_chart_for_mean_and_meadian(request):
    spotify20s = pd.read_csv("/Users/natalialuszawska/Desktop/STUDIA/SEM_3/proj_django/django_with_pandas/charts/BestSpotify2000_2023.csv", sep = ';', encoding = 'utf-8')
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
    fig, ax = plt.subplots(figsize=(10, 6))

    # Możemy wybrać kilka kluczowych kolumn do wizualizacji
    columns_of_interest = ['bpm_avg', 'bpm_median', 'energy_avg', 'energy_median', 'danceability_avg', 'danceability_median']
    colors = ['blue', 'green', 'red', 'purple', 'orange', 'gray']  # Kolory dla różnych kolumn
    width = 0.15  # Szerokość słupków

    # Rysowanie słupków dla każdej kolumny
    for i, column in enumerate(columns_of_interest):
        ax.bar(filtered_data['year'] + i * width, filtered_data[column], width=width, label=column, color=colors[i])

    ax.set_title('Średnia i Mediana różnych cech muzycznych dla wybranych lat')
    ax.set_xlabel('Rok')
    ax.set_ylabel('Wartości')
    ax.legend()
    ax.grid(True)
    ax.set_xticks(filtered_data['year'] + width)  # Ustawienie oznaczeń osi x na lata z danych
    ax.set_xticklabels(filtered_data['year'])

    # Convert plot to HTML
    plot_html = mpld3.fig_to_html(fig)

    context = {
        'plot_html': plot_html
    }

    # return render(request, 'charts/index.html', context)
    return HttpResponse(plot_html)
    # return render(request, 'charts/mean_median_chart.html')

def generate_table_html(top_10_year_indicators):
    table_html = "<table>"
    table_html += "<thead><tr><th>Track Name</th><th>Artist</th></thead>"
    table_html += "<tbody>"
    for index, row in top_10_year_indicators.iterrows():
        table_html += f"<tr><td>{index}</td><td>{row['artist(s)_name_x']}</td></tr>"
    table_html += "</tbody></table>"
    return table_html

def chart_view(request, year, chart_type):
    spotify = load_data()
    print('--------------')
    print('chart_type',chart_type)
    if chart_type == 'top10':
        top_10_year_indicators = top_songs_by_decades(spotify, year)
        chart_html = create_chart(top_10_year_indicators, year)
        table_html = generate_table_html(top_10_year_indicators)
        full_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Wykres i Tabela</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #33333C;
                    color: #fff;
                    line-height: 1.6;
                    hight: 100%;
                }}
                .content {{
                    margin: 0 auto;
                    background: #91979A;
                    box-shadow: 0 0 10px rgba(0,0,0,0.1);
                    color: #333;
                }}
                .chart-table-container {{
                    display: flex;
                    flex-direction: column;
                }}
                .chart-container, .table-container {{
                    background: #fff;
                    color: #333;
                    width: 100%;
                }}
                table {{
                    width: 50%;
                    height: 50%;
                }}
                table, th, td {{
                    border: 1px solid #ddd;
                }}
                th, td {{
                    padding: 8px;
                    text-align: left;
                }}
                th {{
                    background-color: #f2f2f2;
                }}
            </style>
        </head>
        <body>
            <div class="content">
                <div class="chart-table-container">
                    <div class="chart-container">
                        {chart_html}
                    </div>
                    <div class="table-container">
                        {table_html}
                    </div>
                </div>
            </div>
        </body>
        </html>
        """

        return HttpResponse(full_html)
        # return HttpResponse(chart_html)
        #return render(request, 'charts/chart.html', {'year': year, 'chart_type': chart_type})
        # return render(request, 'charts/chart.html', {'chart_html': chart_html})
    elif chart_type == 'playlists':
        print('playlists') 
        top_10_year_indicators = top_songs_in_playlist(spotify, year)
        chart_html = create_chart(top_10_year_indicators, year)
        table_html = generate_table_html(top_10_year_indicators)
        #return render(request, 'charts/chart.html', {'year': year, 'chart_type': chart_type})
        # return HttpResponse(chart_html)
        full_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Wykres i Tabela</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #33333C;
                    color: #fff;
                    line-height: 1.6;
                    hight: 100%;
                }}
                .content {{
                    margin: 0 auto;
                    background: #91979A;
                    box-shadow: 0 0 10px rgba(0,0,0,0.1);
                    color: #333;
                }}
                .chart-table-container {{
                    display: flex;
                    flex-direction: column;
                }}
                .chart-container, .table-container {{
                    background: #fff;
                    color: #333;
                    width: 100%;
                }}
                table {{
                    width: 50%;
                    height: 50%;
                }}
                table, th, td {{
                    border: 1px solid #ddd;
                }}
                th, td {{
                    padding: 8px;
                    text-align: left;
                }}
                th {{
                    background-color: #f2f2f2;
                }}
            </style>
        </head>
        <body>
            <div class="content">
                <div class="chart-table-container">
                    <div class="chart-container">
                        {chart_html}
                    </div>
                    <div class="table-container">
                        {table_html}
                    </div>
                </div>
            </div>
        </body>
        </html>
        """

        return HttpResponse(full_html)


def index(request):
    return render(request, './charts/index.html')
