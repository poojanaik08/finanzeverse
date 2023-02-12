import streamlit as st
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

def loanplanner():
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