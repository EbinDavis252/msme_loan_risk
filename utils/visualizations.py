import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def pie_chart_risk(df):
    counts = df['Risk_Prediction'].value_counts().sort_index()

    # Ensure both classes (0 and 1) are represented
    counts = counts.reindex([0, 1], fill_value=0)

    labels = ['Low Risk (0)', 'High Risk (1)']
    colors = ['#36A2EB', '#FF6384']

    fig, ax = plt.subplots()
    ax.pie(counts, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
    ax.axis('equal')
    return fig

def bar_chart_by_business_type(df):
    grouped = df.groupby('Business_Type')['Risk_Probability (%)'].mean().sort_values()
    fig, ax = plt.subplots(figsize=(10,5))
    sns.barplot(x=grouped.index, y=grouped.values, ax=ax, palette='coolwarm')
    ax.set_ylabel("Avg Risk Probability (%)")
    ax.set_title("Average Risk by Business Type")
    plt.xticks(rotation=45)
    return fig
