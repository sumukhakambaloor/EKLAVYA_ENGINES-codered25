import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Initialize the Dash app
app = dash.Dash(__name__)
app.title = "Ekalavya Engines Visualization Dashboard"

# Load dataset from a linked CSV file
data_path = "EKLAVYA_ENGINES/filtered_dataset.csv"  # Path to the CSV file
data = pd.read_csv(data_path)

# Layout of the app
app.layout = html.Div([
    html.H1("Ekalavya Engines Visualization Dashboard", style={"textAlign": "center", "color": "white"}),

    # Dropdowns for chart selection and parameters
    html.Div([
        html.Div([
            html.Label("Choose Chart Type:", style={"color": "white"}),
            dcc.Dropdown(
                id="chart-type",
                options=[
                    {"label": "Bar Chart", "value": "bar"},
                    {"label": "Pie Chart", "value": "pie"},
                    {"label": "Line Chart", "value": "line"},
                    {"label": "Scatter Plot", "value": "scatter"},
                    {"label": "Histogram", "value": "histogram"},
                    {"label": "Box Plot", "value": "box"}
                ],
                value="bar",
                style={"width": "50%"}
            )
        ], style={"margin": "10px"}),

        html.Div([
            html.Label("Choose X-axis:", style={"color": "white"}),
            dcc.Dropdown(
                id="x-axis",
                options=[{"label": col, "value": col} for col in data.columns],
                value=data.columns[0],
                style={"width": "50%"}
            )
        ], style={"margin": "10px"}),

        html.Div([
            html.Label("Choose Y-axis (if applicable):", style={"color": "white"}),
            dcc.Dropdown(
                id="y-axis",
                options=[{"label": col, "value": col} for col in data.columns],
                value=data.columns[1],
                style={"width": "50%"}
            )
        ], style={"margin": "10px"}),

        html.Div([
            html.Label("Choose Category (if applicable):", style={"color": "white"}),
            dcc.Dropdown(
                id="category",
                options=[{"label": col, "value": col} for col in data.columns],
                value=data.columns[2],
                style={"width": "50%"}
            )
        ], style={"margin": "10px"})
    ]),

    # Graph display
    dcc.Graph(id="dynamic-chart")
], style={"backgroundColor": "#2c2c2c", "padding": "20px"})

# Callback to update the chart
@app.callback(
    Output("dynamic-chart", "figure"),
    [Input("chart-type", "value"),
     Input("x-axis", "value"),
     Input("y-axis", "value"),
     Input("category", "value")]
)
def update_chart(chart_type, x_axis, y_axis, category):
    if data is not None and x_axis is not None:
        if chart_type == "bar":
            fig = px.bar(data, x=x_axis, y=y_axis, color=category, barmode="group")
        elif chart_type == "pie":
            fig = px.pie(data, names=x_axis, values=y_axis, title=f"{y_axis} by {x_axis}")
        elif chart_type == "line":
            fig = px.line(data, x=x_axis, y=y_axis, color=category, title=f"{y_axis} over {x_axis}")
        elif chart_type == "scatter":
            fig = px.scatter(data, x=x_axis, y=y_axis, color=category, size=y_axis, title="Scatter Plot")
        elif chart_type == "histogram":
            fig = px.histogram(data, x=x_axis, color=category, title=f"Distribution of {x_axis}")
        elif chart_type == "box":
            fig = px.box(data, x=category, y=y_axis, color=category, title=f"{y_axis} Distribution by {category}")
        else:
            fig = px.bar()
        fig.update_layout(plot_bgcolor="#2c2c2c", paper_bgcolor="#2c2c2c", font_color="white")
        return fig
    return px.bar()

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
