import streamlit as st
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

from dashboard import dashboard
from loanplanner import loanplanner
from budgetplanner import budgetplanner

def upload():
    # with open('style/upload.css') as f:
    #     st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    menu = ["File Upload","Dashboard", "Loan Planner", "Budget Planner"]
    choice = st.sidebar.selectbox("Menu", menu)
    if choice == "File Upload":
        data_file = st.file_uploader("Upload CSV", type=['csv'])
        #template
        st.markdown("###")
        with st.expander(label="CSV Template"):
            #st.image(image=image, width=1000)
            csv_template = pd.DataFrame(
            data={"Type":["Income","Income", "Expenses", "Expenses", "Savings"],
            "Component": ["Income1", "Income2", "Expense1", "Expense2", "Savings1"],
            "Date":["01/01/2021", "10/08/2022", "21/03/2022", "19/05/2022", "01/02/2023"],
            "Value": [30000, 25000, 4000, 15000, 10000],
            "Year": [2021, 2022, 2022, 2022, 2023]
            })
            st.table(data=csv_template)

        if data_file is not None:
            df = pd.read_csv(data_file, index_col=False, encoding= 'utf-8-sig')
            expense_df = df.loc[df["Type"]=="Expenses"]
            income_df = df.loc[df["Type"]=="Income"]
            savings_df = df.loc[df["Type"]=="Savings"]
            if 'df' not in st.session_state:
                st.session_state.df = df

            if 'expense_df' not in st.session_state:
                st.session_state.expense_df = expense_df

            if 'income_df' not in st.session_state:
                st.session_state.income_df = income_df

            if 'savings_df' not in st.session_state:
                st.session_state.savings_df = savings_df

    if choice == "Dashboard":
        dashboard()
        
    if choice == "Loan Planner":
        loanplanner()
    
    if choice == "Budget Planner":
        budgetplanner()
