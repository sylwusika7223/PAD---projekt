import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

dash.register_page(__name__, name='Sprzedawca')

data = pd.read_excel('cleaned_data.xlsx')

#zmienne
seller_counts = data['Seller type'].value_counts()
mean_price_seller = data.groupby('Seller type')['Price'].mean()

#barplot seller-offer-barplot
fig1=px.bar(seller_counts, x=seller_counts.index, y=seller_counts.values, title='Podział ofert według rodzaju sprzedawcy', color_discrete_sequence=['powderblue'])
fig1.update_layout(
    xaxis_title='Rodzaj sprzedawcy',
    yaxis_title='Liczba ofert'
)
#barplot seller-mean-barplot
fig2=px.bar(mean_price_seller, x=mean_price_seller.index, y=mean_price_seller.values, title='Średnia cena mieszkań w zależności od rodzaju sprzedawcy', color_discrete_sequence=['palevioletred'])
fig2.update_layout(
    xaxis_title='Rodzaj sprzedawcy',
    yaxis_title='Średnia cena (PLN)'
)


layout = html.Div(
    [
        dbc.Row([
            html.H1('Analiza dotycząca sprzedawców')
        ], style={'textAlign': 'center'}),
        dbc.Row([
            html.P('Przedstawiamy tutaj wykresy, na których znaleźli się sprzedawcy.')
        ]),
        html.Hr(),
        dbc.Row([
            html.P('Sprzedawców możemy podzielić na dwie kategorie - biuro nieruchomości oraz osoba prywatna. Wykresy przedstawione poniżej porównują ze sobą obie te kategorie względem liczby ofert na pierwszym wykresie oraz średniej ceny mieszkania na drugim.')
        ]),
        dbc.Row([
            dcc.Graph(
                id='seller-offer-barplot',
                figure=fig1
            )
        ]),
        dbc.Row([
            dcc.Graph(
                id='seller-mean-barplot',
                figure=fig2
            )
        ])
    ], style={'margin-right': '20px'}
)