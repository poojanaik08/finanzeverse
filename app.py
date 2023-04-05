import streamlit as st
from PIL import Image
import hydralit_components as hc

from login import login
from signup import signup
from about import about

image = Image.open("images/logo_f.png")
page_title = "Finanzeverse"
page_icon = image
st.set_page_config(page_title=page_title, page_icon=image,layout="wide", initial_sidebar_state="collapsed")

page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    position: absolute;
    left: 0px;
    top: 0px;
    background: linear-gradient(175deg, rgba(24,24,24,1) 0%, rgba(48,8,70,1) 97%);
    backdrop-filter: blur(5px);
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
        """
st.markdown(hide_st_style, unsafe_allow_html=True)


def main():
    menu_data = [
        {'label':"Finanzeverse"},
        {'label':"Login"},
        {'label':"Signup"},
        {'label':"About"},
    ]
    over_theme = {'txc_inactive': 'white','menu_background':'purple','txc_active':'white','option_active':'black'}

    menu_id = hc.nav_bar(
        menu_definition=menu_data,
        override_theme=over_theme,
    )
    if menu_id == "Finanzeverse":
        image = Image.open("images/Setup 3.0.png")
        st.image(image, caption='')

        st.write("---")

        new_title = '<p style="font-family:Roboto; color:White; font-size: 44px; letter-spacing: 0.1em;text-align: center;top: 1000px;left: 363px; text-shadow: -1.5px 6px 4px rgba(0, 0, 0, 0.2);">How you Deal With Your Finance ???</p>'
        st.markdown(new_title, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            image = Image.open("images/lady_stress1.png")
            st.image(image, caption='')
            new_title = '<p style="font-family:Roboto; color:White; font-size: 44px; letter-spacing: 0.1em;text-align: left;top: 1000px;left: 363px;">Still using old paper files!</p>'
            st.markdown(new_title, unsafe_allow_html=True)
            new_title = '<p style="font-family:Roboto; color:White; font-size: 24px; letter-spacing: 0.1em;text-align: left;top: 1000px;left: 363px;">✖ Stressful<br>✖ Takes lot of Time<br>✖ Numerous Mistakes<br>✖ Costly</p>'
            st.markdown(new_title, unsafe_allow_html=True)

        with col2:
            image = Image.open("images/person_dash1.png")
            st.image(image, caption='')
            new_title = '<p style="font-family:Roboto; color:White; font-size: 44px; letter-spacing: 0.1em;text-align: left;top: 1000px;left: 363px;">Go Digitalise</p>'
            st.markdown(new_title, unsafe_allow_html=True)
            new_title = '<p style="font-family:Roboto; color:White; font-size: 24px; letter-spacing: 0.1em;text-align: left;top: 1000px;left: 363px;">✔ Easy to use<br>✔ Automated work<br>✔ Faster calculation<br>✔ Tension free</p>'
            st.markdown(new_title, unsafe_allow_html=True)

        st.write("---")


        new_title = '<p style="font-family:Roboto; color:White; font-size: 44px; letter-spacing: 0.1em;text-align: center;top: 1000px;left: 363px; text-shadow: -1.5px 6px 4px rgba(0, 0, 0, 0.2);"><br><br>MANAGE YOUR MONEY WITH FINANZEVERSE</p>'
        st.markdown(new_title, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            text='<p><br><br><br></>'
            st.markdown(text, unsafe_allow_html=True)
            new_title = '<p style="font-family:Poppins; color:White; font-size: 28px; letter-spacing: 0.12em;text-align:center; top: 1000px;left: 363px;">We offer you access to a wide range of services<br> that have been thoughtfully developed<br> to be intuitive, engaging and easy to use.</p>'
            st.markdown(new_title, unsafe_allow_html=True) 
            new_title = '<p style="font-family:Roboto; color:White; font-size: 18px; letter-spacing: 0.1em;text-align: center; text-shadow: -1.5px 6px 4px rgba(0, 0, 0, 0.2);"><br><br>☑ DASHBOARD &emsp;☑ LOAN PLANNER &emsp;☑ BUDGET PLANNER</p>'
            st.markdown(new_title, unsafe_allow_html=True)

        with col2:
            image = Image.open("images/Meet.png")
            st.image(image, caption='')

        st.write("---")

        new_title = '<p style="font-family:Roboto; color:White; font-size: 44px; letter-spacing: 0.1em;text-align: center;top: 1000px;left: 363px; text-shadow: -1.5px 6px 4px rgba(0, 0, 0, 0.2);">YOUR PERSONAL DASHBOARD</p>'
        st.markdown(new_title, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            image = Image.open("images/lady_dash 1.png")
            st.image(image, caption='')
            
        with col2:
            text='<p><br><br><br></>'
            st.markdown(text, unsafe_allow_html=True)
            new_title = '<p style="font-family:Poppins; color:White; font-size: 28px; letter-spacing: 0.12em;text-align:center; top: 1000px;left: 363px;">Graphical representation of growth and<br> indication key factor, KPIS, Timeline and<br> Filtering feature, Expense Breakdown<br> and Saving Breakdown (%).</p>'
            st.markdown(new_title, unsafe_allow_html=True) 

        st.write("---")

        new_title = '<p style="font-family:Roboto; color:White; font-size: 44px; letter-spacing: 0.1em;text-align: center;top: 1000px;left: 363px; text-shadow: -1.5px 6px 4px rgba(0, 0, 0, 0.2);"><br>LOAN PLANNER<br>[EMI PLANNING]<br></p>'
        st.markdown(new_title, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            text='<p><br><br><br></>'
            st.markdown(text, unsafe_allow_html=True)
            new_title = '<p style="font-family:Poppins; color:White; font-size: 28px; letter-spacing: 0.12em;text-align:center; top: 1000px;left: 363px;">Option of Loan Planner to manage <br>other KPIs according to EMI.</p>'
            st.markdown(new_title, unsafe_allow_html=True) 
            new_title = '<p style="font-family:Roboto; color:White; font-size: 28px; letter-spacing: 0.1em;text-align: center;top: 1000px;left: 363px;">Get an EMI plan for after filling the details <br>form of your loan.</p>'
            st.markdown(new_title, unsafe_allow_html=True)

        with col2:
            image = Image.open("images/man_dash 1.png")
            st.image(image, caption='')

        st.write("---")

        new_title = '<p style="font-family:Roboto; color:White; font-size: 44px; letter-spacing: 0.1em;text-align: center;top: 1000px;left: 363px; text-shadow: -1.5px 6px 4px rgba(0, 0, 0, 0.2);"><br>BUDGET PLANNER<br><br></p>'
        st.markdown(new_title, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            image = Image.open("images/lady_budget 1.png")
            st.image(image, caption='')
            
        with col2:
            text='<p><br><br><br></>'
            st.markdown(text, unsafe_allow_html=True)
            new_title = '<p style="font-family:Poppins; color:White; font-size: 28px; letter-spacing: 0.12em;text-align:center; top: 1000px;left: 363px;">A Planner to create a Saving Plan and manage expenses.</p>'
            st.markdown(new_title, unsafe_allow_html=True) 
            new_title = '<p style="font-family:Roboto; color:White; font-size: 28px; letter-spacing: 0.1em;text-align: center;top: 1000px;left: 363px;">A goal setter according to which saving plan can be implemented.</p>'
            st.markdown(new_title, unsafe_allow_html=True)

        st.write("---")
        st.image("images/Footer.png")


    if menu_id == "Login":
        login()
    if menu_id == "Signup":
        signup()
    if menu_id == "About":
        about()
if __name__ == "__main__":
    main()

