import plotly.graph_objects as go
import pandas as pd


def draw_bmi_chart(bmi, age_months, sex):
    if sex == 1:  # Boys
        file_path = 'data/bfa-boys-zscore-expanded-tables.feather'
    elif sex == 2:  # Girls
        file_path = 'data/bfa-girls-zscore-expanded-tables.feather'
    else:
        raise ValueError("Invalid sex. Please use 1 for male or 2 for female.")

    # Load data from Excel file
    data = pd.read_feather(file_path)
    age_months_data = data['Day'] / 30.4375

    # Create traces for SD lines
    sd_lines = ['SD3neg', 'SD2neg', 'SD1neg', 'SD0', 'SD1', 'SD2', 'SD3']
    colors = ['black', 'red', '#DAA41F', 'green', '#DAA41F', 'red', 'black']
    labels = ['-3SD', '-2SD', '-1SD', 'Mean', '+1SD', '+2SD', '+3SD']
    traces = [
        go.Scatter(x=age_months_data,
                   y=data[sd],
                   mode='lines',
                   name=label,
                   line=dict(color=color),
                   showlegend=False)
        for sd, color, label in zip(sd_lines, colors, labels)
    ]

    # Add the child BMI point
    traces.append(
        go.Scatter(x=[age_months],
                   y=[bmi],
                   mode='markers',
                   name='Child Data Point',
                   marker=dict(color='red', size=10),
                   showlegend=False))

    # Add shapes for vertical and horizontal lines
    shapes = [
        dict(
            type='line',
            x0=24,
            y0=data['SD3neg'].min() - 1,
            x1=24,
            y1=24,
            line=dict(color="gray",width=2,dash="solid"))
    ] + [
        dict(type="rect",
             xref="paper",
             yref="paper",
             x0=0,
             y0=0,
             x1=1,
             y1=1,
             line=dict(color="black", width=1))
    ]

    # Add annotations for SD labels
    annotations = [
        dict(x=1.001,
             y=data[sd].iloc[-1],
             text=label,
             font=dict(color=color, size=8),
             xref="paper",
             yref="y",
             showarrow=False,
             xanchor="left")
        for sd, label, color in zip(sd_lines, labels, colors)
    ]

    # Layout configuration
    layout = go.Layout(xaxis=dict(title="Age (months)",
                                  tickvals=[0, 12, 24, 36, 48, 60],
                                  ticktext=[
                                      "Birth", "1 year", "2 years", "3 years",
                                      "4 years", "5 years"
                                  ],
                                  ticks="inside",
                                  range=[0, 61]),
                       yaxis=dict(title="BMI (kg/m²)", ticks="inside"),
                       shapes=shapes,
                       annotations=annotations,
                       plot_bgcolor="white",
                       dragmode="pan")
    # Cấu hình biểu đồ
    config = {
        'modeBarButtonsToRemove': [
            'toImage', 'sendDataToCloud', 'autoScale2d',
            'hoverCompareCartesian', 'hoverClosestCartesian', 'zoom2d',
            'toggleSpikelines'
        ],
        'displaylogo':
        False
    }
    # Create the figure and convert to JSON
    fig = go.Figure(data=traces, layout=layout)
    fig.update_traces(hovertemplate="%{x:.2f}, %{y:.2f}")

    return fig.to_json(), config


