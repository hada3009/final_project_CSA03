import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.markdown('<p style="font-size:30px">1. Is your career track high-paying but at high risk of being automated?</p>',unsafe_allow_html=True)

@st.cache_data
def load_data():
  return pd.read_csv("ai_jobs_salaries_clean.csv")
df = load_data()
with st.sidebar:
    a=st.selectbox("employee residence",["ALL"] + sorted(df["employee_residence"].unique().tolist()))
    b=st.selectbox("experience",["ALL"] + sorted(df["experience_level"].unique().tolist()))
    c=st.selectbox("job title",["ALL"] + sorted(df["job_title"].unique().tolist()))
    d=st.radio("Company Size", ["ALL","S", "M", "L"])

isco_exposure_mapping = {
    "Software and applications developers": 0.85,
    "Mathematicians, actuaries and statisticians": 0.76,
    "Business services and administration managers": 0.55,
    "Information and communications technology service managers": 0.45,
    "Physical and earth science professionals": 0.35,
    "Other / Unclassified": 0.50
}
df['isco_group_hint'] = df['isco_group_hint'].fillna("Other / Unclassified")
df['ai_exposure_score'] = df['isco_group_hint'].map(isco_exposure_mapping)

df_test = df.copy()

if a != "ALL":
  df_test = df_test[df_test["employee_residence"] == a]
if b != "ALL":
  df_test = df_test[df_test["experience_level"] == b]
if c != "ALL":
  df_test = df_test[df_test["job_title"] == c]
if d != "ALL":
  df_test = df_test[df_test["company_size"] == d]

df_test = df_test.reset_index(drop=True)
st.dataframe(df_test.iloc[:,:14])

st.dataframe(df.groupby('isco_group_hint')['ai_exposure_score'].first().reset_index())
salary_cutoff = df_test["salary_in_usd"].median()

fig, ax = plt.subplots(figsize=(10, 6.5))

conditions = [
        (df_test["salary_in_usd"] >= salary_cutoff)&(df_test["ai_exposure_score"] < 0.5),
        (df_test["salary_in_usd"] >= salary_cutoff)&(df_test["ai_exposure_score"] >= 0.5),
        (df_test["salary_in_usd"] < salary_cutoff)&(df_test["ai_exposure_score"] < 0.5),
        (df_test["salary_in_usd"] < salary_cutoff)&(df_test["ai_exposure_score"] >= 0.5)
]
choices = ["high salaries, low risks", "high salaries, high risks", "low salaries, low risks", "low salaries, high risks"]
df_test["select"] = np.select(conditions, choices, default="Unclassified")

colors = {
    "high salaries, low risks": "green",
    "high salaries, high risks": "blue",
    "low salaries, low risks": "yellow",
    "low salaries, high risks": "red"
}
max_y = df_test["salary_in_usd"].max() * 1.15
ax.fill_between([0, 0.5], salary_cutoff, max_y, color="green", alpha=0.1)
ax.fill_between([0.5, 1], salary_cutoff, max_y, color="blue", alpha=0.1)
ax.fill_between([0, 0.5], 0, salary_cutoff, color="yellow", alpha=0.1)
ax.fill_between([0.5, 1], 0, salary_cutoff, color="red", alpha=0.1)
sns.scatterplot(
    data=df_test,
    x="ai_exposure_score",
    y="salary_in_usd",
    hue="select",
    palette=colors,
    s=140,
    edgecolor="black",
    ax=ax,
)
ax.set_xlabel("AI Exposure Risk Index Score")
ax.set_ylabel("Annual Compensation (USD)")
ax.set_xlim(0,1)
ax.set_ylim(0, max_y)

plt.tight_layout()
st.pyplot(fig)