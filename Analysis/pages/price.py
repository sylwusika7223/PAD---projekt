import dash
from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

dash.register_page(__name__, name='Cena')

data = pd.read_excel('cleaned_data.xlsx')

#zmienne
districts = data['District'].dropna().unique()
mean_price_per_m2 = data.groupby('District')['Price per m2'].mean().sort_values(ascending=False)

#histogram offer-price-histogram
fig1=px.histogram(data, x='Price', nbins=30, title='Rozkład cen mieszkań', color_discrete_sequence=['purple'])
fig1.update_layout(
    xaxis_title='Cena (PLN)',
    yaxis_title='Liczba ofert'
)
#boxplot
fig2=px.box(data, x='District', y='Price', title='Rozkład cen mieszkań w różnych dzielnicach', color='District')
fig2.update_layout(
    xaxis_title='Dzielnica',
    yaxis_title='Cena (PLN)',
)
#barplot mean-district-barplot
fig3=px.bar(mean_price_per_m2, x=mean_price_per_m2.index, y=mean_price_per_m2.values, title='Średnia cena za metr kwadratowy w poszczególnych dzielnicach', color=mean_price_per_m2)
fig3.update_traces(showlegend=False)
fig3.update_layout(
    xaxis_title='Dzielnica',
    yaxis_title='Średnia cena za metr kwadratowy (PLN)'
)


layout = html.Div(
    [
        dbc.Row([
            dbc.Col(
                html.P('Jako pierwsze chcemy zobaczyć jak wygląda stosunek cen mieszkań do liczby ofert. Z wykresu możemy wyczytać, że najwięcej ofert mieści się w przedziale od 500 tysięcy do 1 milionie złotych.')
            )
        ]),
        dbc.Row([
            dbc.Col(
                dcc.Graph(
                    id='offer-price-histogram',
                    figure=fig1
                ),
            )
        ]),
        dbc.Row([
            dbc.Col(
                html.P('Kolejny wykres przedstawia zależność między ceną, a metrażem mieszkania z podziałem na dzielnice Warszawy. Możemy na nim zaobserwować, że duża większość ofert ma podobną do siebie cenę, jednak jest kilka odchyleń. Najbardziej widocznym jest mieszkanie na Ursynowie, które kosztuje ponad 15 milionów złotych za 842 metry kwadratowe.')
            )
        ]),
        dbc.Row([
            dbc.Col(
                html.P('Ze względu na ogromną liczbę mieszkań, wykres można dostosować zmieniając na suwaku zakres cenowy jaki chcemy podejrzeć.')
            )
        ]),
        dbc.Row([
            dbc.Col(          
                dcc.Graph(id='area-price-scatter'),
            )
        ]),
        dbc.Row([
            dbc.Col(
                dcc.RangeSlider(
                id='price-area-slider',
                min=data['Price'].min(),
                max=data['Price'].max(),
                value=[data['Price'].min(), data['Price'].max()],
                marks={str(price): str(price) for price in range(int(data['Price'].min()), int(data['Price'].max()), 1000000)}
                ),
            )
        ]),
        dbc.Row([
            dbc.Col(
                html.P('Następnym wykresem jest wykres pudełkowy, na którym możemy przeanalizować rozkład cen za mieszkanie w różnych dzielnicach. Do wykresu jest dołączona lista, dzięki której możemy filtrować wyniki. Wybierając jedną lub więcej dzielnic możemy lepiej przyjrzeć się rozkładowi.')
            )
        ]),
        dbc.Row([
            dbc.Col(
                dcc.Dropdown(
                    id='location-dropdown',
                    options=[{'label': district, 'value': district} for district in districts],
                    value=[],
                    multi=True,
                    clearable=False
                )
            )
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(id='boxplot'))
        ]),
        dbc.Row([
            dbc.Col(
                html.P('Ostatnim wykresem na tej podstronie jest wykres przedstawiający średnią cenę za metr kwadratowy w dzielnicach.')
            )
        ]),
        dbc.Row([
            dbc.Col(  
                dcc.Graph(
                    id='mean-district-barplot',
                    figure=fig3
                )
            )
        ])
    ]
)

@callback(
    Output('area-price-scatter', 'figure'),
    [Input('price-area-slider', 'value')]
)
def update_area_price_scatter(price_range):
    filtered_data = data[(data['Price'] >= price_range[0]) & (data['Price'] <= price_range[1])]
    fig1=px.scatter(filtered_data, x='m2', y='Price', title='Zależność między ceną a metrażem mieszkania', color='District')
    fig1.update_layout(
        xaxis_title='Metraż (m2)',
        yaxis_title='Cena (PLN)')
    return fig1

@callback(
    Output('boxplot', 'figure'),
    [Input('location-dropdown', 'value')]
)
def update_boxplot(selected_location):
    if not selected_location:
        filtered_data = data
    else:
        filtered_data = data[data['District'].isin(selected_location)]
    fig2=px.box(filtered_data, x='District', y='Price', title='Rozkład cen mieszkań w różnych dzielnicach', color='District')
    fig2.update_xaxes(title='Dzielnica')
    fig2.update_yaxes(title='Cena (PLN)')
    return fig2