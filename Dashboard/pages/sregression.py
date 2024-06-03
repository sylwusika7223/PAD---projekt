import dash
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

dash.register_page(__name__, name='Model regresyjny')

data = pd.read_excel('predicted_results.xlsx')

layout = html.Div(
    [
        dbc.Row([
            html.H1('Model regresyjny')
        ], style={'textAlign': 'center'}),
        dbc.Row([
            html.P('Podjęłyśmy decyzję, że w naszym projekcie bardziej pasuje model regresji liniowej. Jego zadaniem jest predykcja cen nieruchomości dla danych wybranych jako dane testowe.')
        ]),
        dbc.Row([
            html.P('Poniższa tabelka przedstawia 20 przykładowych danych, które przewidział model.')
        ]),
        dbc.Row([
            dbc.Col(
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
            ),
            dbc.Col(
                dbc.Row([
                    html.P('Błąd średniokwadratowy wynosi: 745933.1019086603'),
                    html.P('Współczynnik determinacji wynosi: 0.666837996471543')
                ])
            )
        ]),
        html.Hr(),
        dbc.Row([
            html.P('Z obserwacji wynika, że model poradził sobie dobrze.')
        ])
    ], style={'margin-right': '20px'}
)