import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

@st.cache_data
def load_data():
  return pd.read_csv("ai_jobs_salaries_clean.csv")
df_test = load_data()

st.dataframe(df_test.iloc[:,:14])

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



st.markdown(
    """
    <style>
        @keyframes su {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .su{
            animation: su 0.8s cubic-bezier(0.25, 1, 0.5, 1) forwards;
        }
    </style>
    <div class="su">
        <h1 style="font-size:80px;color:#1C83E1">Welcome</h1>
        <p style="font-size: 30px;color: darkblue">On this site, I will present to you my project on...</p>
        <br><br>
        <h1 style="font-size=90px;color:#1C83E1">The AI Impact on Jobs & Salaries</h1>
        <br><br>
    </div>
    """, 
    unsafe_allow_html=True
)
with st.sidebar:
    select=st.multiselect(
        "select",
        ["Job Title","Experience Level","Employment Type"]
    )
    a = st.radio("are you ",("A","B","C"))
