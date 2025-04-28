from preswald import text, plotly, connect, get_df, table
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

text('# Assortment Overview Dashboard')

# Load the CSV
df = pd.read_csv('data/sample_first100.csv')
table(df, title='Original Data')

# 1. Sales & Margin Performance by Sub Category (Scatter Plot)
if 'Profit' in df.columns and 'Sales' in df.columns and 'Sub-Category' in df.columns:
    df['Margin Contrib %'] = df['Profit'] / df['Sales']
    df['Net Sales Contrib %'] = df['Sales'] / df['Sales'].sum()
    fig1 = px.scatter(
        df,
        x='Margin Contrib %',
        y='Net Sales Contrib %',
        color='Sub-Category',
        size='Sales',
        hover_name='Sub-Category',
        title='Sales & Margin Performance by Sub Category'
    )
    plotly(fig1)
else:
    text('Missing columns for Sales & Margin Performance by Sub Category')

# 2. Pvt Vs National Brand Performance by Sub Category (Bar Chart)
# Using Category as a proxy for Brand Type (since Brand Type is not present)
if 'Sales' in df.columns and 'Sub-Category' in df.columns and 'Category' in df.columns:
    fig2 = px.bar(
        df,
        x='Sales',
        y='Sub-Category',
        color='Category',
        orientation='h',
        barmode='group',
        title='Category Performance by Sub Category'
    )
    plotly(fig2)
else:
    text('Missing columns for Category Performance by Sub Category')

# 3. Seasonal Trend by Sub Category (Line Chart)
# Using Order Date as a proxy for week/date
if 'Order Date' in df.columns and 'Sales' in df.columns and 'Sub-Category' in df.columns:
    # Try to parse dates
    df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')
    print(df['Order Date'].head())
    print('Number of NaT in Order Date:', df['Order Date'].isna().sum())
    # Drop rows with invalid dates
    df_trend = df.dropna(subset=['Order Date'])
    # Group by month and sub-category
    df_trend = df_trend.groupby([pd.Grouper(key='Order Date', freq='M'), 'Sub-Category'])['Sales'].sum().reset_index()
    print(df_trend.head())
    print('df_trend shape:', df_trend.shape)
    if not df_trend.empty:
        fig3 = px.line(
            df_trend,
            x='Order Date',
            y='Sales',
            color='Sub-Category',
            title='Seasonal Trend by Sub Category (Monthly)'
        )
        plotly(fig3)
    else:
        text('No data available for Seasonal Trend by Sub Category after grouping.')
else:
    text('Missing columns for Seasonal Trend by Sub Category')

# 4. Top 80% Contributing Products by Sales (Pareto Chart)
if 'Product Name' in df.columns and 'Sales' in df.columns:
    df_sorted = df.sort_values('Sales', ascending=False)
    df_sorted['Cumulative Sales %'] = df_sorted['Sales'].cumsum() / df_sorted['Sales'].sum() * 100
    fig4 = go.Figure()
    fig4.add_bar(x=df_sorted['Product Name'], y=df_sorted['Sales'], name='Net Sales Units')
    fig4.add_scatter(x=df_sorted['Product Name'], y=df_sorted['Cumulative Sales %'], name='Cumulative Sales %', yaxis='y2')
    fig4.update_layout(
        title='Top 80% Contributing Products by Sales',
        yaxis=dict(title='Net Sales Units'),
        yaxis2=dict(title='Cumulative Sales %', overlaying='y', side='right'),
        xaxis_tickangle=-45
    )
    plotly(fig4)
else:
    text('Missing columns for Top 80% Contributing Products by Sales')
