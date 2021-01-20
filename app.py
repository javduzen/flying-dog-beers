import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

import yfinance as yf
import pandas as pd
from datetime import datetime



start_date = "2018-01-01"
end_date = datetime.today().strftime('%Y-%m-%d')
#end_date = "2021-01-16"


class Hist_data:
 
    def __init__(self, start, end, stock_name):
        self.start = start 
        self.end = end
        self.stock_name = stock_name
     
    def Stock(self):

        coin_aux = yf.Ticker(self.stock_name)
        coin  =  coin_aux.history(start=self.start,  end=self.end)
        coin = coin.drop(columns=['Dividends', 'Stock Splits'])            
        return coin
    
    def Stock_clp(self):
        clp_aux = yf.Ticker(self.stock_name)
        clp  =  clp_aux.history(start=self.start,  end=self.end)
        #rellenar fechas que faltan
        r = pd.date_range(start=start_date, end=end_date)
        clp = clp.reindex(r).fillna(0.0)
        clp = clp.drop(columns=['Dividends', 'Stock Splits'])
        #rellenar precio de findesemana con el del viernes
        clp = clp.replace(to_replace=0, method='ffill')
        return clp


test_btc = Hist_data(start_date,end_date,"BTC-USD")
data_btc = test_btc.Stock()

test_eth = Hist_data(start_date,end_date,"ETH-USD")
data_eth = test_eth.Stock()

test_clp = Hist_data(start_date,end_date,"CLP%3DX")
data_clp = test_clp.Stock_clp()

"""with pd.ExcelWriter('output.xlsx') as writer:  
    data_btc.to_excel(writer, sheet_name='data_btc')
    data_eth.to_excel(writer, sheet_name='data_eth')
    data_clp.to_excel(writer, sheet_name='data_clp')
    """

df = data_btc.copy()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

#VARIABLES
#primer grafico BTC
df = data_btc.copy()
fig = go.Figure(data=[go.Candlestick(x=df.index,
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'])])

#segundo grafico USD-CLP
df2 = data_clp.copy()
fig2 = go.Figure(data=[go.Candlestick(x=df2.index,
                open=df2['Open'],
                high=df2['High'],
                low=df2['Low'],
                close=df2['Close'])])

#tercer grafico ETH
df3 = data_eth.copy()
fig3 = go.Figure(data=[go.Candlestick(x=df3.index,
                open=df3['Open'],
                high=df3['High'],
                low=df3['Low'],
                close=df3['Close'])])


########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title="Graphs"

########### Set up the layout

    
app.layout = html.Div(children=[
    # All elements from the top of the page
    html.Div([
        html.H1(children='BTC-USD'),

        html.Div(children='''
            Description.
        '''),

        dcc.Graph(
            id='graph1',
            figure=fig
        ),  
    ]),
    # New Div for all elements in the new 'row' of the page
    html.Div([
        html.H1(children='CLP-USD'),

        html.Div(children='''
            Description.
        '''),

        dcc.Graph(
            id='graph2',
            figure=fig2
        ),  
    ]),
        # New Div for all elements in the new 'row' of the page
    html.Div([
        html.H1(children='ETH-USD'),

        html.Div(children='''
            Description.
        '''),

        dcc.Graph(
            id='graph3',
            figure=fig3
        ),  
    ]),
            
])   
    
if __name__ == '__main__':
    app.run_server()
