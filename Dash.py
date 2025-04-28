import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd


def bar_graph_filter(original_db):
    filtered_df = original_db[(original_db['State'] == 'United States') &
                              (original_db['Cause Name'].isin(['All causes', 'Unintentional injuries']))]
    grouped_df = filtered_df.groupby(['Year', 'Cause Name'], as_index=False)['Deaths'].sum()
    pivot_df = grouped_df.pivot(index='Year', columns='Cause Name', values='Deaths')
    pivot_df.reset_index(inplace=True)
    return pivot_df


def heart_disease_diabetes_filter(original_db):
    filtered_df = original_db[(original_db['State'] == 'United States') &
                              (original_db['Cause Name'].isin(['Heart disease', 'Diabetes']))]
    grouped_df = filtered_df.groupby(['Year', 'Cause Name'], as_index=False)['Deaths'].sum()
    pivot_df = grouped_df.pivot(index='Year', columns='Cause Name', values='Deaths')
    pivot_df.reset_index(inplace=True)
    return pivot_df


df = pd.read_csv('Causes_of_Death.csv')

filtered_data_bar_graph = bar_graph_filter(df)
filtered_data_line_graphs = heart_disease_diabetes_filter(df)

causes = df['Cause Name'].unique()
states = df['State'].unique()

app = dash.Dash()
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Death in the United States',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    html.H2(
        children='All Causes vs Unintentional Injuries',
        style={
            'textAlign': 'center',
            'color': colors['text'],
            'marginTop': '40px',
        }
    ),
    dcc.Graph(
        id='Graph1',
        figure={
            'data': [
                {
                    'x': filtered_data_bar_graph['Year'],
                    'y': filtered_data_bar_graph['All causes'],
                    'type': 'bar',
                    'name': 'All causes',
                },
                {
                    'x': filtered_data_bar_graph['Year'],
                    'y': filtered_data_bar_graph['Unintentional injuries'],
                    'type': 'bar',
                    'name': 'Unintentional injuries',
                },
            ],
            'layout': {
                'title': 'All Causes vs Unintentional Injuries',
                'barmode': 'group',
                'xaxis': {
                    'title': 'Year',
                    'tickmode': 'array',
                    'tickvals': filtered_data_bar_graph['Year'],
                    'ticktext': filtered_data_bar_graph['Year'].astype(str),
                },
                'yaxis': {
                    'title': 'Death Amount',
                },
                'plot_bgcolor': '#f9f9f9',
                'paper_bgcolor': '#f9f9f9',
                'font': {
                    'color': 'black',
                },
            }
        }
    ),
    html.H2(
        children='Heart Disease Deaths in the United States Over Time',
        style={
            'textAlign': 'center',
            'color': colors['text'],
            'marginTop': '40px',
        }
    ),
    dcc.Graph(
        id='HeartDiseaseLineGraph',
        figure={
            'data': [
                {
                    'x': filtered_data_line_graphs['Year'],
                    'y': filtered_data_line_graphs['Heart disease'],
                    'type': 'scatter',
                    'mode': 'lines+markers',
                    'name': 'Heart disease',
                },
            ],
            'layout': {
                'title': 'Heart Disease Deaths in the United States (Over Time)',
                'xaxis': {
                    'title': 'Year',
                    'tickmode': 'array',
                    'tickvals': filtered_data_line_graphs['Year'],
                    'ticktext': filtered_data_line_graphs['Year'].astype(str),
                },
                'yaxis': {
                    'title': 'Death Amount',
                },
                'plot_bgcolor': '#f9f9f9',
                'paper_bgcolor': '#f9f9f9',
                'font': {
                    'color': 'black',
                },
            }
        }
    ),
    html.H2(
        children='Diabetes Deaths in the United States Over Time',
        style={
            'textAlign': 'center',
            'color': colors['text'],
            'marginTop': '40px',
        }
    ),
    dcc.Graph(
        id='DiabetesLineGraph',
        figure={
            'data': [
                {
                    'x': filtered_data_line_graphs['Year'],
                    'y': filtered_data_line_graphs['Diabetes'],
                    'type': 'scatter',
                    'mode': 'lines+markers',
                    'name': 'Diabetes',
                },
            ],
            'layout': {
                'title': 'Diabetes Deaths in the United States (Over Time)',
                'xaxis': {
                    'title': 'Year',
                    'tickmode': 'array',
                    'tickvals': filtered_data_line_graphs['Year'],
                    'ticktext': filtered_data_line_graphs['Year'].astype(str),
                },
                'yaxis': {
                    'title': 'Death Amount',
                },
                'plot_bgcolor': '#f9f9f9',
                'paper_bgcolor': '#f9f9f9',
                'font': {
                    'color': 'black',
                },
            }
        }
    ),
    html.H2(
        children='Death by Cause per State',
        style={
            'textAlign': 'center',
            'color': colors['text'],
            'marginTop': '40px',
        }
    ),
    html.Div(
        children=[
            html.Div(
                children=[
                    dcc.Dropdown(
                        id='cause-dropdown',
                        options=[{'label': cause, 'value': cause} for cause in causes],
                        value='Heart disease',
                        style={'width': '200px', 'padding': '10px'}
                    ),
                ],
                style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center', 'color': colors['text'],
                       'marginTop': '20px'}
            ),
            html.Div(
                children=[
                    dcc.Dropdown(
                        id='state-dropdown',
                        options=[{'label': state, 'value': state} for state in states],
                        value='United States',  # Default value
                        style={'width': '200px', 'padding': '10px'}
                    ),
                ],
                style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center', 'color': colors['text'],
                       'marginTop': '20px'}
            )
        ],
        style={'textAlign': 'center', 'marginTop': '40px'}
    ),
    dcc.Graph(id='interactive-graph')
])


@app.callback(
    Output('interactive-graph', 'figure'),
    [Input('cause-dropdown', 'value'),
     Input('state-dropdown', 'value')]
)
def update_interactive_graph(cause, state):
    filtered_df = df[(df['State'] == state) & (df['Year'] >= 2000)]

    if cause == 'Both':
        causes = ['Heart disease', 'Diabetes']
    else:
        causes = [cause]

    filtered_df = filtered_df[filtered_df['Cause Name'].isin(causes)]
    grouped_df = filtered_df.groupby(['Year', 'Cause Name'], as_index=False)['Deaths'].sum()
    pivot_df = grouped_df.pivot(index='Year', columns='Cause Name', values='Deaths')
    pivot_df.reset_index(inplace=True)

    data = []
    for cause in causes:
        data.append({
            'x': pivot_df['Year'],
            'y': pivot_df[cause],
            'type': 'scatter',
            'mode': 'lines+markers',
            'name': cause,
        })

    return {
        'data': data,
        'layout': {
            'title': f'Deaths due to {", ".join(causes)} Over Time ({state})',
            'xaxis': {
                'title': 'Year',
                'tickmode': 'array',
                'tickvals': pivot_df['Year'],
                'ticktext': pivot_df['Year'].astype(str),
            },
            'yaxis': {
                'title': 'Death Amount',
            },
            'plot_bgcolor': '#f9f9f9',
            'paper_bgcolor': '#f9f9f9',
            'font': {
                'color': 'black',
            },
        }
    }


if __name__ == '__main__':
    app.run(debug=True)


