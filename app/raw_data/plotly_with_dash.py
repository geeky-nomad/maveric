import pandas as pd
import plotly.express as px
from dash import Dash, html, dash_table, dcc

app = Dash()

df = pd.read_csv('election_results_2024.csv')
party_seat_counts = df['Leading Party'].value_counts()
# Combine smaller parties into 'OTHERS'
top_n = 10  # Adjust the number of top parties
top_parties = party_seat_counts.nlargest(top_n)
others_count = party_seat_counts[top_n:].sum()
top_parties['OTHERS'] = others_count


# app layout
app.layout = [
    html.Div(children='Election data'),
    dash_table.DataTable(data=df.to_dict('records'), page_size=10),
    dcc.Graph(figure=px.pie(

    ))

]


if __name__ == '__main__':
    app.run(debug=True)