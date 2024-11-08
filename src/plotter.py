import pandas as pd
from pandas import DataFrame
import plotly.graph_objects as go
import plotly.express as px

default_figsize = go.Layout(width=900, height=600)


def plot_adap_cont(cli_arg: str) -> None:
    """
    Plot and save plot_adap_cont to filepath
    :return: None
    """

    # Extract data from file
    data = pd.read_csv(f'../data/processed/{cli_arg}/{cli_arg}.csv')

    # Create a Plotly figure
    fig = go.Figure(layout=default_figsize)

    # Add traces for each column
    for column in data.columns[2:]:
        fig.add_trace(go.Scatter(x=data['#Position'], y=data[column], mode='lines', name=column))

    # Update layout
    fig.update_layout(
        title='Adapter content by position',
        xaxis_title='Position in read (bp)',
        yaxis_title='Adapter Content',
        legend_title='Adapter Type',
        template='plotly_white'
    )

    # Save as HTML
    fig.write_html(f'../data/processed/{cli_arg}/{cli_arg}.html')

    # Save as PNG
    fig.write_image(f'../data/processed/{cli_arg}/{cli_arg}.png')


def per_base_seq_qual(plot_type_name: str) -> None:
    """
    Plot and save per_base_seq_qual to filepath
    :return: None
    """

    data = pd.read_csv(f'../data/processed/{plot_type_name}/{plot_type_name}.csv')

    # Create a Plotly figure
    fig = go.Figure()


def plot_per_base_seq_qual(cli_arg: str) -> None:
    """
    Plot and save per_base_seq_qual to filepath
    :return: None
    """

    # Extract data from file
    data = pd.read_csv(f'../data/processed/{cli_arg}/{cli_arg}.csv')
    box_plots = []

    # Collect data points for manually creating box plot
    for index, row in data.iloc[:, 1:].iterrows():
        box_plots.append(
            go.Box(y=[row['Lower Quartile'], row['Median'], row['Upper Quartile']],
                   name=int(row['#Base']),
                   marker_color='black')
        )

    # Make Figure
    fig = go.Figure(data=box_plots, layout=default_figsize)

    # Add rectangles for colors to indicate thresholds: red
    fig.add_shape(type='rect', x0=0, x1=max(data['#Base']), y0=0, y1=20,
                  line=dict(color="mistyrose"),
                  fillcolor="mistyrose",
                  opacity=0.5)

    # Add rectangles for colors to indicate thresholds: yellow
    fig.add_shape(type='rect', x0=0, x1=max(data['#Base']), y0=20, y1=28,
                  line=dict(color="lightyellow"),
                  fillcolor="lightyellow",
                  opacity=0.5)

    # Add rectangles for colors to indicate thresholds: green
    fig.add_shape(type='rect', x0=0, x1=max(data['#Base']), y0=28, y1=max(data['Upper Quartile']) + 5,
                  line=dict(color='#03AC13'),
                  fillcolor='#03AC13',
                  opacity=0.1)

    fig.update_layout(
        title='Per base sequence quality',
        xaxis_title='Position in read (bp)',
        yaxis_title='Phred quality score',
        template='plotly_white',
        showlegend=False,
        yaxis=dict(range=[0, max(data['Upper Quartile']) + 5]),
        xaxis=dict(tickangle=0)
    )

    # Save as HTML
    fig.write_html(f'../data/processed/{cli_arg}/{cli_arg}.html')

    # Save as PNG
    fig.write_image(f'../data/processed/{cli_arg}/{cli_arg}.png')


def plot_per_tile_seq_qual(cli_arg: str) -> None:
    """
    Plot and save per_tile_seq_qual to filepath
    :return: None
    """

    # Extract data from file
    data = pd.read_csv(f'../data/processed/{cli_arg}/{cli_arg}.csv')

    # Plot heat map
    fig = px.density_heatmap(data, y='Base', x='#Tile', z='Mean', color_continuous_scale='Viridis', nbinsx=15,
                             nbinsy=15)
    fig.update_layout(
        title='Per aggregated tile sequence quality',
        yaxis_title='Position in read (bp)',
        xaxis_title='Tile position of flowcell',
        template='plotly_white',
        coloraxis_colorbar_title='Avg. Q30',
        width=900, height=600
    )

    # Save as HTML
    fig.write_html(f'../data/processed/{cli_arg}/{cli_arg}.html')

    # Save as PNG
    fig.write_image(f'../data/processed/{cli_arg}/{cli_arg}.png')


def plot_per_seq_qual_scores(cli_arg: str) -> None:
    """
    Plot and save per_seq_qual_scores to filepath
    :return: None
    """

    # Extract data from file
    data = pd.read_csv(f'../data/processed/{cli_arg}/{cli_arg}.csv')

    # Update the name from 40 to "Q40"
    data['Display'] = data['#Quality'].astype(str).apply(lambda x: 'Q' + x)

    # Plot treemap
    fig = px.treemap(data.iloc[:, 1:], path=['Display'], values='Count')

    fig.update_layout(
        title='Count of Phred score',
        template='plotly_white',
        width=900, height=600
    )

    # Save as HTML
    fig.write_html(f'../data/processed/{cli_arg}/{cli_arg}.html')

    # Save as PNG
    fig.write_image(f'../data/processed/{cli_arg}/{cli_arg}.png')
