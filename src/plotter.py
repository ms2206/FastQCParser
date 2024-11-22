import pandas as pd
from pandas import DataFrame
import plotly.graph_objects as go
import plotly.express as px
from scipy.stats import norm
from plotly.subplots import make_subplots
import os
import pdb


default_figsize = go.Layout(width=900, height=600)


def plot_adap_cont(cli_arg: str, output_dir:str) -> None:
    """
    Plot and save plot_adap_cont to ~/Downloads/
    :return: None
    """
    try:

        # Extract data from file
        csv_path = os.path.join(output_dir, f'{cli_arg}_report.csv')
        data = pd.read_csv(csv_path)

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
        html_path = os.path.join(output_dir, f'{cli_arg}_plot.html')
        fig.write_html(html_path)

        # Save as PNG
        png_path = os.path.join(output_dir, f'{cli_arg}_plot.png')
        fig.write_image(png_path)

    except Exception as e:
        print(f'An error occurred when making output for {cli_arg}: {e}')


def plot_per_base_seq_qual(cli_arg: str, output_dir:str) -> None:
    """
    Plot and save per_base_seq_qual to ~/Downloads/
    :return: None
    """

    try:

        # Extract data from file
        csv_path = os.path.join(output_dir, f'{cli_arg}_report.csv')
        data = pd.read_csv(csv_path)

        box_plots = []

        # Collect data points for manually creating box plot
        for index, row in data.iloc[:, 1:].iterrows():

            # `#Base` can be represented as `DD-DD` in some fastcq files
            # first try cast to int
            try:
                x_name = str(int(row['#Base']))
            except ValueError:
                x_name = str(row['#Base'])

            box_plots.append(
                go.Box(y=[row['Lower Quartile'], row['Median'], row['Upper Quartile']],
                       name=x_name,
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
            xaxis=dict(tickangle=90)
        )

        # Save as HTML
        html_path = os.path.join(output_dir, f'{cli_arg}_plot.html')
        fig.write_html(html_path)

        # Save as PNG
        png_path = os.path.join(output_dir, f'{cli_arg}_plot.png')
        fig.write_image(png_path)

    except Exception as e:
        print(f'An error occurred when making output for {cli_arg}: {e}')


def plot_per_tile_seq_qual(cli_arg: str, output_dir:str) -> None:
    """
    Plot and save per_tile_seq_qual to ~/Downloads/
    :return: None
    """

    try:

        # Extract data from file
        csv_path = os.path.join(output_dir, f'{cli_arg}_report.csv')
        data = pd.read_csv(csv_path)

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
        html_path = os.path.join(output_dir, f'{cli_arg}_plot.html')
        fig.write_html(html_path)

        # Save as PNG
        png_path = os.path.join(output_dir, f'{cli_arg}_plot.png')
        fig.write_image(png_path)

    except Exception as e:
        print(f'An error occurred when making output for {cli_arg}: {e}')


def plot_per_seq_qual_scores(cli_arg: str, output_dir:str) -> None:
    """
    Plot and save per_seq_qual_scores to ~/Downloads/
    :return: None
    """

    try:

        # Extract data from file
        csv_path = os.path.join(output_dir, f'{cli_arg}_report.csv')
        data = pd.read_csv(csv_path)

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
        html_path = os.path.join(output_dir, f'{cli_arg}_plot.html')
        fig.write_html(html_path)

        # Save as PNG
        png_path = os.path.join(output_dir, f'{cli_arg}_plot.png')
        fig.write_image(png_path)

    except Exception as e:
        print(f'An error occurred when making output for {cli_arg}: {e}')


def plot_per_base_seq_content(cli_arg: str, output_dir:str) -> None:
    """
    Plot and save per_base_seq_content to ~/Downloads/
    :return: None
    """

    try:

        # Extract data from file
        csv_path = os.path.join(output_dir, f'{cli_arg}_report.csv')
        data = pd.read_csv(csv_path)

        # Create a Plotly figure
        fig = go.Figure(layout=default_figsize)

        # Add traces for each column
        for column in data.columns[2:]:
            fig.add_trace(go.Scatter(x=data['#Base'], y=data[column], mode='lines', name=column))

        # Update layout
        fig.update_layout(
            title='Per base sequence content',
            xaxis_title='Position in read (bp)',
            yaxis_title='Sequence content across all bases',
            template='plotly_white',
        )

        # Update y axis range
        fig.update_yaxes(range=[0, 100])

        # Save as HTML
        html_path = os.path.join(output_dir, f'{cli_arg}_plot.html')
        fig.write_html(html_path)

        # Save as PNG
        png_path = os.path.join(output_dir, f'{cli_arg}_plot.png')
        fig.write_image(png_path)

    except Exception as e:
        print(f'An error occurred when making output for {cli_arg}: {e}')


def plot_per_seq_GC_cont(cli_arg: str, output_dir:str) -> None:
    """
    Plot and save per_base_seq_content to ~/Downloads/
    :return: None
    """

    try:

        # Extract data from file
        csv_path = os.path.join(output_dir, f'{cli_arg}_report.csv')
        data = pd.read_csv(csv_path)

        # For Theoretical Distribution
        ## Calculate Mean
        mean = data['#GC Content'].mean()
        st_dev = 10

        # Scaled distribution of GC Content
        probability_density = norm.pdf(data['#GC Content'], mean, st_dev) * 4.5e7
        data['probability_density'] = probability_density

        # Create a Plotly figure
        fig = go.Figure(layout=default_figsize)

        # Add traces
        fig.add_trace(go.Scatter(x=data['#GC Content'], y=data['Count'], name='GC Content'))
        fig.add_trace(go.Scatter(x=data['#GC Content'], y=data['probability_density'], line=dict(dash='dash'),
                                 name='Theoretical Distribution'))

        # Update layout
        fig.update_layout(
            title='Per sequence GC content',
            xaxis_title='GC content',
            yaxis_title='Count',
            template='plotly_white',
        )

        # Save as HTML
        html_path = os.path.join(output_dir, f'{cli_arg}_plot.html')
        fig.write_html(html_path)

        # Save as PNG
        png_path = os.path.join(output_dir, f'{cli_arg}_plot.png')
        fig.write_image(png_path)

    except Exception as e:
        print(f'An error occurred when making output for {cli_arg}: {e}')


def plot_per_base_N_cont(cli_arg: str, output_dir:str) -> None:
    """
    Plot and save per_base_N_cont to ~/Downloads/
    :return: None
    """

    try:

        # Extract data from file
        csv_path = os.path.join(output_dir, f'{cli_arg}_report.csv')
        data = pd.read_csv(csv_path)

        # Make Figure
        fig = go.Figure(layout=default_figsize)

        fig.add_trace(go.Scatter(x=data['#Base'], y=data['N-Count'], name='N-Count'))

        fig.update_yaxes(range=[0, 100])

        # Update layout
        fig.update_layout(
            title='Adapter content by position',
            xaxis_title='Position in read (bp)',
            yaxis_title='N content across all bases',
            template='plotly_white',
            showlegend=True
        )

        # Save as HTML
        html_path = os.path.join(output_dir, f'{cli_arg}_plot.html')
        fig.write_html(html_path)

        # Save as PNG
        png_path = os.path.join(output_dir, f'{cli_arg}_plot.png')
        fig.write_image(png_path)

    except Exception as e:
        print(f'An error occurred when making output for {cli_arg}: {e}')


def plot_seq_len_dist(cli_arg: str, output_dir:str) -> None:
    """
    Plot and save per_base_N_cont to ~/Downloads/
    :return: None
    """

    try:

        # Extract data from file
        csv_path = os.path.join(output_dir, f'{cli_arg}_report.csv')
        data = pd.read_csv(csv_path)

        # Conver Count to Count (millions)
        data['Count_millions'] = [count / 1e6 for count in data['Count']]  # Convert to millions

        # Make Figure
        fig = go.Figure(layout=default_figsize)

        # Plot trace
        fig.add_trace(go.Bar(x=data['#Length'], y=data['Count_millions'], name='Count'))

        # Update layout
        fig.update_layout(
            title='Sequence Length Distribution',
            xaxis_title='Position in read (bp)',
            yaxis_title='Sequence Length (per million reads)',
            template='plotly_white',
        )

        # Update x-axis to show +/- 5 to show data spread
        fig.update_xaxes(range=[min(data['#Length']) - 5, max(data['#Length']) + 5], dtick=1)

        # Update y-axis for human-readable formatting
        fig.update_yaxes(tickformat=".2f", ticksuffix=" M")

        # Save as HTML
        html_path = os.path.join(output_dir, f'{cli_arg}_plot.html')
        fig.write_html(html_path)

        # Save as PNG
        png_path = os.path.join(output_dir, f'{cli_arg}_plot.png')
        fig.write_image(png_path)

    except Exception as e:
        print(f'An error occurred when making output for {cli_arg}: {e}')

def plot_seq_dup(cli_arg: str, output_dir:str) -> None:
    """
    Plot and save per_base_N_cont to ~/Downloads/
    :return: None
    """

    try:

        # Extract data from file
        csv_path = os.path.join(output_dir, f'{cli_arg}_report.csv')
        data = pd.read_csv(csv_path)

        # y value can be one of two
        y_value = 'Percentage of deduplicated' if 'Percentage of deduplicated' in data.columns else 'Percentage of total'

        fig = go.Figure(layout=default_figsize)

        fig.add_trace(
            go.Bar(x=data['#Duplication Level'], y=data[y_value], name='Percentage of deduplicated'))
        fig.add_trace(go.Bar(x=data['#Duplication Level'], y=data['Percentage of total'], name='Percentage of total'))

        # Update layout
        fig.update_layout(
            title='Sequence Duplication Levels',
            xaxis_title='Duplication Level',
            yaxis_title='Percentage of sequences',
            template='plotly_white',
        )

        # Save as HTML
        html_path = os.path.join(output_dir, f'{cli_arg}_plot.html')
        fig.write_html(html_path)

        # Save as PNG
        png_path = os.path.join(output_dir, f'{cli_arg}_plot.png')
        fig.write_image(png_path)

    except Exception as e:
        print(f'An error occurred when making output for {cli_arg}: {e}')

def plot_kmer_cont(cli_arg: str, output_dir:str) -> None:
    """
    Plot and save per_base_N_cont to ~/Downloads/
    :return: None
    """

    try:

        # Extract data from file
        csv_path = os.path.join(output_dir, f'{cli_arg}_report.csv')
        data = pd.read_csv(csv_path)

        fig = make_subplots(
            rows=1, cols=2,
            shared_yaxes=True,
            subplot_titles=['Obs/Exp Max', 'Max Obs/Exp Position'],
            horizontal_spacing=0.1
        )

        fig.add_trace(
            go.Bar(
                y=data['#Sequence'], x=data['Count'], name='Obs/Exp Max', orientation='h',
                marker=dict(color=data['Obs/Exp Max'], colorscale='Blues', line=dict(color='black', width=2))
            ), row=1, col=1
        )

        fig.add_trace(
            go.Bar(
                y=data['#Sequence'], x=data['Count'], name='Max Obs/Exp Position', orientation='h',
                marker=dict(color=data['Max Obs/Exp Position'], colorscale='Blues',
                            colorbar=dict(title='Color Scale', x=1.05, xanchor='left'), line=dict(color='black', width=2))
            ), row=1, col=2
        )

        # Update layout
        fig.update_layout(
            title="Sequence Counts",
            showlegend=False,
            xaxis=dict(title='Count of motifs', side='bottom', title_standoff=25),  # Centralize x-axis title
            xaxis2=dict(title='Count of motifs', side='bottom', title_standoff=25),  # Centralize for second subplot
            template='plotly_white',
            width=900, height=600
        )

        # Save as HTML
        html_path = os.path.join(output_dir, f'{cli_arg}_plot.html')
        fig.write_html(html_path)

        # Save as PNG
        png_path = os.path.join(output_dir, f'{cli_arg}_plot.png')
        fig.write_image(png_path)

    except Exception as e:
        print(f'An error occurred when making output for {cli_arg}: {e}')
