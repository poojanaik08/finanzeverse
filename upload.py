import streamlit as st
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

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
        with open('style/upload.css') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
        col1, col2 = st.columns(2, gap="large")
        with col1:
            total_income = st.session_state.income_df["Value"].sum()
            total_expense = st.session_state.expense_df["Value"].sum()
            #total_savings = total_income - total_expense
            total_savings = st.session_state.savings_df["Value"].sum()
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

            st.markdown("###")
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
                width= 685,
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
            width=685
            )
            fig3.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
            )
            st.plotly_chart(fig3)

    if choice == "Loan Planner":
        st.title("Loan Planner")

        # Function to calculate loan data
        # Calculate monthly interest rate

        col1, col2, col3 = st.columns(3)
        with col1:
            principal = st.number_input('Principal Amount',min_value=0, value=100000, step=1)
        with col2:
            interes_rate = st.number_input('Interest Rate', min_value=0.000, value=0.050, step=0.001)
        with col3:
            term = st.number_input('Term (in months)', min_value=0, value=120, step=1)

        monthly_rate = interes_rate / 12
        # Calculate monthly payment using the formula assuming linear payments
        monthly_payment = (principal * monthly_rate) / (1 - (1 + monthly_rate) ** (-term))
        # Initialize remaining principal and total amount
        remaining_principal = principal
        total_amount = 0

        # Initialize data frame
        data = pd.DataFrame()

        # Iterate over loan term and calculate some values for each month
        for month in range(1, term + 1):
            # Calculate interest amount
            interest_amount = remaining_principal * monthly_rate
            # Calculate principal amount
            principal_amount = monthly_payment - interest_amount
            # Update remaining principal and total amount
            remaining_principal = remaining_principal - principal_amount
            total_amount = total_amount + monthly_payment
            # Print the result
            data_one_iter = pd.DataFrame({
                'Month': [month],
                'Monthly Payment': [monthly_payment],
                'Interest Amount': [interest_amount],
                'Remaining Principal': [remaining_principal],
                'Total Amount': [total_amount]})
            
            data = pd.concat([data, data_one_iter], ignore_index=True)
        data['Interest Monthly Ratio'] = data['Interest Amount'] / data['Monthly Payment']

        # create a line graph with x axis as month and y axis as remaining principal
        fig_remining_principal = px.line(data, x='Month', y='Remaining Principal')
        fig_interest_payed = px.line(data, x='Month', y=['Interest Amount', 'Monthly Payment'], width=900)
        fig_interest_payment_ratio = px.line(data, x='Month', y='Interest Monthly Ratio')

        fig_remining_principal.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',   
        )
        
        fig_interest_payed .update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)', 
            yaxis_title="Value",
        )
        
        fig_interest_payment_ratio.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',   
        )
        
        fig_remining_principal.for_each_xaxis(lambda x: x.update(showgrid=False))
        fig_remining_principal.for_each_yaxis(lambda x: x.update(showgrid=False))
        
        fig_interest_payed.for_each_xaxis(lambda x: x.update(showgrid=False))
        fig_interest_payed.for_each_yaxis(lambda x: x.update(showgrid=False))
        
        fig_interest_payment_ratio.for_each_xaxis(lambda x: x.update(showgrid=False))
        fig_interest_payment_ratio.for_each_yaxis(lambda x: x.update(showgrid=False))

        month_pay = round(data['Monthly Payment'][0])
        tot_amount = round(total_amount)
        st.subheader(f'Monthly Installment: {month_pay}')
        st.subheader(f'Total amount payed at the end of the loan period: {tot_amount}')

        show_brake_down = st.checkbox('Show loan breakdown per month')
        if show_brake_down:
            st.markdown('## Loan breakdown per month')
            st.dataframe(data, width=1500)
            # create download button with streamlit, donload the data frame as csv file
            st.download_button(label='Download data', data=data.to_csv(index=False), file_name='loan_breakdown.csv',
                            mime='text/csv')
 
        figcol1, figcol2 = st.columns(2)
        with figcol1:
            st.markdown('## Remaining principal over time')
            st.plotly_chart(fig_remining_principal, theme=None)
        with figcol2:
            st.markdown('## Monthly payment instalment over time')
            st.plotly_chart(fig_interest_payment_ratio, theme=None)

        st.markdown('## Monyhly installment breakdown per month over time')
        st.plotly_chart(fig_interest_payed, theme=None, use_container_width=True)