def draw_wfa_chart(weight, age_months, sex):
    if sex == 1:  # Boys
        file_path = 'data/wfa-boys-zscore-expanded-tables.feather'
    elif sex == 2:  # Girls
        file_path = 'data/wfa-girls-zscore-expanded-tables.feather'
    else:
        raise ValueError("Invalid sex. Please use 1 for male or 2 for female.")

    # Load data from Excel file
    data = pd.read_feather(file_path)
    age_months_data = data['Day'] / 30.4375

    # Create traces for SD lines
    sd_lines = ['SD3neg', 'SD2neg', 'SD0', 'SD2', 'SD3']
    colors = ['black', 'red', 'green', 'red', 'black']
    labels = ['-3SD', '-2SD', 'Mean', '+2SD', '+3SD']
    traces = [
        go.Scatter(x=age_months_data,
                   y=data[sd],
                   mode='lines',
                   name=label,
                   line=dict(color=color),
                   showlegend=False)
        for sd, color, label in zip(sd_lines, colors, labels)
    ]

    # Add the child weight point
    traces.append(
        go.Scatter(x=[age_months],
                   y=[weight],
                   mode='markers',
                   name='Child Data Point',
                   marker=dict(color='red', size=10),
                   showlegend=False))

    # Add shapes and layout
    shapes = [
        dict(type="rect",
             xref="paper",
             yref="paper",
             x0=0,
             y0=0,
             x1=1,
             y1=1,
             line=dict(color="black", width=1))
    ]

    # Add annotations for SD labels
    annotations = [
        dict(x=1.001,
             y=data[sd].iloc[-1],
             text=label,
             font=dict(color=color, size=8),
             xref="paper",
             yref="y",
             showarrow=False,
             xanchor="left")
        for sd, label, color in zip(sd_lines, labels, colors)
    ]
    layout = go.Layout(xaxis=dict(title="Age (months)",
                                  tickvals=[0, 12, 24, 36, 48, 60],
                                  ticktext=[
                                      "Birth", "1 year", "2 years", "3 years",
                                      "4 years", "5 years"
                                  ],
                                  ticks="inside",
                                  range=[0, 61]),
                       yaxis=dict(title="Weight (kg)", ticks="inside"),
                       shapes=shapes,
                       annotations=annotations,
                       plot_bgcolor="white",
                       dragmode="pan")
    # Cấu hình biểu đồ
    config = {
        'modeBarButtonsToRemove': [
            'toImage', 'sendDataToCloud', 'autoScale2d',
            'hoverCompareCartesian', 'hoverClosestCartesian', 'zoom2d',
            'toggleSpikelines'
        ],
        'displaylogo':
        False
    }
    # Create the figure and convert to JSON
    fig = go.Figure(data=traces, layout=layout)
    fig.update_traces(hovertemplate="%{x:.2f}, %{y:.2f}")

    return fig.to_json(), config


def draw_lhfa_chart(adjusted_lenhei, age_months, sex):
    if sex == 1:  # Boys
        file_path = 'data/lhfa-boys-zscore-expanded-tables.feather'
    elif sex == 2:  # Girls
        file_path = 'data/lhfa-girls-zscore-expanded-tables.feather'
    else:
        raise ValueError("Invalid sex. Please use 1 for male or 2 for female.")

    # Load data from Excel file
    data = pd.read_feather(file_path)
    age_months_data = data['Day'] / 30.4375

    # Create traces for SD lines
    sd_lines = ['SD3neg', 'SD2neg', 'SD0', 'SD2', 'SD3']
    colors = ['black', 'red', 'green', 'red', 'black']
    labels = ['-3SD', '-2SD', 'Mean', '+2SD', '+3SD']
    traces = [
        go.Scatter(x=age_months_data,
                   y=data[sd],
                   mode='lines',
                   name=label,
                   line=dict(color=color),
                   showlegend=False)
        for sd, color, label in zip(sd_lines, colors, labels)
    ]

    # Add the child length/height point
    traces.append(
        go.Scatter(x=[age_months],
                   y=[adjusted_lenhei],
                   mode='markers',
                   name='Child Data Point',
                   marker=dict(color='red', size=10),
                   showlegend=False))
    shapes = [
        dict(
            type='line',
            x0=24,
            y0=data['SD3neg'].min()-4,
            x1=24,
            y1=data['SD3'].max() + 5,
            line=dict(color="gray",width=2,dash="solid"))
    ] + [
        dict(type="rect",
             xref="paper",
             yref="paper",
             x0=0,
             y0=0,
             x1=1,
             y1=1,
             line=dict(color="black", width=1))
    ]

    # Add annotations for SD labels
    annotations = [
        dict(x=1.001,
             y=data[sd].iloc[-1],
             text=label,
             font=dict(color=color, size=8),
             xref="paper",
             yref="y",
             showarrow=False,
             xanchor="left")
        for sd, label, color in zip(sd_lines, labels, colors)
    ]
    # Add layout
    layout = go.Layout(xaxis=dict(title="Age (years)",
                                  tickvals=[0, 12, 24, 36, 48, 60],
                                  ticktext=[
                                      "Birth", "1 year", "2 years", "3 years",
                                      "4 years", "5 years"
                                  ],
                                  ticks="inside",
                                  range=[0, 61]),
                       yaxis=dict(title="Length/Height (cm)", ticks="inside"),
                       shapes=shapes,
                       annotations=annotations,
                       plot_bgcolor="white",
                       dragmode="pan")
    # Cấu hình biểu đồ
    config = {
        'modeBarButtonsToRemove': [
            'toImage', 'sendDataToCloud', 'autoScale2d',
            'hoverCompareCartesian', 'hoverClosestCartesian', 'zoom2d',
            'toggleSpikelines'
        ],
        'displaylogo':
        False
    }
    # Create the figure and convert to JSON
    fig = go.Figure(data=traces, layout=layout)
    fig.update_traces(hovertemplate="%{x:.2f}, %{y:.2f}")

    # Trả về biểu đồ dạng JSON
    return fig.to_json(), config


