import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def pie_chart_risk_distribution(df):
    fig, ax = plt.subplots()
    labels = ['Safe (0)', 'Risky (1)']
    sizes = df['Risk_Prediction'].value_counts().sort_index()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=['#00b894','#d63031'], startangle=140)
    ax.axis('equal')
    return fig

def bar_chart_by_business_type(df):
    fig, ax = plt.subplots(figsize=(8, 4))
    avg_risk = df.groupby('Business_Type')['Risk_Probability (%)'].mean().sort_values()
    avg_risk.plot(kind='barh', color='skyblue', ax=ax)
    ax.set_xlabel("Avg Risk Probability (%)")
    ax.set_title("Avg Risk by Business Type")
    return fig

def boxplot_loan_risk(df):
    fig, ax = plt.subplots(figsize=(6,4))
    sns.boxplot(x='Risk_Prediction', y='Loan_Amount_Requested', data=df, ax=ax, palette='Set2')
    ax.set_title("Loan Amount vs Risk Prediction")
    ax.set_xticklabels(['Safe', 'Risky'])
    return fig

def histogram_risk_prob(df):
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.histplot(df['Risk_Probability (%)'], bins=10, kde=True, ax=ax, color='orange')
    ax.set_title("Risk Probability Distribution")
    return fig

def heatmap_correlation(df):
    fig, ax = plt.subplots(figsize=(8, 5))
    num_df = df.select_dtypes(include=['float64', 'int64'])
    corr = num_df.corr()
    sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
    ax.set_title("Feature Correlation Matrix")
    return fig

def countplot_location(df):
    fig, ax = plt.subplots(figsize=(6,4))
    sns.countplot(x='Location', hue='Risk_Prediction', data=df, palette='Set1', ax=ax)
    ax.set_title("Risk by Location")
    return fig
