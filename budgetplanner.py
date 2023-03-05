import streamlit as st
import plotly.express as px
import pandas as pd
import streamlit.components.v1 as components

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
        # data_frame= st.session_state.savings_df,
            hole=0.55,
            # labels = "Component",
            # names= "Component",
            width=685
        )

        fig1.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
        )
        st.plotly_chart(fig1)
	


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

