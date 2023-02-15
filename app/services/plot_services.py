import plotly.graph_objects as go

# Funtion that, given a record and the x and y axis, returns a plotly figure
def plot(record, x_axis, y_axis, mode='lines+markers'):
    # Get the data from the record
    content = record['content']
    # The content is a list of dictionaries, each dictionary is a row of the table
    x = []
    y = []
    for data in content:
        x.append(data[x_axis])
        y.append(data[y_axis])
    # Check if y can be a list of numbers and convert it to a list of numbers
    try:
        y = list(map(float, y))
    except ValueError:
        pass
    # Create a figure
    fig = go.Figure()
    # Add a scatter plot
    fig.add_trace(go.Scatter(x=x, y=y, mode=mode))
    # fig.show()
    # Return the figure
    html_fig = fig.to_html(full_html=False)
    return html_fig
