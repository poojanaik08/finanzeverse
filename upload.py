import streamlit as st
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from PIL import Image

image = Image.open("images/finance_template.png")

def upload():
    with open('style/upload.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    menu = ["File Upload","Dashboard", "Loan Planner", "Budget Planner"]
    choice = st.sidebar.selectbox("Menu", menu)
    if choice == "File Upload":
        data_file = st.file_uploader("Upload CSV", type=['csv'])
        #template
        st.markdown("###")
        with st.expander(label="CSV Template"):
            st.image(image=image, width=1000)
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
        col1, col2 = st.columns(2, gap="large")
        with col1:
            total_income = st.session_state.income_df["Value"].sum()
            total_expense = st.session_state.expense_df["Value"].sum()
            total_savings = total_income - total_expense
            expense_per = total_expense/total_income
            saving_per = total_savings/total_income

            st.subheader("Metrics")
            total_income = int(total_income)
            total_expense = int(total_expense)
            total_savings = int(total_savings)
            
            subcol1, subcol2, subcol3 = st.columns(3)
            with subcol1:
                st.metric("Total Income", f"{total_income}")
            with subcol2:
                st.metric("Total Expenditure", f"{total_expense}")
            with subcol3:
                st.metric("Total Savings", f"{total_savings}")
            
            
            expense_per = total_expense/total_income
            saving_per = total_savings/total_income
            expense_per = expense_per*100
            expense_per = round(expense_per, 2)
            saving_per = saving_per*100
            saving_per = round(saving_per, 2)
            sub2col1, sub2col2 = st.columns(2)
            with sub2col1:
                st.metric("Expense Percent", f"{expense_per}%")
            with sub2col2:
                st.metric("Savings Percent", f"{saving_per}%")

            st.markdown("###")
            st.subheader("How do I spend?")
            years = st.multiselect("Select Years: ", options=st.session_state.expense_df["Year"].unique(), default=st.session_state.expense_df["Year"].unique(),key="expense_key")
            expense_df_selection = st.session_state.expense_df.query(
                "Year == @years"
            )
            pt = expense_df_selection.pivot_table(
                values="Value",
                index="Component",
                aggfunc="sum",
                fill_value=0
            )
            pt.reset_index().sort_values("Value", ascending=True)

            fig = px.bar(
                pt,
                y= pt.index,
                x="Value",
                template='plotly_white', 
                hover_data= ["Value"],
                hover_name="Value",
                height=350,
                color=pt.index,
            )
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig)

            st.subheader("How do I earn?")
            years1 = st.multiselect("Select Years: ", options=st.session_state.income_df["Year"].unique(), default=st.session_state.income_df["Year"].unique(),key="income_key")
            income_df_selection = st.session_state.income_df.query(
                "Year == @years1"
            )
            pt2 = income_df_selection.pivot_table(
                values="Value",
                index="Component",
                aggfunc="sum",
                fill_value=0
            )
            pt2.reset_index().sort_values("Value", ascending=True)

            fig4 = px.bar(
                pt2,
                y= pt2.index,
                x="Value",
                template='plotly_white', 
                hover_data= ["Value"],
                hover_name="Value",
                height=350,
                color=pt2.index,
            )
            fig4.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig4)

        
        with col2:
            #line charts
            st.subheader("Income and Expense")
            component = st.selectbox(label="Select Income Category", options=st.session_state.income_df["Component"].unique())
            line_income_df_selection = st.session_state.income_df.query(
                "Component == @component"
            )
            component_expense = st.selectbox(label="Select Expense Category", options=st.session_state.expense_df["Component"].unique())
            line_expense_df_selection = st.session_state.expense_df.query(
                "Component == @component_expense"
            )

            fig2 = px.line(
                data_frame=line_income_df_selection,
                y = "Value",
                x = "Date",
                hover_data=["Value"],
                height=600,
                width= 720,
                color="Component",
            )
            fig2.add_scatter(
                y = line_expense_df_selection["Value"],
                x = line_expense_df_selection["Date"],
                mode='lines',
                hovertext="Value",
                name=component_expense,
            )
            fig2.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
            )
            fig2.update_xaxes(tickangle=45)
            st.plotly_chart(fig2)

            st.markdown("###")

            st.subheader("Savings Breakdown")
            fig3 = px.pie(
            data_frame= st.session_state.savings_df,
            hole=0.5,
            labels = "Component",
            names= "Component",
            )
            fig3.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
            )
            st.plotly_chart(fig3)