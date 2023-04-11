import streamlit as st
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

import pickle
model = pickle.load(open('./Model/ML_Model.pkl', 'rb'))

def loanplanner():
    loan_select_box = st.selectbox(label="Choose:", options=["Plan your loans", "Check your loan eligibility status"])
    st.markdown("---")
    if(loan_select_box == "Plan your loans"):
        st.title("Amortized Loan: Paying Back a Fixed Amount Periodically")

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
        st.markdown(f'### Monthly Installment: <span style="color:#DA70D6">{month_pay}</span>', unsafe_allow_html=True)
        st.markdown(f'### Total amount payed at the end of the loan period: <span style="color:#DA70D6">{tot_amount}</span>', unsafe_allow_html=True)

        show_brake_down = st.checkbox('Show loan breakdown per month')
        if show_brake_down:
            st.markdown('## Loan breakdown per month')
            st.dataframe(data, width=1500)
            # create download button with streamlit, donload the data frame as csv file
            st.download_button(label='Download data', data=data.to_csv(index=False), file_name='loan_breakdown.csv',
                            mime='text/csv')
            
        st.markdown("---")

        figcol1, figcol2 = st.columns(2)
        with figcol1:
            st.markdown('### Remaining principal over time')
            st.plotly_chart(fig_remining_principal, theme=None)
        with figcol2:
            st.markdown('### Monthly payment instalment over time')
            st.plotly_chart(fig_interest_payment_ratio, theme=None)

        st.markdown('### Monyhly installment breakdown per month over time')
        st.plotly_chart(fig_interest_payed, theme=None, use_container_width=True)

        st.markdown("###")  
        st.markdown("###")

        st.markdown("---")
        st.header("Balloon Payment Loan: Paying Back a Lump Sum Due at Maturity")

        with st.form(key="balloonLoan", clear_on_submit=True):
            formcol1, formcol2 = st.columns(2)
            with formcol1:
                A = st.number_input("Loan Amount", format="%d", value=200000)
                i = st.number_input("Interest Rate", format="%d", value=7)
            
            with formcol2:
                n = st.number_input("Amortization period (in months)", format="%d", value=60)
                nb = st.number_input("Balloon Payment After (in months)", format="%d", value=24)
            
            calculate = st.form_submit_button(label="Calculate")

        #monthly payment
        i = i / 100
        i = i/12
        pmt = (A * i * (1+i)**n) / ((1+i)**n - 1)

        #balloon payment
        B = (A * (1+i)**nb) - pmt / i * ((1+i)**nb - 1)

        p = pmt*60 + B
        p = round(p ,2)
        total_monthly_pay = pmt*60
        total_monthly_pay = round(total_monthly_pay,2)
        pmt = round(pmt,2)
        B = round(B, 2)
        interest = p - A
        interest = round(interest ,2)

        if calculate:
            st.markdown(f"#### Your fixed monthly payment is Rs. {pmt} in the first {nb/12} years, and then your last balloon payment will be Rs. {B}.")
            st.markdown(f"#### Thus, your total repayment amount is Rs. {p}, from which the total monthly payment is Rs. {total_monthly_pay}, including a total interest payment of Rs. {interest}.")
    
    else:
        st.title("Loan Eligibility Status")

        ## For gender
        gen_display = ('Female','Male')
        gen_options = list(range(len(gen_display)))
        gen = st.selectbox("Gender",gen_options, format_func=lambda x: gen_display[x])

        ## For Marital Status
        mar_display = ('No','Yes')
        mar_options = list(range(len(mar_display)))
        mar = st.selectbox("Marital Status", mar_options, format_func=lambda x: mar_display[x])

        ## No of dependets
        dep_display = ('No','One','Two','More than Two')
        dep_options = list(range(len(dep_display)))
        dep = st.selectbox("Dependents",  dep_options, format_func=lambda x: dep_display[x])

        ## For edu
        edu_display = ('Not Graduate','Graduate')
        edu_options = list(range(len(edu_display)))
        edu = st.selectbox("Education",edu_options, format_func=lambda x: edu_display[x])

        ## For emp status
        emp_display = ('No','Yes')
        emp_options = list(range(len(emp_display)))
        emp = st.selectbox("Self Employed",emp_options, format_func=lambda x: emp_display[x])

        ## For Property status
        prop_display = ('Rural','Semi-Urban','Urban')
        prop_options = list(range(len(prop_display)))
        prop = st.selectbox("Property Area",prop_options, format_func=lambda x: prop_display[x])

        ## For Credit Score
        cred_display = ('Between 300 to 500','Above 500')
        cred_options = list(range(len(cred_display)))
        cred = st.selectbox("CIBIL Score",cred_options, format_func=lambda x: cred_display[x])

        ## Applicant Monthly Income
        mon_income_rup = st.number_input("Applicant's Income",value=0)
        mon_income = mon_income_rup / 84.15

        ## Co-Applicant Monthly Income
        co_mon_income_rup = st.number_input("Co-Applicant's Income",value=0)
        co_mon_income = co_mon_income_rup /84.15

        ## Loan AMount
        loan_amt_rup = st.number_input("Loan Amount",value=0)
        loan_amt = loan_amt_rup / 84.15

        ## loan duration
        dur_display = ['2 Month','6 Month','8 Month','1 Year','16 Month']
        dur_options = range(len(dur_display))
        dur = st.selectbox("Loan Duration",dur_options, format_func=lambda x: dur_display[x])

        if st.button("Submit"):
            duration = 0
            if dur == 0:
                duration = 60
            if dur == 1:
                duration = 180
            if dur == 2:
                duration = 240
            if dur == 3:
                duration = 360
            if dur == 4:
                duration = 480
            features = [[gen, mar, dep, edu, emp, mon_income, co_mon_income, loan_amt, duration, cred, prop]]
            print(features)
            prediction = model.predict(features)
            lc = [str(i) for i in prediction]
            ans = int("".join(lc))
            if ans == 0:
                st.error(
                    'You are not eligible for a loan'
                )
            else:
                st.success(
                    'You are eligible for a loan!'
                )
