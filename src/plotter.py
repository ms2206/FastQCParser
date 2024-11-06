import pandas as pd
from pandas import DataFrame
import plotly.graph_objects as go


def plot_adap_cont() -> None:

    data = pd.read_csv('../data/processed/adap_cont/adap_cont.csv')

    # Create a Plotly figure
    fig = go.Figure()

    # Add traces for each column
    for column in data.columns[2:]:
        fig.add_trace(go.Scatter(x=data['#Position'], y=data[column], mode='lines', name=column))

    # Update layout
    fig.update_layout(
        title='Adapter content by position',
        xaxis_title='Position',
        yaxis_title='Adapter Content',
        legend_title='Adapter Type',
        template='plotly_white'
    )

    # Save as HTML
    fig.write_html('../data/processed/adap_cont/adap_cont.html')

    # Save as PNG
    fig.write_image('../data/processed/adap_cont/adap_cont.png')