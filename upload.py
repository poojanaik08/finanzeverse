import streamlit as st
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

def upload():
    menu = ["File Upload","Dashboard", "Loan Planner", "Budget Planner"]
    choice = st.sidebar.selectbox("Menu", menu)
    if choice == "File Upload":
        data_file = st.file_uploader("Upload CSV", type=['csv'])
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
            st.subheader("Metrics")

            st.markdown("###")
            st.subheader("How do I spend?")
            years = st.multiselect("Select Years: ", options=st.session_state.expense_df["Year"].unique(), default=st.session_state.expense_df["Year"].unique())
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
                color=pt.index,
            )
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig)
        
        with col2:
            #line charts
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