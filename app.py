# STATS #

import dash
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd

app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
server = app.server
app.title='Spotifind'

colors = {
    'background': '#1DB954',
    'text': '#FFFFFF'
}


# UPDATE CLEANED CSV
df = pd.read_csv('songs_scaled.csv')

def generate_table(dataframe, max_rows=25):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H4(children='Song Stats'),
    dcc.Dropdown(id='dropdown', options=[
        {'label': i, 'value': i} for i in df.Song.unique()
    ], multi=True, placeholder='Songs'),
    html.Div(id='table-container')
])

@app.callback(
    dash.dependencies.Output('table-container', 'children'),
    [dash.dependencies.Input('dropdown', 'value')])
def display_table(dropdown_value):
    if dropdown_value is None:
        return generate_table(df)

    dff = df[df.Song.str.contains('|'.join(dropdown_value))]
    return generate_table(dff)

if __name__ == '__main__':
    app.run_server()


'''
import plotly.graph_objects as go

x = ['Danceability', 'Energy', 'Speechiness', 'Acousticness',
    'Instrumentalness', 'Liveness', 'Valence']
y = [df['danceability'][0], df['energy'][0],
     df['speechiness'][0], df['acousticness'][0], df['instrumentalness'][0],
     df['liveness'][0], df['audio_valence'][0]]

# Use textposition='auto' for direct text
fig = go.Figure(data=[go.Bar(
            x=x, y=y,
            text=y,
            textposition='auto',
        )],
    layout=go.Layout(
        title=go.layout.Title(text="Song Statistics")
    ))

fig.show()
'''
