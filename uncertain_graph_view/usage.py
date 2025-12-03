import uncertain_graph_view
from dash import Dash, callback, html, Input, Output

app = Dash(__name__)

app.layout = html.Div([
    uncertain_graph_view.UncertainGraphView(
        id='input',
        positions = [[3, 3], [7, 7]],
        radii = [0.5, 1],
        ccs = [["", "", "001", "001"], ["002", "002", "001", "002"]]
    ),
    html.Div(id='output')
])


# @callback(Output('output', 'children'), Input('input', 'value'))
# def display_output(value):
#     return 'You have entered {}'.format(value)


if __name__ == '__main__':
    app.run(debug=True, port=8080)
