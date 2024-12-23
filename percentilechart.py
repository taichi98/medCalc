import plotly.graph_objects as go
import pandas as pd


def draw_bmi_percentile_chart(bmi, age_months, sex):
    if sex == 1:  # Boys
        file_path = 'data/bfa-boys-percentiles-expanded-tables.feather'
    elif sex == 2:  # Girls
        file_path = 'data/bfa-girls-percentiles-expanded-tables.feather'
    else:
        raise ValueError("Invalid sex. Please use 1 for male or 2 for female.")

    # Load data from Excel file
    data = pd.read_feather(file_path)
    age_months_data = data['Age'] / 30.4375

    # Create traces for percentile lines
    percentiles = ['P3', 'P15', 'P50', 'P85', 'P97']
    colors = ['red', 'orange', 'green', 'orange', 'red']
    labels = ['3rd', '15th', '50th', '85th', '97th']
    traces = [
        go.Scatter(x=age_months_data,
                   y=data[percentile],
                   mode='lines',
                   name=label,
                   line=dict(color=color),
                   showlegend=False)
        for percentile, color, label in zip(percentiles, colors, labels)
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
        dict(type='line',
             x0=year * 12,
             y0=data['P3'].min() - 1,
             x1=year * 12,
             y1=data['P97'].max() + 1,
             line=dict(color="gray",
                       width=2 if year == 2 else 0.2,
                       dash="solid" if year == 2 else "dash"))
        for year in range(1, 6)
    ] + [
        dict(type='line',
             x0=age_months_data.min(),
             y0=y,
             x1=age_months_data.max(),
             y1=y,
             line=dict(color='gray', width=0.2, dash='dash'))
        for y in range(10, 22, 2)
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

    # Add annotations for Percentile labels
    annotations = [
        dict(x=1.001,
             y=data[percentile].iloc[-1],
             text=label,
             font=dict(color=color, size=8),
             xref="paper",
             yref="y",
             showarrow=False,
             xanchor="left")
        for percentile, label, color in zip(percentiles, labels, colors)
    ]

    # Layout configuration
    layout = go.Layout(xaxis=dict(title="Age (months)",
                                  tickvals=[0, 12, 24, 36, 48, 60],
                                  ticktext=[
                                      "Birth", "1 year", "2 years", "3 years",
                                      "4 years", "5 years"
                                  ],
                                  range=[0, 61]),
                       yaxis=dict(title="BMI (kg/m²)"),
                       margin=dict(l=30, r=30, t=20, b=20),
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


def draw_wfa_percentile_chart(weight, age_months, sex):
    if sex == 1:  # Boys
        file_path = 'data/wfa-boys-percentiles-expanded-tables.feather'
    elif sex == 2:  # Girls
        file_path = 'data/wfa-girls-percentiles-expanded-tables.feather'
    else:
        raise ValueError("Invalid sex. Please use 1 for male or 2 for female.")

    # Load data from Excel file
    data = pd.read_feather(file_path)
    age_months_data = data['Age'] / 30.4375

    # Create traces for percentile lines
    percentiles = ['P3', 'P15', 'P50', 'P85', 'P97']
    colors = ['red', 'orange', 'green', 'orange', 'red']
    labels = ['3rd', '15th', '50th', '85th', '97th']
    traces = [
        go.Scatter(x=age_months_data,
                   y=data[percentile],
                   mode='lines',
                   name=label,
                   line=dict(color=color),
                   showlegend=False)
        for percentile, color, label in zip(percentiles, colors, labels)
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
        dict(type='line',
             x0=year * 12,
             y0=data['P3'].min() - 1,
             x1=year * 12,
             y1=data['P97'].max() + 1,
             line=dict(color='gray', width=0.2, dash='solid'))
        for year in range(1, 6)
    ] + [
        dict(type="line",
             x0=age_months_data.min(),
             y0=y,
             x1=age_months_data.max(),
             y1=y,
             line=dict(color="gray", width=0.2, dash="dash"))
        for y in range(5, 25, 5)
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

    # Add annotations for percentile labels
    annotations = [
        dict(x=1.001,
             y=data[percentile].iloc[-1],
             text=label,
             font=dict(color=color, size=8),
             xref="paper",
             yref="y",
             showarrow=False,
             xanchor="left")
        for percentile, label, color in zip(percentiles, labels, colors)
    ]

    layout = go.Layout(xaxis=dict(title="Age (months)",
                                  tickvals=[0, 12, 24, 36, 48, 60],
                                  ticktext=[
                                      "Birth", "1 year", "2 years", "3 years",
                                      "4 years", "5 years"
                                  ],
                                  range=[0, 61]),
                       yaxis=dict(title="Weight (kg)"),
                       margin=dict(l=30, r=30, t=20, b=20),
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


def draw_lhfa_percentile_chart(adjusted_lenhei, age_months, sex):
    if sex == 1:  # Boys
        file_path = 'data/lhfa-boys-percentiles-expanded-tables.feather'
    elif sex == 2:  # Girls
        file_path = 'data/lhfa-girls-percentiles-expanded-tables.feather'
    else:
        raise ValueError("Invalid sex. Please use 1 for male or 2 for female.")

    # Load data from Excel file
    data = pd.read_feather(file_path)
    age_months_data = data['Day'] / 30.4375

    # Create traces for percentile lines (P3, P10, P25, P50, P75, P90, P97)
    percentiles = ['P3', 'P15', 'P50', 'P85', 'P97']
    colors = ['red', 'orange', 'green', 'orange', 'red']
    labels = ['3rd', '15th', '50th', '85th', '97th']
    traces = [
        go.Scatter(x=age_months_data,
                   y=data[percentile],
                   mode='lines',
                   name=label,
                   line=dict(color=color),
                   showlegend=False)
        for percentile, color, label in zip(percentiles, colors, labels)
    ]

    # Add the child length/height point
    traces.append(
        go.Scatter(x=[age_months],
                   y=[adjusted_lenhei],
                   mode='markers',
                   name='Child Data Point',
                   marker=dict(color='red', size=10),
                   showlegend=False))

    # Add shapes for the grid
    shapes = [
        dict(
            type='line',
            x0=year * 12,
            y0=data['P3'].min() - 10,
            x1=year * 12,
            y1=130,
            line=dict(
                color="gray",
                width=2 if year == 2 else 0.2,  # Nét dày hơn cho year = 2
                dash="solid" if year == 2 else "dash"  # Nét liền cho year = 2
            )) for year in range(1, 6)
    ] + [
        dict(type="line",
             x0=age_months_data.min(),
             y0=y,
             x1=age_months_data.max(),
             y1=y,
             line=dict(color="gray", width=0.2, dash="dash"))
        for y in range(40, 130, 10)
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

    # Add annotations for percentile labels
    annotations = [
        dict(x=1.001,
             y=data[percentile].iloc[-1],
             text=label,
             font=dict(color=color, size=8),
             xref="paper",
             yref="y",
             showarrow=False,
             xanchor="left")
        for percentile, label, color in zip(percentiles, labels, colors)
    ]

    # Add layout configuration
    layout = go.Layout(xaxis=dict(title="Age (months)",
                                  tickvals=[0, 12, 24, 36, 48, 60],
                                  ticktext=[
                                      "Birth", "1 year", "2 years", "3 years",
                                      "4 years", "5 years"
                                  ],
                                  range=[0, 61]),
                       yaxis=dict(title="Length/Height (cm)"),
                       margin=dict(l=30, r=30, t=20, b=20),
                       shapes=shapes,
                       annotations=annotations,
                       plot_bgcolor="white",
                       dragmode="pan")

    # Configuration for the chart
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


def draw_wfl_wfh_percentile_chart(weight, length_or_height, sex, measure_type):
    # Determine the file path based on sex and measurement type
    if length_or_height < 65:
        file_type = 'wfl'  # Weight-for-Length
    elif length_or_height > 110:
        file_type = 'wfh'  # Weight-for-Height
    else:
        file_type = 'wfl' if measure_type == 'l' else 'wfh'  # Choose based on length/height type

    if sex == 1:  # Boys
        file_path = f"data/{file_type}-boys-percentiles-expanded-tables.feather"
    elif sex == 2:  # Girls
        file_path = f"data/{file_type}-girls-percentiles-expanded-tables.feather"
    else:
        raise ValueError("Invalid sex. Please use 1 for male or 2 for female.")

    # Load data from Excel file
    data = pd.read_feather(file_path)
    length_or_height_data = data['Length'] if file_type == 'wfl' else data[
        'Height']

    # Create traces for Percentiles (P3, P50, P95, etc.)
    percentiles = ['P3', 'P15', 'P50', 'P85', 'P97']
    colors = ['red', 'orange', 'green', 'orange', 'red']
    labels = ['3rd', '15th', '50th', '85th', '97th']
    traces = [
        go.Scatter(x=length_or_height_data,
                   y=data[percentile],
                   mode='lines',
                   name=label,
                   line=dict(color=color),
                   showlegend=False)
        for percentile, color, label in zip(percentiles, colors, labels)
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
        dict(type='line',
             x0=length_or_height,
             y0=data['P3'].min() - 2,
             x1=length_or_height,
             y1=data['P95'].max() + 2,
             line=dict(color='gray', width=0.2, dash='dash'))
        for length_or_height in range(50, 120, 10)
    ] + [
        dict(type="line",
             x0=length_or_height_data.min(),
             y0=y,
             x1=length_or_height_data.max(),
             y1=y,
             line=dict(color="gray", width=0.2, dash="dash"))
        for y in range(5, int(data['P95'].max() + 2), 5)
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

    # Add annotations for Percentile labels
    annotations = [
        dict(x=1.001,
             y=data[percentile].iloc[-1],
             text=label,
             font=dict(color=color, size=8),
             xref="paper",
             yref="y",
             showarrow=False,
             xanchor="left")
        for percentile, label, color in zip(percentiles, labels, colors)
    ]

    # Determine axis titles
    axis_title = "Length (cm)" if file_type == 'wfl' else "Height (cm)"

    # Create layout
    layout = go.Layout(xaxis=dict(
        title=axis_title,
        range=[length_or_height_data.min(),
               length_or_height_data.max()]),
                       yaxis=dict(title="Weight (kg)"),
                       margin=dict(l=30, r=30, t=20, b=20),
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


def draw_bmi_percentile_chart_above5yr(bmi, age_months, sex):
    if sex == 1:  # Boys
        file_path = 'data/who2007/bfa-boys-perc-who2007-exp.feather'
    elif sex == 2:  # Girls
        file_path = 'data/who2007/bfa-girls-perc-who2007-exp.feather'
    else:
        raise ValueError("Invalid sex. Please use 1 for male or 2 for female.")

    # Load data from Excel file
    data = pd.read_feather(file_path)
    age_months_data = data['Month']

    # Create traces for percentile lines
    percentiles = ['P3', 'P15', 'P50', 'P85', 'P97']
    colors = ['red', 'orange', 'green', 'orange', 'red']
    labels = ['3rd', '15th', '50th', '85th', '97th']
    traces = [
        go.Scatter(x=age_months_data,
                   y=data[percentile],
                   mode='lines',
                   name=label,
                   line=dict(color=color),
                   showlegend=False)
        for percentile, color, label in zip(percentiles, colors, labels)
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

    # Add annotations for Percentile labels
    annotations = [
        dict(x=0.94,
             y=data[percentile].iloc[-1],
             text=label,
             font=dict(color=color, size=10),
             xref="paper",
             yref="y",
             showarrow=False,
             xanchor="left")
        for percentile, label, color in zip(percentiles, labels, colors)
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


def draw_wfa_percentile_chart_above5yr(weight, age_months, sex):
    if sex == 1:  # Boys
        file_path = 'data/who2007/wfa-boys-perc-who2007-exp.feather'
    elif sex == 2:  # Girls
        file_path = 'data/who2007/wfa-girls-perc-who2007-exp.feather'
    else:
        raise ValueError("Invalid sex. Please use 1 for male or 2 for female.")

    # Load data from Excel file
    data = pd.read_feather(file_path)
    age_months_data = data['Month']

    # Create traces for percentile lines
    percentiles = ['P3', 'P15', 'P50', 'P85', 'P97']
    colors = ['red', 'orange', 'green', 'orange', 'red']
    labels = ['3rd', '15th', '50th', '85th', '97th']
    traces = [
        go.Scatter(x=age_months_data,
                   y=data[percentile],
                   mode='lines',
                   name=label,
                   line=dict(color=color),
                   showlegend=False)
        for percentile, color, label in zip(percentiles, colors, labels)
    ]

    # Add the child BMI point
    traces.append(
        go.Scatter(x=[age_months],
                   y=[weight],
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

    # Add annotations for Percentile labels
    annotations = [
        dict(x=0.94,
             y=data[percentile].iloc[-1],
             text=label,
             font=dict(color=color, size=10),
             xref="paper",
             yref="y",
             showarrow=False,
             xanchor="left")
        for percentile, label, color in zip(percentiles, labels, colors)
    ]

    # Layout configuration
    layout = go.Layout(xaxis=dict(title="Age (months)",
                                  tickvals=[61, 72, 84, 96, 108, 120],
                                  ticks="inside",
                                  range=[61, 124]),
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


def draw_lhfa_percentile_chart_above5yr(adjusted_lenhei, age_months, sex):
    if sex == 1:  # Boys
        file_path = 'data/who2007/lhfa-boys-perc-who2007-exp.feather'
    elif sex == 2:  # Girls
        file_path = 'data/who2007/lhfa-girls-perc-who2007-exp.feather'
    else:
        raise ValueError("Invalid sex. Please use 1 for male or 2 for female.")

    # Load data from Excel file
    data = pd.read_feather(file_path)
    age_months_data = data['Month']

    # Create traces for percentile lines
    percentiles = ['P3', 'P15', 'P50', 'P85', 'P97']
    colors = ['red', 'orange', 'green', 'orange', 'red']
    labels = ['3rd', '15th', '50th', '85th', '97th']
    traces = [
        go.Scatter(x=age_months_data,
                   y=data[percentile],
                   mode='lines',
                   name=label,
                   line=dict(color=color),
                   showlegend=False)
        for percentile, color, label in zip(percentiles, colors, labels)
    ]

    # Add the child BMI point
    traces.append(
        go.Scatter(x=[age_months],
                   y=[adjusted_lenhei],
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

    # Add annotations for Percentile labels
    annotations = [
        dict(x=0.94,
             y=data[percentile].iloc[-1],
             text=label,
             font=dict(color=color, size=10),
             xref="paper",
             yref="y",
             showarrow=False,
             xanchor="left")
        for percentile, label, color in zip(percentiles, labels, colors)
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
