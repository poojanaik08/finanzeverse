import streamlit as st
import plotly.express as px
import pandas as pd
import streamlit.components.v1 as components
import numpy as np

def budgetplanner():
    income_df_copy = st.session_state.df.loc[st.session_state.df["Type"]=="Income"]
    income_df_copy['Date'] = pd.to_datetime(income_df_copy['Date'])
    income_df_2022 = income_df_copy[(income_df_copy['Date'] >= '2022-01-04')]
    total_income = income_df_2022["Value"].sum()
    st.title("Your Tax Status:")
    total_income = int(total_income)
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
    
   # st.title("Basic Tax Structure According to 2023")
    # tax_data = pd.DataFrame(
    #     data={"Investment":["5-Year Bank Fixed Deposit","Public Provident Fund (PPF)", "National Savings Certificate", "National Pension System (NPS)", "ELSS Funds","Unit Linked Insurance Plan (ULIP)","Sukanya Samriddhi Yojana (SSY)","Senior Citizen Saving Scheme (SCSS)"],
    #     "Returns": ["6% to 7%", "7% to 8%", "7% to 8%", "12% to 14%", "	15% to 18%", "Varies with Plan Chosen","7.60%","7.40%"],
    #     "Lock-in Period":["5 years", "15 years", "5 years", "Till Retirement", "3 years","5 years","N/A","5 years"],      
    # })
    # st.markdown("###")
    # st.table(data=tax_data)
    st.markdown("###")
    st.header("Basic Tax Structure According to 2023")
    tax_data = pd.DataFrame(
        data={"Income Range":["0 to Rs 2.5 lakh","Rs 2.5 lakh to Rs 5 lakh", "Rs 5 lakh to Rs 7.5 lakh", "Rs 7.50 lakh to Rs 10 lakh", "Rs 10 lakh to Rs 12.5 lakh","Rs 12.5 lakh to Rs 15 lakh","Above Rs 15 lakh"],
        "Tax Applied": [" NIL", "5% above Rs 2.5 lakh", "Rs 12,500 + 10% above Rs 5 lakh", "Rs 37,500 + 15% above Rs 7.5 lakh", "Rs 75,000 + 20% above Rs 10 lakh", "Rs 125,000 + 25% above Rs 12.5 lakh","Rs 187,500 + 30% above Rs 15 lakh"],
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
    st.title("Here are some investement suggestions to save your Taxes:")
    st.markdown("###")
    with st.expander(label="Disclaimer"):
        st.write("Some of the following schemes fall under the Section 80C; according to which you can only get benefits upto 1.5 Lakh collectively.")

    col1, col2, col3,  = st.columns(3, gap="large")
    with col1:
        card_container1 = st.container()
        with card_container1:
            #st.header("PPF")
            st.markdown("""<h2 style="color:#DA70D6;">PPF</h2>""",unsafe_allow_html=True)
            st.subheader("1.5 lakh")
            st.write("The current PPF interest rate is 7.1% (Q4 of FY 2022-23), the minimum investment tenure is fixed at 15 years while the investment amount can range between Rs. 500 to Rs. 1.50 lakh in a financial year.")

    with col2:
        card_container2 = st.container()
        with card_container2:
            #st.header("National Pension System (NPS)")
            st.markdown("""<h2 style="color:#DA70D6;">National Pension System (NPS)</h2>""",unsafe_allow_html=True)
            st.subheader("2 lakh")
            st.write("NPS account tax benefits extend up to ₹2,00,000 per annum for each individual. As an investor, investing this amount will make you eligible to claim ₹1,50,000 tax deduction under Section 80C and an additional ₹50,000 under Section 80CCD(1B).")

    with col3:
        card_container3 = st.container()
        with card_container3:
            #st.header("Sukanya Samriddhi")
            st.markdown("""<h2 style="color:#DA70D6;">Sukanya Samriddhi</h2>""",unsafe_allow_html=True)
            st.subheader("1.5 lakh")
            st.write("The minimum annual contribution to the Sukanya Samriddhi Account is Rs. 250 and the maximum contribution is Rs. 1.5 lakh in a financial year. You have to invest at least the minimum amount every year for up to 15 years from the date of account opening.")

    st.markdown("###")
    col1, col2, col3 = st.columns(3, gap="large")
    with col1:
        card_container1 = st.container()
        with card_container1:
            #st.header("Tax-Saving FD")
            st.markdown("""<h2 style="color:#DA70D6;">Tax-Saving FD</h2>""",unsafe_allow_html=True)
            st.subheader("1.5 lakh")
            st.write("A 5-year term deposit is also called a Tax-Saving FD. If you invest in one, you are eligible for tax deductions under Section 80C of the Income Tax Act, 1961. You can claim up to a maximum of Rs.1.5 lakh.")

    with col2:
        card_container2 = st.container()
        with card_container2:
            #st.header("A Senior Citizens’ Saving Scheme (SCSS)")
            st.markdown("""<h2 style="color:#DA70D6;">A Senior Citizens’ Saving Scheme (SCSS)</h2>""",unsafe_allow_html=True)
            st.subheader("1.08 lakh")
            st.write("A Senior Citizens’ Saving Scheme (SCSS) is a government-backed retirement benefits programme. Senior citizens resident in India can invest a lump sum in the scheme, Get an income tax deduction of up to Rs.1.5 lakh under Section 80C of the Indian Tax Act, 1961.")

    with col3:
        card_container3 = st.container()
        with card_container3:
            #st.header("ELSS")
            st.markdown("""<h2 style="color:#DA70D6;">ELSS</h2>""",unsafe_allow_html=True)
            st.subheader("1.08 lakh")
            st.write("ELSS funds are equity funds that allow you to save tax while you invest for your long term goals. Investment in these funds can are eligible for deduction under Section 80c. These dual benefits mean anyone looking to invest up to Rs. 9,000 per month should only invest in this category.")


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



