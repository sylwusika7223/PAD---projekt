import dash
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

data = pd.read_excel('cleaned_data.xlsx')

dash.register_page(__name__, path='/', name='Strona główna')

#zmienne
offers_per_district = data['District'].value_counts()

#barplot district-barplot
fig1=px.bar(offers_per_district, x=offers_per_district.index, y=offers_per_district.values, title='Liczba ofert w poszczególnych dzielnicach', color_discrete_sequence=['steelblue'])
fig1.update_layout(
    xaxis_title='Dzielnica',
    yaxis_title='Liczba ofert'
)

layout = html.Div(
    [
        dbc.Row([
            html.H1('Analiza danych na temat mieszkań z rynku wtórnego na sprzedaż w Warszawie z dnia 20 maja 2024.')
        ], style={'textAlign': 'center'}),
        dbc.Row([
            html.P('W tym dashbordzie znajduje się analiza mieszkań pod względem cen, metrażu, lokalizacji oraz liczby pokoi. Przeanalizowałyśmy mieszkania wystawione na sprzedaż na stronie otodom.pl. Dane obejmują Warszawę i jej okolice i zostały pobrane 20 maja 2024 roku.')
        ]),
        dbc.Row([
            html.P('Dzięki analizie wystawionych na sprzedaż mieszkań, uzyskałyśmy ponad 7 tysięcy rekorów. Poniższa tabelka przedstawia domyślnie 20 z nich.')
        ]),
        dbc.Row([
            dash_table.DataTable(
                style_data={
                    'whiteSpace': 'normal',
                    'height': 'auto',
                },
                data=data.head(20).to_dict('records'),
                style_header={'backgroundColor': 'rgb(128, 159, 184)', 'color': 'black'},
                columns=[{'name': i, 'id': i} for i in data.columns],
                style_cell={'textAlign': 'left'}
            )
        ]),
        html.Hr(),
        dbc.Row([
            html.P('Poniżej znajduje się wykres przedstawiający podział ofert na poszczególne dzielnice. Możemy zauważyć, że pomiędzy Mokotowem, a powiatem pruszkowskim jest bardzo duża różnica. W dzielnicy Mokotów zostało wystawionych na sprzedaż ponad 1200 mieszkań, podczas gdy w powiecie widnieją tylko 3 oferty.')
        ], style={'marginTop': 25}),
        dbc.Row([
            dcc.Graph(
            id='district-barplot',
            figure=fig1)
        ]),
        html.Hr(),
        dbc.Row([
            html.P('Na podstawie zebranych danych i przedstawionych wykresów możemy zauważyć, że zdecydowana większość ofert jest wystawiana przez biura nieruchomości ale nie oznacza to, że ceny są dużo wyższe. Średnia cena za mieszkanie od osoby prywatnej wynosi 1 milion i 100 tysięcy, a od biura nieruchomości 1 milion i 200 tysięcy złotych. Daje nam to różnicę wynoszącą około 100 tysięcy złotych. Zwykle im bliżej centrum tym wystawiane mieszkania są droższe, z małymi wyjątkami, którymi są dzielnice Mokotów oraz Wilanów. One również plasują się na czołowych miejscach pod względem ceny. Najczęściej za mieszkanie zapłacimy w przedziale od 500 tysięcy do 1 miliona złotych. Zdecydowana większość ofert dotyczy mieszkań 2 lub 3 pokojowych.')
        ], style={'marginTop': 25}),
    ], style={'margin-right': '20px'}
)