def draw_wfl_wfh_chart(weight, length_or_height, sex, measure_type):
    # Determine the file path based on sex and measurement type
    if length_or_height < 65:
        file_type = 'wfl'
    elif length_or_height > 110:
        file_type = 'wfh'
    else:
        file_type = 'wfl' if measure_type == 'l' else 'wfh'

    if sex == 1:  # Boys
        file_path = f"data/{file_type}-boys-zscore-expanded-tables.feather"
    elif sex == 2:  # Girls
        file_path = f"data/{file_type}-girls-zscore-expanded-tables.feather"
    else:
        raise ValueError("Invalid sex. Please use 1 for male or 2 for female.")

    # Load data from Excel file
    data = pd.read_feather(file_path)
    length_or_height_data = data['Length'] if file_type == 'wfl' else data[
        'Height']

    # Create traces for SD lines
    sd_lines = ['SD3neg', 'SD2neg', 'SD1neg', 'SD0', 'SD1', 'SD2', 'SD3']
    colors = ['black', 'red', '#DAA41F', 'green', '#DAA41F', 'red', 'black']
    labels = ['-3SD', '-2SD', '-1SD', 'Mean', '+1SD', '+2SD', '+3SD']
    traces = [
        go.Scatter(x=length_or_height_data,
                   y=data[sd],
                   mode='lines',
                   name=label,
                   line=dict(color=color),
                   showlegend=False)
        for sd, color, label in zip(sd_lines, colors, labels)
    ]

    # Add the child data point
    traces.append(
        go.Scatter(x=[length_or_height],
                   y=[weight],
                   mode='markers',
                   name='Child Data Point',
                   marker=dict(color='red', size=10),
                   showlegend=False))

    # Add layout configurations
    shapes = [
        dict(type="rect",
             xref="paper",
             yref="paper",
             x0=0,
             y0=0,
             x1=1,
             y1=1,
             line=dict(color="black", width=1))
    ]

    # Add annotations for SD labels
    annotations = [
        dict(x=1.001,
             y=data[sd].iloc[-1],
             text=label,
             font=dict(color=color, size=8),
             xref="paper",
             yref="y",
             showarrow=False,
             xanchor="left")
        for sd, label, color in zip(sd_lines, labels, colors)
    ]

    # Determine axis titles
    axis_title = "Length (cm)" if file_type == 'wfl' else "Height (cm)"

    # Create layout
    layout = go.Layout(xaxis=dict(
        title=axis_title,
        ticks="inside",
        range=[length_or_height_data.min(),
               length_or_height_data.max()]),
                       yaxis=dict(title="Weight (kg)", ticks="inside"),
                       shapes=shapes,
                       annotations=annotations,
                       plot_bgcolor="white",
                       dragmode="pan")

    # Configure the chart
    config = {
        'modeBarButtonsToRemove': [
            'toImage', 'sendDataToCloud', 'autoScale2d',
            'hoverCompareCartesian', 'hoverClosestCartesian', 'zoom2d',
            'toggleSpikelines'
        ],
        'displaylogo':
        False
    }

    # Create the figure and return as JSON
    fig = go.Figure(data=traces, layout=layout)
    fig.update_traces(hovertemplate="%{x:.2f}, %{y:.2f}")

    return fig.to_json(), config


