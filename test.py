import agdash
import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import pandas as pd

app = dash.Dash(__name__)

app.scripts.config.serve_locally = True
app.css.config.serve_locally = True

df = pd.read_csv(
    'https://raw.githubusercontent.com/plotly/'
    'datasets/master/gapminderDataFiveYear.csv', usecols = ['country', 'year', 'pop', 'continent', 'lifeExp', 'gdpPercap'], dtype={
            "country" : str,
            "year" : int,
            "pop" : float,
            "continent" : str,
            "lifeExp" : float,
            "gdpPercap" : float
        }) 

app.layout = html.Div([
    agdash.dashag(
        id='input',
        columnDefs= [{
            'headerName': 'Country', 'field': 'country'
        }, {
            'headerName': 'Year', 'field': 'year'
        }, {
            'headerName': 'Pop', 'field': 'pop', 'cellRenderer':'''function(params){
                   if (params.value !== undefined && params.value !== null){
                       return '<b> $' + (params.value) + '</b>';
                   }
                   return "" 
               }'''
        }, {
           'headerName': 'Continent', 'field': 'continent', 'editable': True 
        },  {
           'headerName': 'Life Expentancy', 'field': 'lifeExp' 
        },  {
           'headerName': 'GDP Percap', 'field': 'gdpPercap' 
        }],
        rowData= []
    ),
    html.Button(id='submit-button', n_clicks=0, children='Update data'),
    html.Div(id='output', children='no data')
])

@app.callback(Output('input', 'rowData'),
              [Input('submit-button', 'n_clicks')])
def update_output(n_clicks):
    return df[0:5].to_dict('rows') if n_clicks != 0 else df.to_dict('rows')


@app.callback(Output('output', 'children'),
              [Input('input', 'cellValueChanged')])
def update_outp(data):
    print(data)
    return 'cell data has been changed {}'.format(data) if data != None else 'nodata'


if __name__ == '__main__':
    app.run_server(debug=True)
