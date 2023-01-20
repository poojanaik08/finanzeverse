import calendar
from datetime import datetime
import streamlit as st
import pandas as pd
import database as db

#----------------SETTINGS-------------------
def f1():
    incomes = ["Salary","Business Profit", "Stocks", "Other Income"]
    expenses = ["EMIs", "Groceries & Food", "Medicine", "House Rent", "Leisure", "Shopping"]
    savings = ["Emergency Funds","FD", "Mutual Funds", "Liquid Cash"]
    currency = "INR"

    st.title("Enter Your Details")
    #------------------DROP DOWN VALUES FOR SELECTING THE PERIOD------------------
    years = [datetime.today().year-10,datetime.today().year-9,datetime.today().year-8,datetime.today().year-7,datetime.today().year-6,datetime.today().year-5,datetime.today().year-4,datetime.today().year-3,datetime.today().year-2,datetime.today().year-1,datetime.today().year, datetime.today().year+1]
    months = list(calendar.month_name[1:])

    with st.form("entry_form", clear_on_submit=True):
        username = st.text_input(label="Username", key="username")

        col1, col2 = st.columns(2)
        col1.selectbox("Select Month:", months, key="month")
        col2.selectbox("Select Year:", years, key="year")

        "---" #divider
        st.number_input(label="Networth", min_value=0, format="%i", key="networth")
        st.markdown("###")
        with st.expander("Income"):
            for income in incomes:
                st.number_input(f"{income}:", min_value=0, format="%i", step=10, key=income)
                
        with st.expander("Expense"):    
            for expense in expenses:
                st.number_input(f"{expense}:", min_value=0, format="%i", step=10, key=expense)
        
        with st.expander("Savings"):    
            for saving in savings:
                st.number_input(f"{saving}:", min_value=0, format="%i", step=10, key=saving)

        st.markdown("###")
        savings_target = st.number_input(label="Savings Target (%)", min_value=0, format="%i",key="savings_target")
        
        "---"
        submitted = st.form_submit_button("Save Data")
        if submitted:
            period = str(st.session_state["year"]) + "_" + str(st.session_state["month"])
            incomes = {income: st.session_state[income] for income in incomes}
            expenses = {expense: st.session_state[expense] for expense in expenses}
            savings = {saving: st.session_state[saving] for saving in savings}
            
            db.insert_values(username, period, incomes, expenses, savings, savings_target) 
            st.success("Data Saved")

        st.markdown("###")
    st.header("OR, Upload an existing CSV file")
    data_file = st.file_uploader("Upload CSV", type=['csv'])
    if st.button("Upload Data"):
        if data_file is not None:
            df = pd.read_csv(data_file, encoding= 'unicode_escape')
            