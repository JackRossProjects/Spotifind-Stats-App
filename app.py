import dash
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd

df = pd.read_csv('song_data.csv')

def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

app = dash.Dash()

app.layout = html.Div(children=[
    html.H4(children='Song Stats'),
    dcc.Dropdown(id='dropdown', options=[
        {'label': i, 'value': i} for i in df.song_name.unique()
    ], multi=True, placeholder='Songs'),
    html.Div(id='table-container')
])

@app.callback(
    dash.dependencies.Output('table-container', 'children'),
    [dash.dependencies.Input('dropdown', 'value')])
def display_table(dropdown_value):
    if dropdown_value is None:
        return generate_table(df)

    dff = df[df.song_name.str.contains('|'.join(dropdown_value))]
    return generate_table(dff)

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

if __name__ == '__main__':
    app.run_server(debug=True)


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