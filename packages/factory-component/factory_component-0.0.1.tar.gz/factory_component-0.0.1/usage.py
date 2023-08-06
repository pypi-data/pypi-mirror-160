import factory_component
from dash import Dash, html, Input, Output

app = Dash(__name__)

app.layout = html.Div([
    factory_component.Rnd(
        default={
                    'x': 0,
                    'y': 0,
                    'width': 320,
                    'height': 200,
                },
        style={'background':'red'},
    )
])


if __name__ == '__main__':
    app.run_server(debug=True)
