import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

st.markdown('<p style="font-size:30px">1. Is my career track high-paying but at high risk of being automated?</p>',unsafe_allow_html=True)

with st.sidebar:
    a=st.selectbox("region",['US','CA'])

df_test=pd.read_csv("ai_jobs_salaries_clean.csv")
st.dataframe(df_test.groupby('employee_residence').get_group(a))

isco_exposure_mapping = {
    "Software and applications developers": 0.85,
    "Mathematicians, actuaries and statisticians": 0.76,
    "Business services and administration managers": 0.55,
    "Information and communications technology service managers": 0.45,
    "Physical and earth science professionals": 0.35,
    "Other / Unclassified": 0.50
}
df_test['isco_group_hint'] = df_test['isco_group_hint'].fillna("Other / Unclassified")
df_test['ai_exposure_score'] = df_test['isco_group_hint'].map(isco_exposure_mapping)

st.dataframe(df_test.groupby('isco_group_hint')['ai_exposure_score'].first().reset_index())

salary_cutoff = df_test["salary_in_usd"].median()
risk_cutoff = 0.50

fig, ax = plt.subplots(figsize=(10, 6.5))

conditions = [
        (df_test["salary_in_usd"] >= salary_cutoff)&(df_test["ai_exposure_score"] < risk_cutoff),
        (df_test["salary_in_usd"] >= salary_cutoff)&(df_test["ai_exposure_score"] >= risk_cutoff),
        (df_test["salary_in_usd"] < salary_cutoff)&(df_test["ai_exposure_score"] < risk_cutoff),
        (df_test["salary_in_usd"] < salary_cutoff)&(df_test["ai_exposure_score"] >= risk_cutoff)
]
choices = ["high salaries, low risks", "high salaries, high risks", "low salaries, low risks", "low salaries, high risks"]
df_test["select"] = np.select(conditions, choices, default="Unclassified")

palette_colors = {
    "high salaries, low risks": "green",
    "high salaries, high risks": "blue",
    "low salaries, low risks": "yellow",
    "low salaries, high risks": "red"
}
max_y = df_test["salary_in_usd"].max() * 1.15
max_x = 1.05
ax.fill_between([0, risk_cutoff], salary_cutoff, max_y, color="green", alpha=0.08, zorder=0)
ax.fill_between([risk_cutoff, max_x], salary_cutoff, max_y, color="blue", alpha=0.08, zorder=0)
ax.fill_between([0, risk_cutoff], 0, salary_cutoff, color="yellow", alpha=0.08, zorder=0)
ax.fill_between([risk_cutoff, max_x], 0, salary_cutoff, color="red", alpha=0.08, zorder=0)

ax.axhline(y=salary_cutoff, color="gray", linewidth=1.2, alpha=0.7, zorder=0)
ax.axvline(x=risk_cutoff, color="gray", linewidth=1.2, alpha=0.7, zorder=0)

sns.scatterplot(
    data=df_test,
    x="ai_exposure_score",
    y="salary_in_usd",
    hue="select",
    palette=palette_colors,
    s=100,
    edgecolor="black",
    ax=ax,
)
ax.set_xlabel("AI Exposure Risk Index Score", fontsize=11, labelpad=10)
ax.set_ylabel("Annual Compensation (USD)", fontsize=11, labelpad=10)
ax.xaxis.set_major_formatter(lambda x, pos: f"{x*100:.0f}%")
ax.yaxis.set_major_formatter(lambda y, pos: f"${y:,.0f}")
ax.set_xlim(0, max_x)
ax.set_ylim(0, max_y)

plt.tight_layout()
st.pyplot(fig)