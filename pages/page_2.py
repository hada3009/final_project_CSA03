import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

@st.cache_data
def load_data():
  return pd.read_csv("ai_jobs_salaries_clean.csv")
df = load_data()

with st.sidebar:
    a=st.selectbox("employee residence",["ALL"] + sorted(df["employee_residence"].unique().tolist()))
    b=st.selectbox("experience",sorted(df["experience_level"].unique().tolist()))
    c=st.selectbox("job title",sorted(df["job_title"].unique().tolist()))
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
if d != "ALL":
  df_test = df_test[df_test["company_size"] == d]

df_test = df_test.reset_index(drop=True)

e=st.number_input("your salary in us dollar")

avg_salary = df_test['salary_in_usd'].mean()
aes=df_test['ai_exposure_score'].mean()*100
job_count = len(df_test)

col1,col2,col3=st.columns(3,gap="small")

with col1:
    st.metric(f"Average salary({a})",f"${avg_salary:,.0f} USD",f"{(avg_salary-e):,.0f} compared to yours")
with col2:
    st.metric("Analysed profile",f"{job_count:,d}")
with col3:
    st.metric("Experience level",b)
if aes> 75:
    st.error(f"{aes:.1f}%, high exposure job")
elif 40 <=aes<= 75:
    st.warning(f"{aes:.1f}%, moderate exposure job")
else:
    st.success(f"{aes:.1f}%, low exposure job")

X = pd.get_dummies(df[['experience_level','ai_exposure_score']], columns=['experience_level'], drop_first=True)
y = df['salary_in_usd']

model = LinearRegression()
model.fit(X, y)

i = pd.DataFrame(0,[0],X.columns)

i['ai_exposure_score'] = aes / 100
if f"experience_level_{b}" in i.columns:
    i[f"experience_level_{b}"] = 1

pred = model.predict(i)[0]

col4, col5 = st.columns(2)
with col4:
    st.metric(f"Predicted Salary ({b})",f"${pred:,.0f} USD")
with col5:
    st.metric("Prediction vs Your Current Salary",f"${(pred - e):,.0f} USD",f"{((pred - e)/e*100):.1f}%")

fig, ax = plt.subplots(figsize=(10, 4))
sns.kdeplot(df['salary_in_usd'], ax=ax)
ax.axvline(pred, color="red")
ax.set_title(f"Salary Distribution for {c} ({b})")
ax.set_xlabel("Salary in USD")
ax.set_ylabel("Density")
st.pyplot(fig)

yearly_avg = df_test.groupby('work_year')['salary_in_usd'].mean().reset_index()
st.line_chart(yearly_avg,x='work_year',y='salary_in_usd')