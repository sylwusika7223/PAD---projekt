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
            
        ]),
        dbc.Row([
            html.P('W tym dashbordzie znajduje się analiza mieszkań względem cen, metrażu, lokalizacji oraz liczby pokoi. Przeanalizowałyśmy mieszkania wystawione na sprzedaż na stronie otodom.pl. Dane obejmują Warszawę i jej okolicę, a pobranie danych nastąpiło 20 maja 2024 roku.')
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
        ], style={'margin-right': '20px'}),
        dbc.Row([
            dcc.Graph(
            id='district-barplot',
            figure=fig1)
        ])
    ]
)