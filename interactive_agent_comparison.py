import pandas as pd
import plotly.express as px


CSV_FILE = "results/agent_evaluation.csv"

# Loading Data 
df = pd.read_csv(CSV_FILE)

# Calculate the success rate
df["success_rate"] = df["success"] / (df["success"] + df["fire"] + df["stuck"])

# Creating a new column for grid + fire spread
df["scenario"] = df["grid"] + " | fire=" + df["fire_spread"].astype(str)

# Plot Interactive Bar Chart using plotly
fig = px.bar(
    df,
    x="scenario",
    y="success_rate",
    color="agent",
    barmode="group",
    title="Agent Success Rate Comparison across Grid Sizes & Fire Spread",
    labels={"scenario": "Environment (Grid + Fire Spread)", "success_rate": "Success Rate"},
    
)

fig.update_traces(textposition='outside')
fig.update_layout(
    xaxis_tickangle=-45,
    yaxis=dict(range=[0, 1]),
    plot_bgcolor='white'
)

fig.show()
