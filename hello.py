from preswald import text, plotly, connect, get_df, table
import pandas as pd
import plotly.express as px

text("# Welcome to Preswald!")
text("This is your first app. 🎉")

# Load the CSV
connect()
df = pd.read_csv('data/sample_first100.csv')

# Create a scatter plot
fig = px.scatter(df, x='Profit', y='Sales', text='Category',
                 title='Profit vs. Sales by Category',
                 labels={'Profit': 'Profit', 'Sales': 'Sales'})

# Add labels for each point
fig.update_traces(textposition='top center', marker=dict(size=12, color='lightblue'))

# Style the plot
fig.update_layout(template='plotly_white')

# Show the plot
plotly(fig)

# Show the data
table(df)
