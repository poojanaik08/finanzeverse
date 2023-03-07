import streamlit as st
import plotly.express as px
import pandas as pd
import streamlit.components.v1 as components
import numpy as np

def budgetplanner():
    total_income = st.session_state.income_df["Value"].sum()
    total_expense = st.session_state.expense_df["Value"].sum()
    #total_savings = total_income - total_expense
    total_savings = st.session_state.savings_df["Value"].sum()
    # expense_per = total_expense/total_income
    # saving_per = total_savings/total_income

    st.title("Your Tax Status:")
    total_income = int(total_income)
    total_expense = int(total_expense)
    total_savings = int(total_savings)
    tax = calculate_income_tax(total_income)					
    tax = int(tax)

    mcol1, mcol2 = st.columns(2)
    mcol1.markdown(f"""
        <div style="background-color:#4827a2;padding:5px;border-radius:10px;width:500px;text-align:center;padding-top:20px">
        <p style="font-size:30px;"><b>Total Income</b> <br>{total_income}</p>
        </div>
        """, unsafe_allow_html=True)
    
    mcol2.markdown(f"""
        <div style="background-color:#4827a2;padding:5px;border-radius:10px;width:500px;text-align:center;padding-top:20px">
        <p style="font-size:30px;"><b>Total tax applicable is</b> <br>{tax}</p>
        </div>
        """, unsafe_allow_html=True)
    
	
    st.markdown("---")
    st.title("Calculate The CAGR")
    with st.expander(label="Know More About CAGR"):
        st.write("CAGR (Compound Annual Growth Rate) measures your investments' average annual growth over a given period. When calculating CAGR, profits are assumed to be reinvested at the end of each year of the time horizon. In most cases, an investment cannot grow at the same rate year after year. Despite this, the CAGR calculator is widely used to compare alternative investments.")

    rcol1,rcol2 = st.columns(2, gap='large')
    with rcol1:
        # with st.form(key="cagrcal", clear_on_submit=True):
        start_value = st.number_input("Initial Value", format="%d", value=800000, step=1000)
        end_value = st.number_input("Final Value Costs", format="%d", value=2100000, step=1000)
        num_periods = st.number_input("Duration of Investment", format="%d", value=6)

        CAGR = cagr(start_value, end_value, num_periods)
        CAGR = CAGR*100
        CAGR = round(CAGR, 2)
        # st.metric(CAGR)
        st.metric("CAGR",  f"{CAGR}")


    df = pd.DataFrame({
        'x' :['Initial Value','Final Value'],
        'y' :[start_value,end_value]})
    with rcol2:
        fig1 = px.pie(
            df,
            values="y",names="x",
            hole=0.55, 
            
            width=685
        )

        fig1.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',

        )
        st.plotly_chart(fig1)
    
    st.markdown("---")
    st.markdown("###")
    st.title("Basic Tax Structure According to 2023")
    tax_data = pd.DataFrame(
        data={"Investment":["5-Year Bank Fixed Deposit","Public Provident Fund (PPF)", "National Savings Certificate", "National Pension System (NPS)", "ELSS Funds","Unit Linked Insurance Plan (ULIP)","Sukanya Samriddhi Yojana (SSY)","Senior Citizen Saving Scheme (SCSS)"],
        "Returns": ["6% to 7%", "7% to 8%", "7% to 8%", "12% to 14%", "	15% to 18%", "Varies with Plan Chosen","7.60%","7.40%"],
        "Lock-in Period":["5 years", "15 years", "5 years", "Till Retirement", "3 years","5 years","N/A","5 years"],      
    })
    st.markdown("###")
    st.table(data=tax_data)

    st.markdown("---")    
    sum = 0
    st.header("Tax Deduction")
    health_insurance_value = 0

    health_sum = 0
    ecar_sum = 0
    home_loan_sum = 0
    home_rent_sum=0
    student_sum = 0
    interest_bank_sum = 0
    disability_sum = 0
    royalty_sum = 0 

    health_insurance = st.checkbox("Health Insurance")
    if health_insurance:
        health_insurance_value = st.number_input(label="Enter Value:", format="%d", value=0, key="health")
        if(health_insurance_value > 25000):
            health_sum =  25000
        else:
            health_sum = health_insurance_value

        sum += health_sum

    ecar_loan = st.checkbox("Electric Car Loan")
    if ecar_loan:
        ecar_loan_value = st.number_input(label="Enter Value:", format="%d", value=0, key="ecar")
        ecar_loan_owner = st.selectbox("Is the vehicle registered in the name of the owner or the business enterprise", ["Yes", "No"])
        ecar_loan_period = st.selectbox("Is the loan sanctioned during the period starting from April 1, 2019, to March 31, 2023", ["Yes", "No"])
        ecar_loan_first = st.selectbox("Is this your first purchase of an electric vehicle", ["Yes", "No"])
        if(ecar_loan_owner=="Yes" and ecar_loan_period=="Yes" and ecar_loan_first=="Yes"):
            ecar_sum = 150000
        else:
            st.markdown(f"""<p style="font-size:16px;color:red;margin-top:-15px;">*You are not eligible for any tax deduction</p>""", unsafe_allow_html=True)

        sum += ecar_sum

    home_loan = st.checkbox("Home Loan")
    if home_loan:
        home_question = st.selectbox("Did own any property on the date of the sanctioned loan?", ["No", "Yes"])
        certificate_question = st.selectbox("Have you been provided interest certificate for the Loan by the Bank?", ["Yes", "No"])
        home_loan_value = st.number_input(label="Enter Loan Amount:", format="%d", value=150000, key="home_amount")
        propertry_cost = st.number_input(label="Enter Cost of Property:", format="%d", value=40000, key="property_cost")
        principal_component = st.number_input(label="Enter Principal Component:", format="%d", value=100000, key="principal_componet")
        interest_component = st.number_input(label="Enter Interest Component:", format="%d", value=50000, key="interest_component")
        if(home_loan_value>3500000 or propertry_cost>5000000 or home_question=="Yes" or certificate_question=="No"):
            home_loan_sum = 0
            st.markdown(f"""<p style="font-size:16px;color:red;margin-top:-15px;">*You are not eligible for any tax deduction</p>""", unsafe_allow_html=True)
        else:
            if(principal_component < 150000):
                principal = principal_component
            else:
                principal = 150000
            if(interest_component < 200000):
                interest = interest_component
            else:
                interest = 200000
            
            home_loan_sum = principal + interest 

        sum += home_loan_sum

    home_rent = st.checkbox("Home Rent")
    if home_rent:
        home_rent_resident = st.selectbox("Are you residing in the rented property?", ["Yes", "No"], key="resident")
        home_rent_HRA = st.selectbox("Have you received home rent allowance from your employer?", ["No", "Yes"], key="home_hra")
        home_rent_value = st.number_input(label="Enter rent per annum:", format="%d", value=150000, key="rent")
        home_rent_income = st.number_input(label="Enter Income per annum:", format="%d", value=500000, key="income")
        deduction1=60000
        rent= (home_rent_income*10)/100
        deduction2 = home_rent_value-rent

        deduction3 = (home_rent_income*25)/100
    
        if(home_rent_resident == "Yes" and home_rent_HRA == "No"):
            if(deduction2>0 and deduction3>0):
                if(deduction2 < 60000 and deduction2 < deduction3):
                    home_rent_sum = deduction2
                elif(deduction3 < 60000 and deduction3 < deduction2):
                    home_rent_sum = deduction3
                else:
                    home_rent_sum = deduction1
            else:
                st.markdown(f"""<p style="font-size:16px;color:red;margin-top:-15px;">*You are not eligible for any tax deduction</p>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""<p style="font-size:16px;color:red;margin-top:-15px;">*You are not eligible for any tax deduction</p>""", unsafe_allow_html=True)
        
        sum += home_rent_sum

    student_loan = st.checkbox("Student Loan")
    if student_loan:
        student_certificate = st.selectbox("Do you have Education Loan Certificate provided by your Bank?", ["Yes", "No"])
        student_interest = st.number_input(label="Enter Interest Amount:", format="%d", value=0, key="student_interest")
        if(student_certificate=='Yes'):
            student_sum = student_interest
        else:
            st.markdown(f"""<p style="font-size:16px;color:red;margin-top:-15px;">*You are not eligible for any tax deduction</p>""", unsafe_allow_html=True)
        
        sum += student_sum

    interest_on_bank_acc = st.checkbox("Interest on Bank Account")
    if interest_on_bank_acc:
        interest_on_bank_acc_value = st.number_input(label="Enter Interest Income from Savings Bank Account:", format="%d", value=0, key="interest_on_bank_acc")
        if(interest_on_bank_acc_value<=10000):
            interest_bank_sum = interest_on_bank_acc_value
        else:
            interest_bank_sum = 10000

        sum += interest_bank_sum

    ddr = st.checkbox("Disability, Dependent, Relatives")
    if ddr:
        ddr_certificate = st.selectbox("Do you have certificate certifying the disability from a recognized medical authority in Form 10-IA?", ["Yes", "No"], key="ddr_cert")
        level_disability = st.number_input("Enter the level of disability(in %) as mentioned in certificate:", format="%d", value=40, key="level_disability")
        if (ddr_certificate == 'Yes'):
            if(health_insurance):
                if (level_disability>=80):
                    disability_sum = 125000 - health_insurance_value
                elif (level_disability>=40):
                    disability_sum = 75000 - health_insurance_value
                else:
                    st.markdown(f"""<p style="font-size:16px;color:red;margin-top:-15px;">*You are not eligible for any tax deduction</p>""", unsafe_allow_html=True)
            else:
                if (level_disability>=80):
                    disability_sum = 125000 
                elif (level_disability>=40):
                    disability_sum = 75000 
                else:
                    st.markdown(f"""<p style="font-size:16px;color:red;margin-top:-15px;">*You are not eligible for any tax deduction</p>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""<p style="font-size:16px;color:red;margin-top:-15px;">*You are not eligible for any tax deduction</p>""", unsafe_allow_html=True)

        sum += disability_sum

    royalty_income = st.checkbox("Royalty Income")
    if royalty_income:
        royalty_income_value = st.number_input(label="Enter Value:", format="%d", value=0, key="royalty_income")
        royalty_income_patent = st.selectbox("Is your patent registered under the Patent Act 1970?", ["Yes", "No"], key="patent")
        if(royalty_income_patent):
            if(royalty_income_value>=300000):
                royalty_sum = 300000
            else:
                royalty_sum = royalty_income_value
        else:
            st.markdown(f"""<p style="font-size:16px;color:red;margin-top:-15px;">*You are not eligible for any tax deduction</p>""", unsafe_allow_html=True)

        sum += royalty_sum

    st.markdown(f"""<h4 style="padding:5px; background-color:#8753b8; width:300px; border-radius:5px">Tax: Deduction: {sum}</h4>""", unsafe_allow_html=True)

    tax_deduction_data = {
        "Category": ["Health Insurance", "Electric Car Loan", "Home Loan", "Home Rent", "Student Loan", 
                    "Interest on Bank Account", "Disability, Dependent, Relatives", "Royalty Income", "Total"],
        "Section": ["80D", "80EEB", "24, 80C, 80EE", "80GG", "80E", "80TTA", "80DD", "80RRB","-"],
        "Amount Deducted": [health_sum, ecar_sum, home_loan_sum, home_rent_sum, student_sum, interest_bank_sum,
                            disability_sum, royalty_sum, sum]
    }
    st.markdown("###")
    st.table(tax_deduction_data)
	
def calculate(amount, percent):
	return (amount * percent) / 100

def calculate_income_tax(total_income:float) -> float:
	if total_income <= 250000:
		return 0
	elif total_income <= 500000:
		return calculate(total_income - 250000, 5)
	elif total_income <= 750000:
		return calculate(total_income - 500000, 10) + 12500						
	elif total_income <= 1000000:
		return calculate(total_income - 750000, 15) + 37500						
	elif total_income <= 1250000:
		return calculate(total_income - 1000000, 20) + 75000						
	elif total_income <= 1500000:
		return calculate(total_income - 1250000, 25) + 125000						
	else:
		return calculate(total_income - 1500000, 30) + 187500
	

def cagr(start_value, end_value, num_periods):
    return (end_value / start_value)**(1 / num_periods) - 1