def draw_bmi_chart_above5yr(bmi, age_months, sex):
    if sex == 1:  # Boys
        file_path = 'data/who2007/bfa-boys-z-who-2007-exp.feather'
    elif sex == 2:  # Girls
        file_path = 'data/who2007/bfa-girls-z-who-2007-exp.feather'
    else:
        raise ValueError("Invalid sex. Please use 1 for male or 2 for female.")

    # Load data from Excel file
    data = pd.read_feather(file_path)
    age_months_data = data['Month']

    # Create traces for SD lines
    sd_lines = ['SD3neg', 'SD2neg', 'SD1neg', 'SD0', 'SD1', 'SD2', 'SD3']
    colors = ['black', 'red', '#DAA41F', 'green', '#DAA41F', 'red', 'black']
    labels = ['-3SD', '-2SD', '-1SD', 'Mean', '+1SD', '+2SD', '+3SD']
    traces = [
        go.Scatter(x=age_months_data,
                   y=data[sd],
                   mode='lines',
                   name=label,
                   line=dict(color=color),
                   showlegend=False)
        for sd, color, label in zip(sd_lines, colors, labels)
    ]

    # Add the child BMI point
    traces.append(
        go.Scatter(x=[age_months],
                   y=[bmi],
                   mode='markers',
                   name='Child Data Point',
                   marker=dict(color='red', size=10),
                   showlegend=False))

    # Add shapes for vertical and horizontal lines
    shapes = [
        dict(type="rect",
             xref="paper",
             yref="paper",
             x0=0,
             y0=0,
             x1=1,
             y1=1,
             line=dict(color="black", width=1))
    ]

    # Add annotations for SD labels
    annotations = [
        dict(x=0.94,
             y=data[sd].iloc[-1],
             text=label,
             font=dict(color=color, size=10),
             xref="paper",
             yref="y",
             showarrow=False,
             xanchor="left")
        for sd, label, color in zip(sd_lines, labels, colors)
    ]

    # Layout configuration
    layout = go.Layout(xaxis=dict(title="Age (months)",
                                  tickvals=[
                                      61, 72, 84, 96, 108, 120, 132, 144, 156,
                                      168, 180, 192, 204, 216, 228
                                  ],
                                  ticks="inside",
                                  range=[61, 240]),
                       yaxis=dict(title="BMI (kg/m²)",
                                  ticks="inside",
                                  title_standoff=10),
                       shapes=shapes,
                       annotations=annotations,
                       plot_bgcolor="white",
                       dragmode="pan")
    # Cấu hình biểu đồ
    config = {
        'modeBarButtonsToRemove': [
            'toImage', 'sendDataToCloud', 'autoScale2d',
            'hoverCompareCartesian', 'hoverClosestCartesian', 'zoom2d',
            'toggleSpikelines'
        ],
        'displaylogo':
        False
    }
    # Create the figure and convert to JSON
    fig = go.Figure(data=traces, layout=layout)
    fig.update_traces(hovertemplate="%{x:.2f}, %{y:.2f}")

    return fig.to_json(), config


def draw_wfa_chart_above5yr(weight, age_months, sex):
    if sex == 1:  # Boys
        file_path = 'data/who2007/wfa-boys-z-who-2007-exp.feather'
    elif sex == 2:  # Girls
        file_path = 'data/who2007/wfa-girls-z-who-2007-exp.feather'
    else:
        raise ValueError("Invalid sex. Please use 1 for male or 2 for female.")

    # Load data from Excel file
    data = pd.read_feather(file_path)
    age_months_data = data['Month']

    # Create traces for SD lines
    sd_lines = ['SD3neg', 'SD2neg', 'SD0', 'SD2', 'SD3']
    colors = ['black', 'red', 'green', 'red', 'black']
    labels = ['-3SD', '-2SD', 'Mean', '+2SD', '+3SD']
    traces = [
        go.Scatter(x=age_months_data,
                   y=data[sd],
                   mode='lines',
                   name=label,
                   line=dict(color=color),
                   showlegend=False)
        for sd, color, label in zip(sd_lines, colors, labels)
    ]

    # Add the child weight point
    traces.append(
        go.Scatter(x=[age_months],
                   y=[weight],
                   mode='markers',
                   name='Child Data Point',
                   marker=dict(color='red', size=10),
                   showlegend=False))

    # Add shapes and layout
    shapes = [
        dict(type="rect",
             xref="paper",
             yref="paper",
             x0=0,
             y0=0,
             x1=1,
             y1=1,
             line=dict(color="black", width=1))
    ]

    # Add annotations for SD labels
    annotations = [
        dict(x=0.94,
             y=data[sd].iloc[-1],
             text=label,
             font=dict(color=color, size=10),
             xref="paper",
             yref="y",
             showarrow=False,
             xanchor="left")
        for sd, label, color in zip(sd_lines, labels, colors)
    ]
    layout = go.Layout(xaxis=dict(title="Age (months)",
                                  tickvals=[61, 72, 84, 96, 108, 120],
                                  ticks="inside",
                                  range=[61, 124]),
                       yaxis=dict(title="Weight (kg)",
                                  ticks="inside",
                                  title_standoff=10),
                       shapes=shapes,
                       annotations=annotations,
                       plot_bgcolor="white",
                       dragmode="pan")
    # Cấu hình biểu đồ
    config = {
        'modeBarButtonsToRemove': [
            'toImage', 'sendDataToCloud', 'autoScale2d',
            'hoverCompareCartesian', 'hoverClosestCartesian', 'zoom2d',
            'toggleSpikelines'
        ],
        'displaylogo':
        False
    }
    # Create the figure and convert to JSON
    fig = go.Figure(data=traces, layout=layout)
    fig.update_traces(hovertemplate="%{x:.2f}, %{y:.2f}")

    return fig.to_json(), config


