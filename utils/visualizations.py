import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import streamlit as st

def pie_chart_risk_distribution(df):
    fig, ax = plt.subplots()
    sizes = df['Risk_Prediction'].value_counts().sort_index()

    # Generate labels based on actual data
    labels = [f'Safe (0)' if i == 0 else f'Risky (1)' for i in sizes.index]

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
    fig, ax = plt.subplots()

    if 'Risk_Prediction' not in df.columns or 'LoanAmount' not in df.columns:
        st.warning("Required columns not found: 'Risk_Prediction' and 'LoanAmount'")
        return fig

    sns.boxplot(x='Risk_Prediction', y='LoanAmount', data=df, ax=ax, palette='Set2')
    ax.set_title('Loan Amount Distribution by Risk Category')
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
