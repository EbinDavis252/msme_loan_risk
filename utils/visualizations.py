import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def donut_chart_risk(df):
    counts = df['Predicted_Risk'].value_counts()
    labels = counts.index
    sizes = counts.values

    fig, ax = plt.subplots()
    wedges, texts, autotexts = ax.pie(
        sizes,
        labels=labels,
        autopct='%1.1f%%',
        startangle=90,
        colors=['#36A2EB', '#FF6384'],
        wedgeprops=dict(width=0.4)
    )
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