def draw_lhfa_chart_above5yr(adjusted_lenhei, age_months, sex):
    if sex == 1:  # Boys
        file_path = 'data/who2007/lhfa-boys-z-who-2007-exp.feather'
    elif sex == 2:  # Girls
        file_path = 'data/who2007/lhfa-girls-z-who-2007-exp.feather'
    else:
        raise ValueError("Invalid sex. Please use 1 for male or 2 for female.")

    # Load data from Excel file
    data = pd.read_feather(file_path)
    age_months_data = data['Month']

    # Create traces for SD lines
    sd_lines = ['SD3neg', 'SD2neg', 'SD0', 'SD2', 'SD3']
    colors = ['black', 'red', 'green', 'red', 'black']
    labels = ['-3SD', '-2SD', 'Mean', '+2SD', '+3SD']
    traces = [
        go.Scatter(x=age_months_data,
                   y=data[sd],
                   mode='lines',
                   name=label,
                   line=dict(color=color),
                   showlegend=False)
        for sd, color, label in zip(sd_lines, colors, labels)
    ]

    # Add the child length/height point
    traces.append(
        go.Scatter(x=[age_months],
                   y=[adjusted_lenhei],
                   mode='markers',
                   name='Child Data Point',
                   marker=dict(color='red', size=10),
                   showlegend=False))
    shapes = [
        dict(type="rect",
             xref="paper",
             yref="paper",
             x0=0,
             y0=0,
             x1=1,
             y1=1,
             line=dict(color="black", width=1))
    ]

    # Add annotations for SD labels
    annotations = [
        dict(x=0.94,
             y=data[sd].iloc[-1],
             text=label,
             font=dict(color=color, size=10),
             xref="paper",
             yref="y",
             showarrow=False,
             xanchor="left")
        for sd, label, color in zip(sd_lines, labels, colors)
    ]
    # Add layout
    layout = go.Layout(xaxis=dict(title="Age (months)",
                                  tickvals=[
                                      61, 72, 84, 96, 108, 120, 132, 144, 156,
                                      168, 180, 192, 204, 216, 228
                                  ],
                                  ticks="inside",
                                  range=[61, 240]),
                       yaxis=dict(title="Length/Height (cm)",
                                  ticks="inside",
                                  title_standoff=10),
                       shapes=shapes,
                       annotations=annotations,
                       plot_bgcolor="white",
                       dragmode="pan")
    # Cấu hình biểu đồ
    config = {
        'modeBarButtonsToRemove': [
            'toImage', 'sendDataToCloud', 'autoScale2d',
            'hoverCompareCartesian', 'hoverClosestCartesian', 'zoom2d',
            'toggleSpikelines'
        ],
        'displaylogo':
        False
    }
    # Create the figure and convert to JSON
    fig = go.Figure(data=traces, layout=layout)
    fig.update_traces(hovertemplate="%{x:.2f}, %{y:.2f}")

    # Trả về biểu đồ dạng JSON
    return fig.to_json(), config
