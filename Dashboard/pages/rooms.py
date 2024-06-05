import dash
from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

dash.register_page(__name__, name='Liczba pokoi')

data = pd.read_excel('cleaned_data.xlsx')

#zmienne
mean_price_rooms = data.groupby('Rooms')['Price'].mean()
districts = data['District'].dropna().unique()
average_area_by_district = data.groupby('District')['m2'].mean().sort_values()

#barplot area-district-barplot
fig = px.bar(average_area_by_district, x=average_area_by_district.values, y=average_area_by_district.index, orientation='h', title='Średni metraż mieszkania w zależności od dzielnicy', color=average_area_by_district)
fig.update_layout(
    xaxis_title='Średni metraż mieszkania (m2)', 
    yaxis_title='Dzielnica'
)
#barplot mean-rooms-barplot
fig1=px.bar(mean_price_rooms, x=mean_price_rooms.index, y=mean_price_rooms.values, title='Średnia cena mieszkań w zależności od liczby pokoi', color_discrete_sequence=['thistle'])
fig1.update_layout(
    xaxis_title='Liczba pokoi',
    yaxis_title='Średnia cena (PLN)'
)

layout = html.Div(
    [
        dbc.Row([
            html.H1('Analiza dotycząca liczby pokoi')
        ], style={'textAlign': 'center'}),
        dbc.Row([
            html.P('Na tej stronie znajdują się wykresy, w których ważną rolę odgrywa liczba pokoi. Znajdziemy tutaj zależności pomiędzy liczbą pokoi a ceną, ofertami oraz metrażem.')
        ]),
        html.Hr(),
        dbc.Row([
            html.P('Zanim jednak przyjrzymy się wykresom obrazującym liczbę pokoi, zerkniemy na wykres przedstawiający rozkład średniego metrażu mieszkań w warszawskich dzielnicach.')
        ]),
        dbc.Row([
            html.P('Z wykresu możemy wyczytać, że mieszkania o największym metrażu znajdują się w dzielnicy Wesoła. Mieszkania są większe od mieszkań na Wilanowie o średnio ponad 10 metrów kwadratowych. Natomiast różnica pomiędzy mieszkaniami w Wesołej, a tymi w dzielnicy Włochy, które są najmniejsze, to ponad 40 metrów kwadratowych.')
        ]),
        dbc.Row([
            dcc.Graph(
                id='area-district-barplot',
                figure=fig
            )
        ]),
        html.Hr(),
        dbc.Row([
            html.P('Pierwszym wykresem związanym z liczbą pokoi jest wykres obrazujący zależność między średnią ceną mieszkań, a pokojami.')
        ]),
        dbc.Row([
            dcc.Graph(
                id='mean-rooms-barplot',
                figure=fig1
            )
        ]),
        dbc.Row([
            html.P('Wykres \'Rozkład liczby pokoi w ofertach\' obrazuje jak wygląda liczebność pokoi w różnych ofertach. Możemy tutaj zauważyć, że najwięcej ofert zostało wystawionych z 2 lub 3 pokojami.')
        ]),
        dbc.Row([
            html.P('W przypadku tego wykresu możemy dokładniej sprawdzić ilość ofert, operując na interesującej nas ilości pokoi.')
        ]),
        dbc.Row([
            dcc.Graph(id='room-offer-histogram')
        ]),
        dbc.Row([
            dcc.RangeSlider(
                id='room-offer-slider',
                min=data['Rooms'].min(),
                max=data['Rooms'].max(),
                value=[data['Rooms'].min(), data['Rooms'].max()],
                marks={str(room): str(room) for room in range(int(data['Rooms'].min()), int(data['Rooms'].max()))}
            )
        ]),
        html.Hr(),
        dbc.Row([
            html.P('Poniższe dwa wykresy są do siebie bardzo podobne. Pierwszy z nich przedstawia zależność metrażu od liczby pokoi z uwzględnieniem dzielnic, w których mieszkania się znajdują. Natomiast drugi z nich przedstawia zależność między liczbą pokoi, a ceną mieszkań również z uwzględnieniem dzielnic, w których się one znajdują.')
        ]),
        dbc.Row([
            html.P('W przypadku obu wykresów możemy sprawdzić dokładniejszą liczbę pokoi w zależności od wybranej dzielnicy. Trzeba jednak pamiętać, że wraz z wyborem dzielnicy, oba wykresy się zmieniają.')
        ]),
        dbc.Row([
            dcc.Dropdown(
                id='location-dropdown',
                options=[{'label': district, 'value': district} for district in districts],
                value=[],
                multi=True,
                clearable=False
            )
        ]),
        dbc.Row([
            dcc.Graph(id='room-m2-scatter')
        ]),
        dbc.Row([
            dcc.Graph(id='room-price-scatter')
        ])
    ], style={'margin-right': '20px'}
)

@callback(
    Output('room-offer-histogram', 'figure'),
    [Input('room-offer-slider', 'value')]
)
def update_room_offer_histogram(room_range):
    filtered_data = data[(data['Rooms'] >= room_range[0]) & (data['Rooms'] <= room_range[1])]
    fig2=px.histogram(filtered_data, x='Rooms', nbins=30, title='Rozkład liczby pokoi w ofertach', color_discrete_sequence=['royalblue'])
    fig2.update_layout(
        xaxis_title='Liczba pokoi',
        yaxis_title='Liczba ofert'
    )
    return fig2

@callback(
    Output('room-m2-scatter', 'figure'),
    [Input('location-dropdown', 'value')]
)
def update_room_m2_scatter(selected_location):
    if not selected_location:
        filtered_data = data
    else:
        filtered_data = data[data['District'].isin(selected_location)]
    
    fig3=px.scatter(filtered_data, x='Rooms', y='m2', title='Zależność metrażu od liczby pokoi', color='District')
    fig3.update_layout(
        xaxis_title='Liczba pokoi',
        yaxis_title='Metraż (m2)'
    )
    return fig3

@callback(
    Output('room-price-scatter', 'figure'),
    [Input('location-dropdown', 'value')]
)
def update_room_price_scatter(selected_location):
    if not selected_location:
        filtered_data = data
    else:
        filtered_data = data[data['District'].isin(selected_location)]
    
    fig4=px.scatter(filtered_data, x='Rooms', y='Price', title='Zależność między liczbą pokoi a ceną mieszkania', color='District')
    fig4.update_layout(
        xaxis_title='Liczba pokoi',
        yaxis_title='Cena (PLN)'
    )
    return fig4